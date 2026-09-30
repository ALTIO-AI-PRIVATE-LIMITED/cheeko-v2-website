#!/usr/bin/env bash
# Renders a 2-second test video with the real pipeline (render.mjs + finish.sh), using only files in this kit.
set -euo pipefail
KIT="$(cd "$(dirname "$0")" && pwd)"
SITE="$KIT/workspace/cheeko-v2-website"
D="$SITE/brag-output-selftest"; W="$D/work"
FF="$(command -v ffmpeg)" || { echo "Install ffmpeg first"; exit 1; }
mkdir -p "$W"
cp "$KIT/selftest/compose.html" "$W/"
cp "$KIT/skills/cheeko-video/scripts/"{pw.mjs,render.mjs,stills.mjs,finish.sh} "$W/" 2>/dev/null || \
cp "$SITE/.claude/skills/cheeko-video/scripts/"{pw.mjs,render.mjs,stills.mjs,finish.sh} "$W/"
cd "$W"
"$FF" -y -loglevel error -f lavfi -i anullsrc=r=48000:cl=stereo -t 2 music-final.wav
node render.mjs "$FF" 2
mv raw.mp4 "$D/selftest.mp4"
node stills.mjs 1.8 >/dev/null 2>&1 || true
echo "OK: $D/selftest.mp4 ($(du -h "$D/selftest.mp4" | cut -f1))"
