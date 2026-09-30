#!/bin/sh
# Prepare a feature Reel's work/ folder: template + mask + scripts. Usage: setup.sh <video dir name>   (spec.js is written by hand)
set -e
T="$(cd "$(dirname "$0")" && pwd)"; R="/Users/ravikumar/Cheeko Master/cheeko-v2-website"; W="$R/$1/work"; mkdir -p "$W"
# New design (Sep 2026): the screen mask and the outline come from the new renders (marketing/tools/device_v2_mask.py)
MASK=$(python3 -c "import base64;print('data:image/png;base64,'+base64.b64encode(open('$R/assets/img/device-v2/screen_mask.png','rb').read()).decode())")
SIL=$(python3 -c "import base64;print('data:image/png;base64,'+base64.b64encode(open('$R/assets/img/device-v2/silhouette.png','rb').read()).decode())")
python3 -c "import sys;s=open('$T/feature.html').read().replace('MASKURI','$MASK').replace('SILURI','$SIL');open('$W/compose.html','w').write(s)"
cp "$T/synth.py" "$T/cues.mjs" "$W/"; cp "$R/brag-output-2026-09-28-reel/work/"{pw.mjs,render.mjs,stills.mjs,finish.sh,sheet.py} "$W/"
echo "ready: $W"
