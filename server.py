#!/usr/bin/env python3
"""Пульс: zero-dependency local analytics service for VK, Telegram and MAX."""

import json
import html
import base64
import hashlib
import hmac
import os
import re
import secrets
import ssl
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import persistent_store as store
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone, date
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from http.cookies import SimpleCookie

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "app"
DATA_DIR = ROOT / "data"
RUNTIME_FILE = DATA_DIR / "runtime.json"
ACCOUNT_FILE = DATA_DIR / "account.json"
CONNECTIONS_FILE = DATA_DIR / "connections.json"
USERS_FILE = DATA_DIR / "users.json"
FOLDERS_FILE = DATA_DIR / "folders.json"
FOLDER_DIR = DATA_DIR / "folders"
LOCK = store.StoreLock("data")
SYNC_LOCK = store.StoreLock("sync")
SESSIONS = {}

PLATFORMS = ("vk", "telegram", "max")


def load_dotenv():
    path = ROOT / ".env"
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def folder_path(folder_id, name):
    return FOLDER_DIR / folder_id / name


def read_runtime(folder_id):
    with LOCK:
        try:
            return store.read_json(folder_path(folder_id, "runtime.json"))
        except (FileNotFoundError, json.JSONDecodeError):
            return {"last_sync": None, "platforms": {}, "events": []}


def write_runtime(folder_id, data):
    with LOCK:
        store.write_json(folder_path(folder_id, "runtime.json"), data)


def read_secure_json(path, default):
    with LOCK:
        try:
            return store.read_json(path)
        except (FileNotFoundError, json.JSONDecodeError):
            return default


def write_secure_json(path, data):
    with LOCK:
        store.write_json(path, data)


def password_hash(password, salt=None):
    salt_bytes = base64.b64decode(salt) if salt else os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_bytes, 240000)
    return base64.b64encode(salt_bytes).decode("ascii"), base64.b64encode(digest).decode("ascii")


def verify_password(password, account):
    _, digest = password_hash(password, account["salt"])
    return hmac.compare_digest(digest, account["password_hash"])


def default_connections():
    return {key: {"url": "", "target_id": "", "token": "", "webhook_secret": secrets.token_urlsafe(24)} for key in PLATFORMS}


def migrate_legacy():
    """One-time copy; retain the original files as a recovery backup."""
    if store.remote_enabled():
        if not store.exists(USERS_FILE) or not store.exists(FOLDERS_FILE):
            raise RuntimeError("Сначала перенесите существующие аккаунты и папки в постоянное хранилище")
        return
    with LOCK:
        if store.exists(USERS_FILE):
            return
        try:
            legacy = store.read_json(ACCOUNT_FILE)
        except (FileNotFoundError, json.JSONDecodeError):
            legacy = None
        users = {}
        folders = {}
        if legacy:
            user_id = secrets.token_hex(12)
            legacy.update({"id": user_id, "role": "admin", "premium": False, "extra_folders": 0, "blocked": False})
            users[user_id] = legacy
            folder_id = secrets.token_hex(12)
            folders[folder_id] = {"id": folder_id, "owner_id": user_id, "name": "Министерство молодёжной политики ЛНР", "blocked": False, "blocked_projects": []}
            if store.exists(CONNECTIONS_FILE):
                write_json_unlocked(folder_path(folder_id, "connections.json"), store.read_json(CONNECTIONS_FILE))
            if store.exists(RUNTIME_FILE):
                write_json_unlocked(folder_path(folder_id, "runtime.json"), store.read_json(RUNTIME_FILE))
        write_json_unlocked(FOLDERS_FILE, folders)
        write_json_unlocked(USERS_FILE, users)


def ensure_first_folders():
    """Upgrade accounts registered before automatic starter folders were introduced."""
    with LOCK:
        users = store.read_json(USERS_FILE)
        folders = store.read_json(FOLDERS_FILE)
        changed = False
        for user_id in users:
            if any(folder["owner_id"] == user_id for folder in folders.values()):
                continue
            folder_id = secrets.token_hex(12)
            folders[folder_id] = {"id": folder_id, "owner_id": user_id, "name": "Моя первая папка", "blocked": False, "blocked_projects": []}
            changed = True
        if changed:
            write_json_unlocked(FOLDERS_FILE, folders)


def write_json_unlocked(path, data):
    store.write_json(path, data)


def public_user(user, for_admin=False):
    result = {key: user.get(key) for key in ("id", "name", "email", "role", "created_at")}
    if for_admin or user.get("premium"):
        result["premium"] = bool(user.get("premium"))
    if for_admin:
        result.update({"extra_folders": user.get("extra_folders", 0), "blocked": user.get("blocked", False)})
    return result


def folder_limit(user):
    return (3 if user.get("premium") else 1) + user.get("extra_folders", 0)


def owned_folder(user, folder_id, platform=None):
    folder = read_secure_json(FOLDERS_FILE, {}).get(folder_id)
    if not folder or folder["owner_id"] != user["id"]:
        raise PermissionError("Папка не найдена")
    if folder.get("blocked"):
        raise PermissionError("Папка заблокирована администратором")
    if platform and platform in folder.get("blocked_projects", []):
        raise PermissionError("Проект заблокирован администратором")
    return folder


def load_connections(folder_id):
    defaults = default_connections()
    path = folder_path(folder_id, "connections.json")
    if not store.exists(path):
        store.write_json(path, defaults, only_if_missing=True)
    saved = read_secure_json(path, {})
    for platform in defaults:
        defaults[platform].update(saved.get(platform, {}))
    return defaults


def save_connection(folder_id, platform, payload):
    if platform not in ("vk", "telegram", "max"):
        raise ValueError("Неизвестная площадка")
    connections = load_connections(folder_id)
    current = connections[platform]
    url = str(payload.get("url") or current.get("url") or "").strip()
    parsed = urllib.parse.urlparse(url)
    allowed_hosts = {
        "vk": ("vk.ru", "vk.com", "www.vk.ru", "www.vk.com"),
        "telegram": ("t.me", "www.t.me"),
        "max": ("max.ru", "www.max.ru"),
    }
    if parsed.scheme != "https" or parsed.netloc.lower() not in allowed_hosts[platform]:
        raise ValueError("Укажите корректную HTTPS-ссылку на выбранной площадке")
    new_target_value = payload.get("target_id") if "target_id" in payload else current.get("target_id", "")
    new_target_id = str(new_target_value or "").strip()
    identity_changed = url.rstrip("/") != current.get("url", "").rstrip("/") or new_target_id != current.get("target_id", "")
    token = payload.get("token")
    if token:
        current["token"] = token.strip()
    current.update({
        "url": url.rstrip("/"),
        "target_id": new_target_id,
        "confirmation_code": str(payload.get("confirmation_code") or current.get("confirmation_code") or "").strip(),
        "webhook_secret": current.get("webhook_secret") or secrets.token_urlsafe(24),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })
    connections[platform] = current
    write_secure_json(folder_path(folder_id, "connections.json"), connections)
    if identity_changed:
        runtime = read_runtime(folder_id)
        runtime.setdefault("platforms", {}).pop(platform, None)
        runtime["snapshots"] = [row for row in runtime.get("snapshots", []) if row.get("platform") != platform]
        runtime["daily_snapshots"] = {day: {key: value for key, value in entries.items() if key != platform} for day, entries in runtime.get("daily_snapshots", {}).items()}
        runtime["post_archive"] = {key: value for key, value in runtime.get("post_archive", {}).items() if value.get("platform") != platform}
        if platform == "vk":
            runtime.pop("vk_history", None)
        write_runtime(folder_id, runtime)
    return current


