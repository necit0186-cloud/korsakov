"""Package the full KORSAKOV UI and Python API for Vercel."""

import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
target = root / "vercel-full"
(target / "api").mkdir(parents=True, exist_ok=True)
(target / "public").mkdir(parents=True, exist_ok=True)

for name in ("server.py", "persistent_store.py"):
    shutil.copyfile(root / name, target / name)
for asset in ("index.html", "styles.css", "app.js", "favicon.svg", "korsakov-mark.svg"):
    shutil.copyfile(root / "app" / asset, target / "public" / asset)

(target / "api" / "index.py").write_text(
    "import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent.parent))\n"
    "from server import Handler\n\nclass handler(Handler):\n    pass\n", encoding="utf-8"
)
(target / "vercel.json").write_text(json.dumps({
    "version": 2,
    "rewrites": [
        {"source": "/api/:path*", "destination": "/api/index"},
        {"source": "/webhooks/:path*", "destination": "/api/index"},
    ],
    "regions": ["fra1"],
    "functions": {"api/index.py": {"includeFiles": "{server.py,persistent_store.py}", "maxDuration": 300}},
    "crons": [{"path": "/api/cron/sync", "schedule": "0 4 * * *"}],
}, indent=2) + "\n", encoding="utf-8")
print("Built", target)
