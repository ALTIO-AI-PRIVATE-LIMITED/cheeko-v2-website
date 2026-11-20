#!/usr/bin/env bash
# From raw2x.mp4 (592x480, rendered at 2x) make the files for Cheeko and for review.
#   ../device/<name>_296x240.mp4    H.264 Baseline (no B-frames), 296x240, 30 fps, AAC-LC 48 kHz mono, -16 LUFS: plays on Cheeko
#   ../device/<name>_296x240.avi    MJPEG 296x240 + PCM audio, same timing (for MJPEG-only players)
#   ../preview_on_device.mp4        the video playing inside the yellow Cheeko, for review on a computer
# Usage (inside work/): bash finish_device.sh <name>
set -euo pipefail
NAME=$1; mkdir -p ../device
IMG="/Users/ravikumar/Cheeko Master/cheeko-v2-website/assets/img/device-v2"
AUD="loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000"
ffmpeg -y -loglevel error -i raw2x.mp4 -vf "scale=296:240:flags=lanczos,format=yuv420p" -r 30 \
  -c:v libx264 -profile:v baseline -level 3.0 -bf 0 -g 60 -crf 18 -preset slow \
  -af "$AUD" -ac 1 -c:a aac -b:a 96k -movflags +faststart "../device/${NAME}_296x240.mp4"
ffmpeg -y -loglevel error -i raw2x.mp4 -vf "scale=296:240:flags=lanczos" -r 30 -c:v mjpeg -q:v 4 \
  -af "$AUD" -ac 1 -c:a pcm_s16le "../device/${NAME}_296x240.avi"
# review preview: the 296x240 file scaled back up into the device's glass (preview_device.png, preview_mask.png, preview_geom.txt
# are the yellow front render and glass mask pre-scaled to 900 px wide)
read SX SY SW SH < preview_geom.txt
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "../device/${NAME}_296x240.mp4")
ffmpeg -y -loglevel error -i "../device/${NAME}_296x240.mp4" -loop 1 -i preview_device.png -loop 1 -i preview_mask.png -filter_complex \
  "[2:v]format=gray[m];[0:v]scale=${SW}:${SH}:flags=lanczos,format=rgba[v];[v][m]alphamerge[vm];[1:v]format=rgba[dev];[dev][vm]overlay=${SX}:${SY}:shortest=1,format=yuv420p[o]" \
  -map "[o]" -map 0:a -t "$DUR" -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 160k -movflags +faststart ../preview_on_device.mp4
ls -la ../device ../preview_on_device.mp4