def safe_connections(folder_id):
    connections = load_connections(folder_id)
    blocked = read_secure_json(FOLDERS_FILE, {}).get(folder_id, {}).get("blocked_projects", [])
    base_url = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
    result = {}
    for platform, item in connections.items():
        if platform in blocked:
            continue
        result[platform] = {
            "url": item.get("url", ""),
            "target_id": item.get("target_id", ""),
            "has_token": bool(item.get("token")),
            "confirmation_code": item.get("confirmation_code", ""),
            "webhook_secret": item.get("webhook_secret", "") if platform == "vk" else "",
            "webhook_url": "%s/webhooks/%s/%s" % (base_url, platform, folder_id) if base_url else "",
        }
    return result


def create_session(user_id):
    token = secrets.token_urlsafe(32)
    if store.remote_enabled():
        store.save_session(token, user_id)
    else:
        SESSIONS[token] = (user_id, time.time() + 86400)
    return token


def cleanup_sessions():
    now = time.time()
    for token, expires in list(SESSIONS.items()):
        if expires[1] < now:
            SESSIONS.pop(token, None)


def fetch_json(url, headers=None, method="GET", payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={"User-Agent": "PulseAnalytics/1.0", "Content-Type": "application/json", **(headers or {})},
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            detail = json.loads(exc.read().decode("utf-8")).get("description")
        except Exception:
            detail = None
        raise RuntimeError(detail or "API вернул ошибку HTTP %s" % exc.code)
    except urllib.error.URLError as exc:
        raise RuntimeError("Нет связи с API: %s" % exc.reason)


def fetch_text(url):
    request = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; PulseAnalytics/1.0; +http://localhost)",
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.7",
    })
    for attempt in range(2):
        try:
            with urllib.request.urlopen(request, timeout=18) as response:
                return response.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            raise RuntimeError("Публичная страница вернула HTTP %s" % exc.code)
        except (urllib.error.URLError, TimeoutError) as exc:
            reason = exc.reason if isinstance(exc, urllib.error.URLError) else exc
            transient = isinstance(reason, (TimeoutError, ConnectionResetError, ConnectionAbortedError)) or (
                isinstance(reason, ssl.SSLError) and "timed out" in str(reason).lower()
            )
            if attempt == 0 and transient:
                time.sleep(0.5)
                continue
            raise RuntimeError("Нет связи с публичной страницей: %s" % reason)


