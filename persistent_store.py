"""Local JSON files or a durable Upstash Redis store, using only stdlib."""

import hashlib
import json
import os
import secrets
import threading
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path


def _credentials():
    url = os.getenv("KV_REST_API_URL") or os.getenv("UPSTASH_REDIS_REST_URL")
    token = os.getenv("KV_REST_API_TOKEN") or os.getenv("UPSTASH_REDIS_REST_TOKEN")
    if bool(url) != bool(token):
        raise RuntimeError("Укажите URL и токен постоянного хранилища вместе")
    if not url and os.getenv("VERCEL"):
        raise RuntimeError("Постоянное хранилище не подключено")
    return url, token


def remote_enabled():
    return bool(_credentials()[0])


def redis(*command):
    url, token = _credentials()
    if not url:
        raise RuntimeError("Постоянное хранилище не подключено")
    if not url.startswith("https://"):
        raise RuntimeError("Хранилище должно использовать HTTPS")
    request = urllib.request.Request(
        url.rstrip("/"),
        data=json.dumps(command, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        result = json.load(response)
    if "error" in result:
        raise RuntimeError("Ошибка постоянного хранилища: " + result["error"])
    return result["result"]


def file_key(path):
    relative = Path(path).resolve().relative_to(Path(__file__).resolve().parent / "data")
    return "korsakov:file:" + relative.as_posix()


def read_json(path):
    if remote_enabled():
        value = redis("GET", file_key(path))
        if value is None:
            raise FileNotFoundError(str(path))
        return json.loads(value)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def exists(path):
    return redis("EXISTS", file_key(path)) == 1 if remote_enabled() else Path(path).exists()


def write_json(path, data, only_if_missing=False):
    if remote_enabled():
        command = ["SET", file_key(path), json.dumps(data, ensure_ascii=False)]
        if only_if_missing:
            command.append("NX")
        return redis(*command) == "OK"
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + "." + secrets.token_hex(6) + ".tmp")
    try:
        temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.chmod(temp, 0o600)
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)
    return True


def _session_key(token):
    return "korsakov:session:" + hashlib.sha256(token.encode("utf-8")).hexdigest()


def save_session(token, user_id):
    if remote_enabled():
        redis("SET", _session_key(token), user_id, "EX", 86400)


def get_session(token):
    return redis("GET", _session_key(token)) if token and remote_enabled() else None


def delete_session(token):
    if token and remote_enabled():
        redis("DEL", _session_key(token))


class StoreLock:
    """Serialize read-modify-write operations across serverless instances."""

    def __init__(self, name, lease_seconds=180):
        self.name = "korsakov:lock:" + name
        self.lease_seconds = lease_seconds
        self.local = threading.Lock()
        self._current = threading.local()

    def __enter__(self):
        self._current.context = self.__call__()
        self._current.context.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            return self._current.context.__exit__(exc_type, exc, tb)
        finally:
            del self._current.context

    @contextmanager
    def __call__(self):
        with self.local:
            if not remote_enabled():
                yield
                return
            owner = secrets.token_hex(16)
            deadline = time.monotonic() + 20
            while redis("SET", self.name, owner, "NX", "EX", self.lease_seconds) != "OK":
                if time.monotonic() >= deadline:
                    raise RuntimeError("Хранилище занято; повторите запрос")
                time.sleep(0.1)
            try:
                yield
            finally:
                redis("EVAL", "if redis.call('GET', KEYS[1]) == ARGV[1] then return redis.call('DEL', KEYS[1]) else return 0 end", 1, self.name, owner)
