#!/usr/bin/env bash
# Cheeko Video Kit setup. Run once after unzipping (and again if you move the folder):
#   bash setup.sh              paths + Playwright/Chromium + Python venv
#   bash setup.sh --with-site  also pull the website's own photos and pages from the public GitHub repo
set -euo pipefail
KIT="$(cd "$(dirname "$0")" && pwd)"
WS="$KIT/workspace"
SITE="$WS/cheeko-v2-website"

echo "1/4  Pointing every script and doc at $WS"
python3 - "$KIT" "$WS" <<'PY'
import sys, pathlib
kit, new = pathlib.Path(sys.argv[1]), sys.argv[2]
marker = kit / ".kit-root"
olds = ["/Users/ravikumar/" + "Cheeko Master"] + ([marker.read_text().strip()] if marker.exists() else [])
me = kit / "setup.sh"   # never edit this script while bash is running it
n = 0
for p in kit.rglob("*"):
    if p.is_file() and p != me and p.suffix in {".py", ".mjs", ".js", ".sh", ".md", ".html", ".json", ".txt"} and "node_modules" not in p.parts:
        try: s = p.read_text()
        except Exception: continue
        t = s
        for o in olds:
            if o != new: t = t.replace(o, new)
        if t != s: p.write_text(t); n += 1
marker.write_text(new)
print(f"     updated {n} files")
PY

if [[ "${1:-}" == "--with-site" ]]; then
  echo "2/4  Pulling the website (public repo Craftech360-projects/cheeko-v2-website)"
  TMP="$(mktemp -d)"
  git clone --depth 1 -q https://github.com/Craftech360-projects/cheeko-v2-website "$TMP/site"
  rsync -a --ignore-existing --exclude .git "$TMP/site/" "$SITE/"
  rm -rf "$TMP"
else
  echo "2/4  Skipping the website pull (run with --with-site for the kids photos in assets/img/live)"
fi

echo "3/4  Node: Playwright + Chromium"
command -v node >/dev/null || { echo "Install Node 22+ first"; exit 1; }
( cd "$SITE" && npm i --no-save --no-package-lock --silent playwright@1.58 && npx --yes playwright install chromium )

echo "4/4  Python venv (numpy, Pillow, requests, websocket-client)"
python3 -m venv "$SITE/.venv"
"$SITE/.venv/bin/pip" install -q numpy pillow requests websocket-client

command -v ffmpeg >/dev/null && echo "ffmpeg: $(command -v ffmpeg)" || echo "NOTE: install ffmpeg (brew install ffmpeg / apt install ffmpeg)"
echo "Done. Next: bash selftest.sh   (renders 2 seconds of a real video to prove it works)"
