#!/bin/sh
# Rebuild the Cheeko Video Library page and publish it to GitHub Pages
# (repo Craftech360-projects/cheeko-video-library, https://craftech360-projects.github.io/cheeko-video-library/).
set -e
T="$(cd "$(dirname "$0")" && pwd)"; S="$T/../library-site"
"$T/../../cheeko-v2-website/.venv/bin/python" "$T/library_page.py" "$S/index.html" --site
cd "$S"
if git diff --quiet && git diff --cached --quiet; then echo "no changes"; exit 0; fi
git add -A && git commit -q -m "Update the video library ($(date +%Y-%m-%d))

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git push -q && echo "pushed; live in a minute or two"
