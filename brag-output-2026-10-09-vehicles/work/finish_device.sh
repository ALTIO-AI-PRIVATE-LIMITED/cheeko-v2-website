#!/usr/bin/env bash
# From raw2x_L<level>.mp4 (592x480, rendered at 2x) make the one final file for Cheeko (Ravi 2026-10-09: the final video is enough,
# no AVI copy, no in-device preview):
#   ../device/<name>_296x240.mp4   H.264 Baseline (no B-frames), 296x240, 30 fps, AAC-LC 48 kHz mono, -16 LUFS
# Usage (inside work/): bash finish_device.sh <name> <level>
set -euo pipefail
NAME=$1; LV=$2; mkdir -p ../device
ffmpeg -y -loglevel error -i raw2x_L${LV}.mp4 -vf "scale=296:240:flags=lanczos,format=yuv420p" -r 30 \
  -c:v libx264 -profile:v baseline -level 3.0 -bf 0 -g 60 -crf 18 -preset slow \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000" -ac 1 -c:a aac -b:a 96k -movflags +faststart "../device/${NAME}_296x240.mp4"
ls -la "../device/${NAME}_296x240.mp4"
