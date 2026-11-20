#!/usr/bin/env bash
# The one final file for Cheeko: <slug>/device/<name>_296x240.mp4 (H.264 Baseline, 30 fps, AAC-LC 48 kHz mono, -16 LUFS).
# Usage: bash finish.sh <slug> <level> <name>
set -euo pipefail
cd "$(dirname "$0")"; SLUG=$1; LV=$2; NAME=$3; mkdir -p "$SLUG/device"
ffmpeg -y -loglevel error -i "$SLUG/raw2x_L$LV.mp4" -vf "scale=296:240:flags=lanczos,format=yuv420p" -r 30 \
  -c:v libx264 -profile:v baseline -level 3.0 -bf 0 -g 60 -crf 18 -preset slow \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000" -ac 1 -c:a aac -b:a 96k -movflags +faststart "$SLUG/device/${NAME}_296x240.mp4"
echo "$SLUG/device/${NAME}_296x240.mp4"