def clean_html(value):
    value = re.sub(r"<br\s*/?>", "\n", value or "", flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def parse_public_count(value):
    raw = html.unescape(value or "").strip().upper().replace(" ", "").replace(",", ".")
    match = re.search(r"([\d.]+)\s*([KКMМ]?)", raw)
    if not match:
        return 0
    number_value = float(match.group(1))
    suffix = match.group(2)
    if suffix in ("K", "К"):
        number_value *= 1000
    elif suffix in ("M", "М"):
        number_value *= 1000000
    return int(number_value)


def public_vk(url=None):
    target_url = url
    page = fetch_text(target_url)
    members = re.search(r'"members_count":(\d+)', page)
    wall_count = re.search(r'"main_type":"wall","main_type_count":(\d+)', page)
    screen_name = target_url.rstrip("/").rsplit("/", 1)[-1]
    name = re.search(r'"name":"([^"\\]*(?:\\.[^"\\]*)*)","screen_name":"%s"' % re.escape(screen_name), page)
    if not members:
        raise RuntimeError("VK не отдал число подписчиков на публичной странице")
    title = "Министерство молодёжной политики ЛНР"
    if name:
        try:
            title = json.loads('"%s"' % name.group(1))
        except json.JSONDecodeError:
            pass
    return {
        "configured": True,
        "status": "connected",
        "source": "public",
        "url": target_url,
        "name": title,
        "subscribers": int(members.group(1)),
        "posts_count": int(wall_count.group(1)) if wall_count else 0,
        "recent_posts": [],
    }


def parse_telegram_posts(page):
    marker = re.compile(r'<div class="tgme_widget_message[^>]+data-post="([^"]+)"', re.I)
    matches = list(marker.finditer(page))
    posts = []
    for index, match in enumerate(matches):
        segment = page[match.start():(matches[index + 1].start() if index + 1 < len(matches) else len(page))]
        text_match = re.search(r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>', segment, re.I | re.S)
        title = clean_html(text_match.group(1)) if text_match else "Публикация без текста"
        views_match = re.search(r'<span class="tgme_widget_message_views">([^<]+)</span>', segment, re.I)
        date_match = re.search(r'<time datetime="([^"]+)"', segment, re.I)
        reactions = 0
        for reaction in re.findall(r'<span class="tgme_reaction"[^>]*>(.*?)</span>', segment, re.I | re.S):
            count_match = re.search(r'(\d[\d\s.,KКMМ]*)\s*$', clean_html(reaction))
            if count_match:
                reactions += parse_public_count(count_match.group(1))
        views = parse_public_count(views_match.group(1)) if views_match else 0
        iso_date = date_match.group(1) if date_match else None
        display_date = "Дата не указана"
        if iso_date:
            try:
                post_date = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
                display_date = post_date.strftime("%d.%m.%Y, %H:%M")
            except ValueError:
                display_date = iso_date
        post_path = match.group(1)
        posts.append({
            "id": "telegram-%s" % post_path.rsplit("/", 1)[-1],
            "platform": "telegram",
            "title": title[:220],
            "date": display_date,
            "published_at": iso_date,
            "type": "Публикация",
            "reach": views,
            "reactions": reactions,
            "comments": 0,
            "er": round(reactions / views * 100, 2) if views else 0,
            "trend": 0,
            "url": "https://t.me/%s" % post_path,
        })
    return posts


def public_telegram(url=None):
    target_url = url
    profile = fetch_text(target_url)
    username = target_url.rstrip("/").rsplit("/", 1)[-1]
    feed = fetch_text("https://t.me/s/%s" % username)
    subscribers = re.search(r'<div class="tgme_page_extra">\s*([^<]+?)\s+subscribers', profile, re.I)
    name = re.search(r'<meta property="og:title" content="([^"]+)"', profile, re.I)
    posts = parse_telegram_posts(feed)
    if not subscribers:
        raise RuntimeError("Telegram не отдал число подписчиков на публичной странице")
    total_views = sum(post["reach"] for post in posts)
    total_reactions = sum(post["reactions"] for post in posts)
    return {
        "configured": True,
        "status": "connected",
        "source": "public",
        "url": target_url,
        "name": html.unescape(name.group(1)) if name else "МинМол ЛНР",
        "subscribers": parse_public_count(subscribers.group(1)),
        "reach": total_views,
        "engagement": round(total_reactions / total_views * 100, 2) if total_views else 0,
        "posts_count": len(posts),
        "recent_posts": posts,
    }


def public_max(url=None):
    target_url = url
    page = fetch_text(target_url)
    followers = re.search(r'"userInteractionCount"\s*:\s*(\d+)', page)
    name = re.search(r'<meta property="og:title" content="([^"]+)"', page, re.I)
    channel_id = re.search(r'channelId:(\d+)', page)
    if not followers:
        raise RuntimeError("MAX не отдал число подписчиков на публичной странице")
    return {
        "configured": True,
        "status": "connected",
        "source": "public",
        "url": target_url,
        "name": html.unescape(name.group(1)) if name else "Минмол ЛНР",
        "subscribers": int(followers.group(1)),
        "chat_id": channel_id.group(1) if channel_id else None,
        "posts_count": 0,
        "recent_posts": [],
    }


def sync_vk(folder_id):
    config = load_connections(folder_id)["vk"]
    token, group_id = config.get("token"), config.get("target_id")
    if not token or not group_id:
        return public_vk(config.get("url"))
    query = urllib.parse.urlencode({
        "group_id": group_id,
        "fields": "members_count,description",
        "access_token": token,
        "v": "5.199",
    })
    data = fetch_json("https://api.vk.com/method/groups.getById?" + query)
    if "error" in data:
        raise RuntimeError(data["error"].get("error_msg", "Ошибка VK API"))
    response = data.get("response", {})
    groups = response if isinstance(response, list) else response.get("groups", [])
    group = groups[0] if groups else {}
    result = {
        "configured": True,
        "status": "connected",
        "source": "api",
        "url": config.get("url"),
        "name": group.get("name", "Сообщество VK"),
        "subscribers": group.get("members_count", 0),
        "recent_posts": [],
    }
    # Расширенная статистика доступна только администраторам. Её отсутствие
    # не должно ломать базовую синхронизацию числа подписчиков.
    try:
        end = int(datetime.now(timezone.utc).timestamp())
        start = end - 30 * 86400
        stats_query = urllib.parse.urlencode({
            "group_id": group_id,
            "timestamp_from": start,
            "timestamp_to": end,
            "interval": "day",
            "access_token": token,
            "v": "5.199",
        })
        stats = fetch_json("https://api.vk.com/method/stats.get?" + stats_query)
        periods = stats.get("response", []) if "error" not in stats else []
        reach = sum((period.get("reach") or {}).get("reach", 0) for period in periods)
        if reach:
            result["reach"] = reach
    except Exception:
        pass
    return result


def sync_telegram(folder_id):
    config = load_connections(folder_id)["telegram"]
    token, chat_id = config.get("token"), config.get("target_id")
    if not token or not chat_id:
        return public_telegram(config.get("url"))
    base = "https://api.telegram.org/bot%s/" % token
    chat_q = urllib.parse.urlencode({"chat_id": chat_id})
    chat = fetch_json(base + "getChat?" + chat_q)
    count = fetch_json(base + "getChatMemberCount?" + chat_q)
    if not chat.get("ok") or not count.get("ok"):
        raise RuntimeError(chat.get("description") or count.get("description") or "Ошибка Telegram API")
    result = chat["result"]
    synced = {
        "configured": True,
        "status": "connected",
        "source": "api",
        "url": config.get("url"),
        "name": result.get("title") or result.get("username") or "Telegram канал",
        "subscribers": count["result"],
        "recent_posts": [],
    }
    # Bot API confirms access and audience, while the public feed exposes
    # current view/reaction counters for public channels.
    try:
        public = public_telegram(config.get("url"))
        synced.update({
            "recent_posts": public.get("recent_posts", []),
            "posts_count": public.get("posts_count", 0),
            "reach": public.get("reach", 0),
            "engagement": public.get("engagement", 0),
        })
    except Exception:
        pass
    return synced


def sync_max(folder_id):
    config = load_connections(folder_id)["max"]
    token, chat_id = config.get("token"), config.get("target_id")
    if not token or not chat_id:
        return public_max(config.get("url"))
    url = "https://platform-api2.max.ru/chats/%s" % urllib.parse.quote(chat_id)
    chat = fetch_json(url, headers={"Authorization": token})
    return {
        "configured": True,
        "status": "connected",
        "source": "api",
        "url": config.get("url"),
        "name": chat.get("title") or "Канал MAX",
        "subscribers": chat.get("participants_count", 0),
        "posts_count": chat.get("messages_count", 0),
        "recent_posts": [],
    }


PLATFORM_BASE = {
    "vk": {"name": "Сообщество VK", "handle": "VK", "url": "https://vk.ru/", "subscribers": 0, "growth": 0, "reach": 0, "engagement": 0, "posts": 0, "color": "#2787F5"},
    "telegram": {"name": "Канал Telegram", "handle": "Telegram", "url": "https://t.me/", "subscribers": 0, "growth": 0, "reach": 0, "engagement": 0, "posts": 0, "color": "#28A8E9"},
    "max": {"name": "Канал MAX", "handle": "MAX", "url": "https://max.ru/", "subscribers": 0, "growth": 0, "reach": 0, "engagement": 0, "posts": 0, "color": "#875BF7"},
}


def make_dashboard(folder_id, period):
    period = period if period in (7, 30, 90) else 30
    runtime = read_runtime(folder_id)
    snapshots = sorted(runtime.get("snapshots", []), key=lambda row: row.get("captured_at", ""))
    platforms = []
    configs = load_connections(folder_id)
    blocked = read_secure_json(FOLDERS_FILE, {}).get(folder_id, {}).get("blocked_projects", [])
    for key, original in PLATFORM_BASE.items():
        if key in blocked:
            continue
        item = {"id": key, **original}
        configured_url = configs[key].get("url") or ""
        slug = urllib.parse.urlparse(configured_url).path.strip("/").split("/")[-1]
        item["url"] = configured_url
        item["handle"] = ("@" + slug) if slug else "Не подключено"
        saved = runtime.get("platforms", {}).get(key, {})
        if configured_url and saved.get("status") == "connected" and saved.get("url", "").rstrip("/") == configured_url.rstrip("/"):
            item["subscribers"] = saved.get("subscribers", item["subscribers"])
            item["name"] = saved.get("name", item["name"])
            item["reach"] = saved.get("reach", 0) or 0
            item["engagement"] = saved.get("engagement", 0) or 0
            item["posts"] = saved.get("posts_count", 0) or 0
            item["source"] = saved.get("source", "public")
            item["url"] = saved.get("url", item["url"])
            item["status"] = "connected"
        else:
            item["status"] = "pending"

        history = [row for row in snapshots if row.get("platform") == key and row.get("subscribers") is not None]
        item["history"] = [row["subscribers"] for row in history[-12:]] or [item["subscribers"]]
        if len(history) >= 2 and history[0]["subscribers"]:
            item["growth"] = round((history[-1]["subscribers"] - history[0]["subscribers"]) / history[0]["subscribers"] * 100, 2)
        platforms.append(item)

    now = datetime.now(timezone.utc)
    start_day = (now - timedelta(days=period - 1)).date()
    all_posts = []
    for key, saved in runtime.get("platforms", {}).items():
        if key in blocked or not configs.get(key, {}).get("url"):
            continue
        all_posts.extend(saved.get("recent_posts") or [])
    posts = []
    for post in all_posts:
        published = post.get("published_at")
        if not published:
            posts.append(post)
            continue
        try:
            if datetime.fromisoformat(published.replace("Z", "+00:00")).date() >= start_day:
                posts.append(post)
        except ValueError:
            posts.append(post)
    posts.sort(key=lambda row: row.get("published_at") or "", reverse=True)

    first_known = {item["id"]: item["subscribers"] for item in platforms}
    first_seen = set()
    by_day = {}
    for row in snapshots:
        if row.get("platform") in blocked or not configs.get(row.get("platform"), {}).get("url"):
            continue
        try:
            row_day = datetime.fromisoformat(row["captured_at"].replace("Z", "+00:00")).date()
        except (KeyError, ValueError):
            continue
        if row.get("subscribers") is not None:
            by_day.setdefault(row_day, {})[row.get("platform")] = row["subscribers"]
            if row.get("platform") not in first_seen:
                first_known[row.get("platform")] = row["subscribers"]
                first_seen.add(row.get("platform"))

    post_days = {}
    for post in posts:
        try:
            post_day = datetime.fromisoformat(post["published_at"].replace("Z", "+00:00")).date()
        except (KeyError, TypeError, ValueError):
            continue
        bucket = post_days.setdefault(post_day, {"reach": 0, "reactions": 0})
        bucket["reach"] += post.get("reach", 0) or 0
        bucket["reactions"] += post.get("reactions", 0) or 0

    running = dict(first_known)
    points = []
    for i in range(period):
        day = start_day + timedelta(days=i)
        running.update(by_day.get(day, {}))
        activity = post_days.get(day, {"reach": 0, "reactions": 0})
        daily_er = round(activity["reactions"] / activity["reach"] * 100, 2) if activity["reach"] else 0
        points.append({"date": day.strftime("%d.%m"), "audience": sum(running.values()), "reach": activity["reach"], "engagement": daily_er})

    total_subscribers = sum(p["subscribers"] for p in platforms)
    total_reach = sum(post.get("reach", 0) or 0 for post in posts)
    total_reactions = sum(post.get("reactions", 0) or 0 for post in posts)
    avg_er = round(total_reactions / total_reach * 100, 2) if total_reach else 0
    history_dates = sorted(set(row.get("captured_at", "")[:10] for row in snapshots if row.get("captured_at")))
    net_growth = points[-1]["audience"] - points[0]["audience"] if len(history_dates) > 1 else 0
    audience_change = round(net_growth / points[0]["audience"] * 100, 2) if points[0]["audience"] else 0
    best_post = max(posts, key=lambda row: row.get("reach", 0), default=None)
    return {
        "period": period,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "last_sync": runtime.get("last_sync"),
        "summary": [
            {"id": "audience", "label": "Общая аудитория", "value": total_subscribers, "format": "number", "change": audience_change, "caption": ("%+d за период" % net_growth) if net_growth else "история накапливается"},
            {"id": "reach", "label": "Публичные просмотры", "value": total_reach, "format": "compact", "change": 0, "caption": "доступные публикации"},
            {"id": "engagement", "label": "Вовлечённость", "value": avg_er, "format": "percent", "change": 0, "caption": "реакции / просмотры"},
            {"id": "posts", "label": "Публикации", "value": len(posts), "format": "number", "change": 0, "caption": "в публичной ленте"},
        ],
        "platforms": platforms,
        "trend": points,
        "posts": posts,
        "audience": {"new": max(net_growth, 0), "left": max(-net_growth, 0), "net": net_growth},
        "insights": [
            {"tone": "violet", "title": "Публичный мониторинг работает", "text": "Аудитория VK, Telegram и MAX обновляется автоматически каждые 30 минут."},
            {"tone": "green", "title": "Лидер по просмотрам" if best_post else "История контента накапливается", "text": ((best_post["title"][:90] + " — %s просмотров" % best_post["reach"]) if best_post else "После синхронизации здесь появятся доступные публикации Telegram.")},
            {"tone": "blue", "title": "Расширенная статистика", "text": "Токены администратора добавят охваты VK и публикации MAX, недоступные на публичных страницах."},
        ],
    }


def connection_status(folder_id):
    runtime = read_runtime(folder_id)
    configs = load_connections(folder_id)
    result = []
    for key in ("vk", "telegram", "max"):
        if key in read_secure_json(FOLDERS_FILE, {}).get(folder_id, {}).get("blocked_projects", []):
            continue
        saved = runtime.get("platforms", {}).get(key, {})
        config = configs[key]
        result.append({
            "id": key,
            "configured": bool(config.get("url")),
            "status": saved.get("status", "ready"),
            "source": saved.get("source", "public"),
            "url": config.get("url", ""),
            "has_token": bool(config.get("token")),
            "realtime": bool(config.get("webhook_active")),
            "name": saved.get("name", PLATFORM_BASE[key]["name"]),
            "error": saved.get("error"),
            "last_sync": saved.get("last_sync"),
        })
    return result


def platform_name(key):
    return {"vk": "VK", "telegram": "Telegram", "max": "MAX"}.get(key, key)


def configure_webhook(folder_id, platform):
    if platform not in ("telegram", "max"):
        raise ValueError("Автоматическая настройка webhook доступна для Telegram и MAX")
    base_url = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
    if not base_url.startswith("https://"):
        raise ValueError("Сначала укажите PUBLIC_BASE_URL с публичным HTTPS-адресом")
    connections = load_connections(folder_id)
    config = connections[platform]
    token = config.get("token")
    if not token:
        raise ValueError("Сначала сохраните токен бота")
    webhook_url = "%s/webhooks/%s/%s" % (base_url, platform, folder_id)
    if platform == "telegram":
        response = fetch_json(
            "https://api.telegram.org/bot%s/setWebhook" % token,
            method="POST",
            payload={
                "url": webhook_url,
                "secret_token": config["webhook_secret"],
                "allowed_updates": ["channel_post", "edited_channel_post", "message_reaction", "message_reaction_count", "chat_member"],
            },
        )
        if not response.get("ok"):
            raise RuntimeError(response.get("description", "Telegram не принял webhook"))
    elif platform == "max":
        response = fetch_json(
            "https://platform-api2.max.ru/subscriptions",
            headers={"Authorization": token},
            method="POST",
            payload={
                "url": webhook_url,
                "update_types": ["message_created", "message_callback", "message_edited", "message_removed", "bot_added"],
                "secret": config["webhook_secret"],
            },
        )
        if response.get("success") is False:
            raise RuntimeError(response.get("message", "MAX не принял webhook"))
    else:
        raise ValueError("Webhook VK подключается вручную по инструкции")
    config["webhook_active"] = True
    config["webhook_configured_at"] = datetime.now(timezone.utc).isoformat()
    connections[platform] = config
    write_secure_json(folder_path(folder_id, "connections.json"), connections)
    return {"ok": True, "webhook_url": webhook_url}


def archive_posts(runtime, platform):
    archive = runtime.setdefault("post_archive", {})
    for post in runtime.get("platforms", {}).get(platform, {}).get("recent_posts") or []:
        if post.get("id") and post.get("published_at"):
            archive["%s:%s" % (platform, post["id"])] = post


def _run_sync(folder_id):
    runtime = read_runtime(folder_id)
    runtime.setdefault("platforms", {})
    runtime.setdefault("snapshots", [])
    synced_at = datetime.now(timezone.utc).isoformat()
    configs = load_connections(folder_id)
    syncers = {"vk": sync_vk, "telegram": sync_telegram, "max": sync_max}
    results = {}
    # Независимые API вызываются параллельно: медленная площадка не блокирует остальные.
    with ThreadPoolExecutor(max_workers=3) as executor:
        blocked = read_secure_json(FOLDERS_FILE, {}).get(folder_id, {}).get("blocked_projects", [])
        futures = {executor.submit(syncer, folder_id): key for key, syncer in syncers.items() if configs[key].get("url") and key not in blocked}
        for future in as_completed(futures):
            key = futures[future]
            try:
                result = future.result()
                result["last_sync"] = synced_at if result.get("configured") else None
                previous = runtime.get("platforms", {}).get(key, {})
                if result.get("source") == "api":
                    merged = {post.get("id"): post for post in previous.get("recent_posts", []) if post.get("id")}
                    merged.update({post.get("id"): post for post in result.get("recent_posts", []) if post.get("id")})
                    posts = sorted(merged.values(), key=lambda post: post.get("published_at") or "", reverse=True)[:100]
                    result["recent_posts"] = posts
                    result["posts_count"] = max(result.get("posts_count", 0) or 0, len(posts))
                    result["reach"] = result.get("reach") or sum(post.get("reach", 0) or 0 for post in posts)
                    reactions = sum(post.get("reactions", 0) or 0 for post in posts)
                    result["engagement"] = result.get("engagement") or (round(reactions / result["reach"] * 100, 2) if result["reach"] else 0)
            except Exception as exc:
                result = {"configured": True, "status": "error", "error": str(exc), "last_sync": synced_at}
            results[key] = result

    for key in ("vk", "telegram", "max"):
        if not configs[key].get("url"):
            runtime["platforms"].pop(key, None)
            continue
        if key in blocked:
            runtime["platforms"].pop(key, None)
            continue
        result = results[key]
        runtime["platforms"][key] = result
        if result.get("status") == "connected":
            snapshot = {
                "platform": key,
                "captured_at": synced_at,
                "subscribers": result.get("subscribers"),
                "reach": result.get("reach"),
                "posts_count": result.get("posts_count"),
            }
            runtime["snapshots"].append(snapshot)
            runtime.setdefault("daily_snapshots", {}).setdefault(synced_at[:10], {})[key] = snapshot
            archive_posts(runtime, key)
    runtime["snapshots"] = runtime["snapshots"][-3000:]
    runtime["last_sync"] = synced_at
    write_runtime(folder_id, runtime)
    return {"ok": True, "last_sync": synced_at, "connections": connection_status(folder_id)}


def run_sync(folder_id):
    with SYNC_LOCK:
        return _run_sync(folder_id)


def validate_report_year(value):
    try:
        year = int(value)
    except (ValueError, TypeError):
        raise ValueError("Укажите год")
    if not 2006 <= year <= datetime.now(timezone.utc).year:
        raise ValueError("Год вне доступного диапазона")
    return year


def fetch_vk_history(folder_id, year):
    config = load_connections(folder_id)["vk"]
    token, group_id = config.get("token"), config.get("target_id")
    if not token or not group_id or not config.get("url"):
        raise ValueError("Для истории VK сохраните токен администратора и ID сообщества")
    start = int(datetime(year, 1, 1, tzinfo=timezone.utc).timestamp())
    end = min(datetime(year + 1, 1, 1, tzinfo=timezone.utc), datetime.now(timezone.utc))
    query = urllib.parse.urlencode({"group_id": group_id, "timestamp_from": start, "timestamp_to": int(end.timestamp()) - 1, "interval": "month", "access_token": token, "v": "5.199"})
    response = fetch_json("https://api.vk.com/method/stats.get?" + query)
    if "error" in response:
        raise RuntimeError(response["error"].get("error_msg", "VK не вернул статистику"))
    periods = response.get("response", [])
    if not isinstance(periods, list):
        raise RuntimeError("VK вернул неожиданный формат статистики")
    months = {}
    for period in periods:
        try:
            point = datetime.fromtimestamp(period["period_from"], timezone.utc)
            if point.year == year:
                month = str(point.month)
                months[month] = months.get(month, 0) + int((period.get("reach") or {}).get("reach", 0) or 0)
        except (KeyError, TypeError, ValueError, OverflowError):
            continue
    with SYNC_LOCK:
        if load_connections(folder_id)["vk"].get("target_id") != group_id:
            raise ValueError("ID сообщества изменился во время загрузки")
        runtime = read_runtime(folder_id)
        runtime.setdefault("vk_history", {})[str(year)] = {"months": months, "fetched_at": datetime.now(timezone.utc).isoformat()}
        write_runtime(folder_id, runtime)
    return {"ok": True, "months_available": len(months)}


def history_report(folder_id, year, grouping):
    if grouping not in ("month", "quarter"):
        raise ValueError("Выберите месяцы или кварталы")
    runtime = read_runtime(folder_id)
    configs = load_connections(folder_id)
    blocked = read_secure_json(FOLDERS_FILE, {}).get(folder_id, {}).get("blocked_projects", [])
    platforms = [key for key in PLATFORMS if configs[key].get("url") and key not in blocked]
    daily = {}
    for snapshot in runtime.get("snapshots", []):
        day, platform = snapshot.get("captured_at", "")[:10], snapshot.get("platform")
        if platform in platforms and len(day) == 10:
            daily.setdefault(day, {})[platform] = max((daily.get(day, {}).get(platform), snapshot), key=lambda row: row.get("captured_at", "") if row else "")
    for day, entries in runtime.get("daily_snapshots", {}).items():
        for platform, snapshot in entries.items():
            if platform in platforms:
                daily.setdefault(day, {})[platform] = max((daily.get(day, {}).get(platform), snapshot), key=lambda row: row.get("captured_at", "") if row else "")

    def period_index(month):
        return month if grouping == "month" else (month - 1) // 3 + 1

    buckets = {}
    for day, entries in daily.items():
        try:
            date_value = date.fromisoformat(day)
        except ValueError:
            continue
        if date_value.year != year:
            continue
        for platform, snapshot in entries.items():
            buckets.setdefault((period_index(date_value.month), platform), {"samples": [], "posts": {}, "vk_reach": None})["samples"].append((day, snapshot.get("subscribers")))

    archive = dict(runtime.get("post_archive", {}))
    for platform, saved in runtime.get("platforms", {}).items():
        for post in saved.get("recent_posts") or []:
            if post.get("id") and post.get("published_at"):
                archive.setdefault("%s:%s" % (platform, post["id"]), post)
    for post in archive.values():
        platform = post.get("platform")
        if platform not in platforms:
            continue
        try:
            published = datetime.fromisoformat(post["published_at"].replace("Z", "+00:00"))
        except (KeyError, AttributeError, ValueError):
            continue
        if published.year == year:
            key = (period_index(published.month), platform)
            buckets.setdefault(key, {"samples": [], "posts": {}, "vk_reach": None})["posts"][post["id"]] = post

    vk_history = runtime.get("vk_history", {}).get(str(year), {})
    if "vk" in platforms:
        for month, reach in vk_history.get("months", {}).items():
            index = period_index(int(month))
            bucket = buckets.setdefault((index, "vk"), {"samples": [], "posts": {}, "vk_reach": None})
            bucket["vk_reach"] = (bucket["vk_reach"] or 0) + reach

    rows = []
    for index in range(1, (12 if grouping == "month" else 4) + 1):
        for platform in platforms:
            bucket = buckets.get((index, platform), {"samples": [], "posts": {}, "vk_reach": None})
            samples = sorted((item for item in bucket["samples"] if item[1] is not None), key=lambda item: item[0])
            posts = list(bucket["posts"].values())
            views = sum(post.get("reach", 0) or 0 for post in posts)
            reactions = sum(post.get("reactions", 0) or 0 for post in posts)
            rows.append({"period": index, "platform": platform, "observed_days": len(samples),
                         "audience": samples[-1][1] if samples else None,
                         "audience_change": samples[-1][1] - samples[0][1] if len(samples) > 1 else None,
                         "posts": len(posts) if posts else None,
                         "post_views": views if posts else None,
                         "reactions": reactions if posts else None,
                         "vk_reach": bucket["vk_reach"]})
    years = {datetime.now(timezone.utc).year}
    for day in daily:
        if day[:4].isdigit():
            years.add(int(day[:4]))
    for post in archive.values():
        published = post.get("published_at") or ""
        if published[:4].isdigit():
            years.add(int(published[:4]))
    years.update(int(key) for key in runtime.get("vk_history", {}) if key.isdigit())
    return {"year": year, "grouping": grouping, "years_with_data": sorted(years, reverse=True), "platforms": platforms,
            "vk_available": "vk" in platforms and bool(configs["vk"].get("token") and configs["vk"].get("target_id")),
            "vk_fetched_at": vk_history.get("fetched_at"), "rows": rows}


def sync_scheduler(stop_event):
    try:
        interval = max(5, int(os.getenv("SYNC_INTERVAL_MINUTES", "30"))) * 60
    except ValueError:
        interval = 1800
    while not stop_event.is_set():
        try:
            folders = read_secure_json(FOLDERS_FILE, {})
            users = read_secure_json(USERS_FILE, {})
            for folder_id, folder in folders.items():
                if not folder.get("blocked") and not users.get(folder["owner_id"], {}).get("blocked"):
                    run_sync(folder_id)
        except Exception as exc:
            print("Ошибка автосинхронизации: %s" % exc)
        stop_event.wait(interval)


def store_webhook_event(folder_id, platform, event):
    with SYNC_LOCK:
        _store_webhook_event(folder_id, platform, event)


def _store_webhook_event(folder_id, platform, event):
    runtime = read_runtime(folder_id)
    events = runtime.setdefault("events", [])
    event_id = event.get("update_id") or event.get("event_id")
    if event_id is not None and any(row.get("platform") == platform and row.get("event_id") == event_id for row in events[-200:]):
        return
    events.append({"platform": platform, "event_id": event_id, "received_at": datetime.now(timezone.utc).isoformat(), "update": event})
    runtime["events"] = events[-1000:]
    if platform == "telegram":
        message = event.get("channel_post") or event.get("edited_channel_post")
        if message:
            chat = message.get("chat", {})
            message_id = message.get("message_id")
            username = chat.get("username")
            published = datetime.fromtimestamp(message.get("date", time.time()), timezone.utc)
            post = {
                "id": "telegram-%s" % message_id,
                "platform": "telegram",
                "title": (message.get("text") or message.get("caption") or "Новая публикация")[:220],
                "date": published.strftime("%d.%m.%Y, %H:%M"),
                "published_at": published.isoformat(),
                "type": "Публикация",
                "reach": 0,
                "reactions": 0,
                "comments": 0,
                "er": 0,
                "trend": 0,
                "url": "https://t.me/%s/%s" % (username, message_id) if username else "",
            }
            platform_data = runtime.setdefault("platforms", {}).setdefault("telegram", {})
            posts = platform_data.setdefault("recent_posts", [])
            posts = [existing for existing in posts if existing.get("id") != post["id"]]
            platform_data["recent_posts"] = ([post] + posts)[:100]
            platform_data["posts_count"] = max(platform_data.get("posts_count", 0) or 0, len(platform_data["recent_posts"]))
        reaction_update = event.get("message_reaction_count")
        if reaction_update:
            post_id = "telegram-%s" % reaction_update.get("message_id")
            reaction_count = sum(item.get("total_count", 0) or 0 for item in reaction_update.get("reactions", []))
            platform_data = runtime.setdefault("platforms", {}).setdefault("telegram", {})
            for post in platform_data.setdefault("recent_posts", []):
                if post.get("id") == post_id:
                    post["reactions"] = reaction_count
                    post["er"] = round(reaction_count / post.get("reach", 0) * 100, 2) if post.get("reach") else 0
                    break
    elif platform == "vk":
        event_type = event.get("type")
        platform_data = runtime.setdefault("platforms", {}).setdefault("vk", {})
        if event_type in ("group_join", "group_leave") and platform_data.get("subscribers") is not None:
            platform_data["subscribers"] = max(0, platform_data["subscribers"] + (1 if event_type == "group_join" else -1))
        if event_type in ("wall_post_new", "wall_repost"):
            raw = event.get("object") or {}
            raw = raw.get("post", raw) if isinstance(raw, dict) else {}
            published = datetime.fromtimestamp(raw.get("date", time.time()), timezone.utc)
            post_id = raw.get("id")
            owner_id = raw.get("owner_id")
            views = (raw.get("views") or {}).get("count", 0)
            reactions = (raw.get("likes") or {}).get("count", 0)
            comments = (raw.get("comments") or {}).get("count", 0)
            post = {
                "id": "vk-%s" % post_id,
                "platform": "vk",
                "title": (raw.get("text") or "Новая публикация VK")[:220],
                "date": published.strftime("%d.%m.%Y, %H:%M"),
                "published_at": published.isoformat(),
                "type": "Публикация",
                "reach": views,
                "reactions": reactions,
                "comments": comments,
                "er": round((reactions + comments) / views * 100, 2) if views else 0,
                "trend": 0,
                "url": "https://vk.ru/wall%s_%s" % (owner_id, post_id) if owner_id and post_id else "",
            }
            posts = [existing for existing in platform_data.setdefault("recent_posts", []) if existing.get("id") != post["id"]]
            platform_data["recent_posts"] = ([post] + posts)[:100]
            platform_data["posts_count"] = max(platform_data.get("posts_count", 0) or 0, len(platform_data["recent_posts"]))
        if event_type in ("wall_reply_new", "wall_reply_delete"):
            raw = event.get("object") or {}
            raw = raw.get("comment", raw) if isinstance(raw, dict) else {}
            post_id = "vk-%s" % raw.get("post_id")
            for post in platform_data.setdefault("recent_posts", []):
                if post.get("id") == post_id:
                    post["comments"] = max(0, (post.get("comments", 0) or 0) + (1 if event_type == "wall_reply_new" else -1))
                    interactions = (post.get("reactions", 0) or 0) + post["comments"]
                    post["er"] = round(interactions / post.get("reach", 0) * 100, 2) if post.get("reach") else 0
                    break
    elif platform == "max":
        platform_data = runtime.setdefault("platforms", {}).setdefault("max", {})
        raw = event.get("message") or event.get("object") or {}
        if isinstance(raw, dict) and isinstance(raw.get("message"), dict):
            raw = raw["message"]
        chat_id = event.get("chat_id") or (raw.get("recipient") or {}).get("chat_id") or raw.get("chat_id")
        if chat_id:
            connections = load_connections(folder_id)
            if not connections["max"].get("target_id"):
                connections["max"]["target_id"] = str(chat_id)
                connections["max"]["updated_at"] = datetime.now(timezone.utc).isoformat()
                write_secure_json(folder_path(folder_id, "connections.json"), connections)
        if event.get("update_type") in ("message_created", "message_edited") and isinstance(raw, dict):
            body = raw.get("body") or {}
            text = body.get("text") if isinstance(body, dict) else ""
            timestamp = raw.get("timestamp") or event.get("timestamp") or int(time.time() * 1000)
            try:
                timestamp = float(timestamp)
            except (TypeError, ValueError):
                timestamp = time.time()
            if timestamp > 100000000000:
                timestamp = timestamp / 1000
            published = datetime.fromtimestamp(timestamp, timezone.utc)
            message_id = body.get("mid") if isinstance(body, dict) else raw.get("message_id")
            message_id = message_id or raw.get("message_id") or raw.get("id")
            post = {
                "id": "max-%s" % message_id,
                "platform": "max",
                "title": (text or "Новая публикация MAX")[:220],
                "date": published.strftime("%d.%m.%Y, %H:%M"),
                "published_at": published.isoformat(),
                "type": "Публикация",
                "reach": 0,
                "reactions": 0,
                "comments": 0,
                "er": 0,
                "trend": 0,
                "url": "",
            }
            posts = [existing for existing in platform_data.setdefault("recent_posts", []) if existing.get("id") != post["id"]]
            platform_data["recent_posts"] = ([post] + posts)[:100]
            platform_data["posts_count"] = max(platform_data.get("posts_count", 0) or 0, len(platform_data["recent_posts"]))
    archive_posts(runtime, platform)
    write_runtime(folder_id, runtime)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC), **kwargs)

    def log_message(self, fmt, *args):
        sys.stdout.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))

    def send_json(self, payload, status=200, headers=None):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def send_text(self, text, status=200):
        body = str(text).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length > 65536 or length < 0:
            raise ValueError("Слишком большой запрос")
        return json.loads(self.rfile.read(length) or b"{}")

    def session_token(self):
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        return cookie.get("pulse_session").value if cookie.get("pulse_session") else ""

    def current_user(self):
        if not store.remote_enabled():
            cleanup_sessions()
        token = self.session_token()
        session = (store.get_session(token), time.time() + 1) if store.remote_enabled() else SESSIONS.get(token)
        if not session or session[1] <= time.time():
            return None
        user = read_secure_json(USERS_FILE, {}).get(session[0])
        return user if user and not user.get("blocked") else None

    def require_auth(self):
        user = self.current_user()
        if user:
            return user
        self.send_json({"ok": False, "error": "Требуется авторизация"}, 401)
        return None

    def selected_folder(self, user, query, platform=None):
        folder_id = urllib.parse.parse_qs(query).get("folder_id", [""])[0]
        try:
            owned_folder(user, folder_id, platform)
            return folder_id
        except PermissionError as exc:
            self.send_json({"ok": False, "error": str(exc)}, 403)
            return None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/cron/sync":
            secret = os.getenv("CRON_SECRET", "")
            if not secret or not hmac.compare_digest(self.headers.get("Authorization", ""), "Bearer " + secret):
                return self.send_json({"error": "Доступ запрещён"}, 403)
            folders = read_secure_json(FOLDERS_FILE, {})
            users = read_secure_json(USERS_FILE, {})
            synced, failed = 0, 0
            for folder_id, folder in folders.items():
                if folder.get("blocked") or users.get(folder["owner_id"], {}).get("blocked"):
                    continue
                try:
                    run_sync(folder_id)
                    synced += 1
                except Exception as exc:
                    failed += 1
                    print("Ошибка синхронизации папки %s: %s" % (folder_id, exc))
            return self.send_json({"ok": failed == 0, "synced": synced, "failed": failed})
        if parsed.path == "/api/health":
            return self.send_json({"ok": True, "service": "korsakov", "time": datetime.now(timezone.utc).isoformat()})
        if parsed.path == "/api/auth/status":
            user = self.current_user()
            return self.send_json({
                "authenticated": bool(user), "setup_required": False,
                "account": public_user(user) if user else None,
            })
        if not parsed.path.startswith("/api/"):
            return super().do_GET()
        user = self.require_auth()
        if not user:
            return
        if parsed.path == "/api/folders":
            folders = read_secure_json(FOLDERS_FILE, {})
            return self.send_json({"folders": [folder for folder in folders.values() if folder["owner_id"] == user["id"]], "limit": folder_limit(user)})
        if parsed.path == "/api/admin":
            if user.get("role") != "admin":
                return self.send_json({"error": "Доступ запрещён"}, 403)
            folders = read_secure_json(FOLDERS_FILE, {})
            return self.send_json({"users": [{**public_user(item, for_admin=True), "folders": [{**folder, "projects": [{"platform": key, "url": config.get("url", ""), "blocked": key in folder.get("blocked_projects", [])} for key, config in read_secure_json(folder_path(folder["id"], "connections.json"), {}).items() if config.get("url")]} for folder in folders.values() if folder["owner_id"] == item["id"]]} for item in read_secure_json(USERS_FILE, {}).values()]})
        folder_id = self.selected_folder(user, parsed.query)
        if not folder_id:
            return
        if parsed.path == "/api/dashboard":
            query = urllib.parse.parse_qs(parsed.query)
            try:
                period = int(query.get("period", ["30"])[0])
            except ValueError:
                period = 30
            return self.send_json(make_dashboard(folder_id, period))
        if parsed.path == "/api/connections":
            return self.send_json({"connections": connection_status(folder_id)})
        if parsed.path == "/api/history":
            runtime = read_runtime(folder_id)
            blocked = read_secure_json(FOLDERS_FILE, {})[folder_id].get("blocked_projects", [])
            return self.send_json({"snapshots": [row for row in runtime.get("snapshots", []) if row.get("platform") not in blocked]})
        if parsed.path == "/api/history/report":
            query = urllib.parse.parse_qs(parsed.query)
            try:
                year = validate_report_year(query.get("year", [datetime.now(timezone.utc).year])[0])
                return self.send_json(history_report(folder_id, year, query.get("grouping", ["month"])[0]))
            except ValueError as exc:
                return self.send_json({"error": str(exc)}, 400)
        if parsed.path == "/api/cabinet":
            base_url = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
            return self.send_json({
                "account": public_user(user),
                "connections": safe_connections(folder_id),
                "public_base_url": base_url,
                "realtime_available": base_url.startswith("https://"),
            })
        return self.send_json({"error": "not found"}, 404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/auth/register":
            try:
                payload = self.read_json()
                name = str(payload.get("name", "")).strip()
                email = str(payload.get("email", "")).strip().lower()
                password = str(payload.get("password", ""))
                if len(name) < 2 or len(name) > 100 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email) or len(password) < 8:
                    raise ValueError("Укажите имя, корректную почту и пароль от 8 символов")
                salt, digest = password_hash(password)
                with LOCK:
                    users = store.read_json(USERS_FILE)
                    if any(row["email"] == email for row in users.values()):
                        return self.send_json({"ok": False, "error": "Эта почта уже зарегистрирована"}, 409)
                    user_id = secrets.token_hex(12)
                    users[user_id] = {"id": user_id, "name": name, "email": email, "salt": salt, "password_hash": digest, "role": "admin" if not users else "user", "premium": False, "extra_folders": 0, "blocked": False, "created_at": datetime.now(timezone.utc).isoformat()}
                    write_json_unlocked(USERS_FILE, users)
                    folders = store.read_json(FOLDERS_FILE)
                    folder_id = secrets.token_hex(12)
                    folders[folder_id] = {"id": folder_id, "owner_id": user_id, "name": "Моя первая папка", "blocked": False, "blocked_projects": []}
                    write_json_unlocked(FOLDERS_FILE, folders)
                token = create_session(user_id)
                secure = "; Secure" if os.getenv("PUBLIC_BASE_URL", "").startswith("https://") else ""
                return self.send_json({"ok": True}, headers={"Set-Cookie": "pulse_session=%s; Path=/; HttpOnly; SameSite=Strict; Max-Age=86400%s" % (token, secure)})
            except (ValueError, json.JSONDecodeError) as exc:
                return self.send_json({"ok": False, "error": str(exc)}, 400)
        if parsed.path == "/api/auth/login":
            try:
                payload = self.read_json()
                account = next((u for u in read_secure_json(USERS_FILE, {}).values() if u["email"] == str(payload.get("email", "")).strip().lower()), None)
                if not account or not verify_password(str(payload.get("password", "")), account):
                    return self.send_json({"ok": False, "error": "Неверная почта или пароль"}, 401)
                if account.get("blocked"):
                    return self.send_json({"ok": False, "error": "Аккаунт заблокирован"}, 403)
                token = create_session(account["id"])
                secure = "; Secure" if os.getenv("PUBLIC_BASE_URL", "").startswith("https://") else ""
                return self.send_json({"ok": True}, headers={"Set-Cookie": "pulse_session=%s; Path=/; HttpOnly; SameSite=Strict; Max-Age=86400%s" % (token, secure)})
            except (ValueError, json.JSONDecodeError):
                return self.send_json({"ok": False, "error": "Некорректный запрос"}, 400)
        if parsed.path == "/api/auth/logout":
            store.delete_session(self.session_token())
            SESSIONS.pop(self.session_token(), None)
            return self.send_json({"ok": True}, headers={"Set-Cookie": "pulse_session=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0"})

        webhook = re.fullmatch(r"/webhooks/(vk|telegram|max)/([a-f0-9]{24})", parsed.path)
        if webhook:
            platform, folder_id = webhook.groups()
            try:
                event = self.read_json()
                folder = read_secure_json(FOLDERS_FILE, {}).get(folder_id)
                users = read_secure_json(USERS_FILE, {})
                if not folder or folder.get("blocked") or platform in folder.get("blocked_projects", []) or users.get(folder["owner_id"], {}).get("blocked"):
                    return self.send_text("forbidden", 403)
                config = load_connections(folder_id)[platform]
                secret = config.get("webhook_secret", "")
                received = event.get("secret") if platform == "vk" else self.headers.get("X-Telegram-Bot-Api-Secret-Token" if platform == "telegram" else "X-Max-Bot-Api-Secret")
                if not secret or not hmac.compare_digest(str(received or ""), secret):
                    return self.send_text("forbidden", 403)
                if platform == "vk" and event.get("type") == "confirmation":
                    if not config.get("confirmation_code"):
                        return self.send_text("confirmation code is not configured", 409)
                    connections = load_connections(folder_id)
                    connections["vk"]["webhook_active"] = True
                    connections["vk"]["webhook_configured_at"] = datetime.now(timezone.utc).isoformat()
                    write_secure_json(folder_path(folder_id, "connections.json"), connections)
                    return self.send_text(config["confirmation_code"])
                store_webhook_event(folder_id, platform, event)
                return self.send_text("ok")
            except (ValueError, json.JSONDecodeError):
                return self.send_text("bad request", 400)
        user = self.require_auth()
        if not user:
            return
        try:
            payload = self.read_json()
            if parsed.path == "/api/folders/create":
                name = str(payload.get("name", "")).strip()
                if not 1 <= len(name) <= 100:
                    raise ValueError("Название папки должно содержать от 1 до 100 символов")
                with LOCK:
                    folders = store.read_json(FOLDERS_FILE)
                    if sum(f["owner_id"] == user["id"] for f in folders.values()) >= folder_limit(user):
                        raise PermissionError("Достигнут лимит папок. Дополнительную папку можно запросить у администратора")
                    folder_id = secrets.token_hex(12)
                    folders[folder_id] = {"id": folder_id, "owner_id": user["id"], "name": name, "blocked": False, "blocked_projects": []}
                    write_json_unlocked(FOLDERS_FILE, folders)
                return self.send_json({"ok": True, "folder": folders[folder_id]})
            if parsed.path == "/api/folders/rename":
                name = payload.get("name")
                if not isinstance(name, str) or not 1 <= len(name.strip()) <= 100:
                    raise ValueError("Название папки должно содержать от 1 до 100 символов")
                folder_id = payload.get("folder_id")
                with LOCK:
                    folders = store.read_json(FOLDERS_FILE)
                    folder = folders.get(folder_id) if isinstance(folder_id, str) else None
                    if not folder or folder["owner_id"] != user["id"]:
                        raise PermissionError("Папка не найдена")
                    if folder.get("blocked"):
                        raise PermissionError("Папка заблокирована администратором")
                    folder["name"] = name.strip()
                    write_json_unlocked(FOLDERS_FILE, folders)
                return self.send_json({"ok": True, "folder": folder})
            if parsed.path == "/api/admin/update":
                if user.get("role") != "admin":
                    raise PermissionError("Доступ запрещён")
                field = payload.get("field")
                target_id = payload.get("user_id")
                with LOCK:
                    users = store.read_json(USERS_FILE)
                    folders = store.read_json(FOLDERS_FILE)
                    if target_id not in users:
                        raise ValueError("Пользователь не найден")
                    if field in ("premium", "blocked"):
                        if type(payload.get("value")) is not bool:
                            raise ValueError("Ожидается true или false")
                        if field == "blocked" and target_id == user["id"] and payload["value"]:
                            raise PermissionError("Нельзя заблокировать себя")
                        users[target_id][field] = payload["value"]
                        write_json_unlocked(USERS_FILE, users)
                    elif field == "extra_folders":
                        value = payload.get("value")
                        if type(value) is not int or not 0 <= value <= 100:
                            raise ValueError("Дополнительных папок может быть от 0 до 100")
                        users[target_id][field] = value
                        write_json_unlocked(USERS_FILE, users)
                    elif field in ("folder_blocked", "project_blocked"):
                        folder = folders.get(payload.get("folder_id"))
                        if not folder or folder["owner_id"] != target_id or type(payload.get("value")) is not bool:
                            raise ValueError("Некорректная папка или значение")
                        if field == "folder_blocked":
                            folder["blocked"] = payload["value"]
                        else:
                            platform = payload.get("platform")
                            configs = store.read_json(folder_path(folder["id"], "connections.json")) if store.exists(folder_path(folder["id"], "connections.json")) else {}
                            if platform not in PLATFORMS or not configs.get(platform, {}).get("url"):
                                raise ValueError("Проект не найден")
                            blocked = set(folder.get("blocked_projects", []))
                            (blocked.add if payload["value"] else blocked.discard)(platform)
                            folder["blocked_projects"] = sorted(blocked)
                        write_json_unlocked(FOLDERS_FILE, folders)
                    else:
                        raise ValueError("Неизвестное действие")
                return self.send_json({"ok": True})
            platform = payload.get("platform")
            folder_id = str(payload.get("folder_id", ""))
            owned_folder(user, folder_id, platform if parsed.path.startswith("/api/connections/") else None)
            if parsed.path == "/api/sync":
                return self.send_json(run_sync(folder_id))
            if parsed.path == "/api/history/backfill":
                owned_folder(user, folder_id, "vk")
                return self.send_json(fetch_vk_history(folder_id, validate_report_year(payload.get("year"))))
            if parsed.path == "/api/connections/save":
                save_connection(folder_id, platform, payload)
                result = run_sync(folder_id)
                return self.send_json({"ok": True, "connections": result["connections"], "cabinet": safe_connections(folder_id)})
            if parsed.path == "/api/connections/webhook":
                return self.send_json(configure_webhook(folder_id, platform))
        except PermissionError as exc:
            return self.send_json({"ok": False, "error": str(exc)}, 403)
        except (ValueError, RuntimeError, json.JSONDecodeError, TypeError) as exc:
            return self.send_json({"ok": False, "error": str(exc)}, 400)
        return self.send_json({"ok": False, "error": "not found"}, 404)


if __name__ == "__main__":
    load_dotenv()
    migrate_legacy()
    ensure_first_folders()
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "127.0.0.1")
    server = ThreadingHTTPServer((host, port), Handler)
    stop_sync = threading.Event()
    sync_thread = threading.Thread(target=sync_scheduler, args=(stop_sync,), name="pulse-sync", daemon=True)
    sync_thread.start()
    print("KORSAKOV запущен: http://localhost:%d" % port)
    print("Остановить: Ctrl+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервис остановлен")
    finally:
        stop_sync.set()
        server.server_close()
