"""One-time, non-destructive import of existing accounts and archives."""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import persistent_store as store  # noqa: E402


def load_environment(path):
    if not path:
        return
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip().strip('"').strip("'")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", help="Vercel environment file (keep outside Git)")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    args = parser.parse_args()
    load_environment(args.env_file)
    if not store.remote_enabled():
        parser.error("Укажите KV_REST_API_URL и KV_REST_API_TOKEN")
    files = [args.data_dir / "users.json", args.data_dir / "folders.json"]
    files += sorted((args.data_dir / "folders").glob("*/*.json"))
    if not all(path.is_file() for path in files[:2]):
        parser.error("Не найдены users.json и folders.json")
    if store.redis("EXISTS", "korsakov:migration:complete"):
        parser.error("Импорт уже завершён; существующие данные не перезаписываются")
    payloads = [(path, path.read_bytes()) for path in files]
    for path, content in payloads:
        json.loads(content)
        existing = store.redis("GET", store.file_key(path))
        if existing is not None and json.loads(existing) != json.loads(content):
            parser.error("В хранилище уже есть отличающиеся данные: " + str(path.relative_to(args.data_dir)))
    for path, content in payloads:
        store.redis("SET", store.file_key(path), content.decode("utf-8"), "NX")
    if any(path.read_bytes() != content for path, content in payloads):
        parser.error("Локальные данные изменились во время импорта; остановите локальный сервер и повторите")
    for path, content in payloads:
        remote = store.redis("GET", store.file_key(path))
        if remote is None or json.loads(remote) != json.loads(content):
            parser.error("Проверка импорта не прошла: " + str(path.relative_to(args.data_dir)))
    digest = hashlib.sha256(b"".join(content for _, content in payloads)).hexdigest()
    store.redis("SET", "korsakov:migration:complete", digest, "NX")
    print("Импортировано и проверено файлов:", len(files))
    print("Контрольная сумма:", digest)


if __name__ == "__main__":
    main()
