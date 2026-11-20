#!/usr/bin/env bash
# Pull the poster frame, bake it in as frame 0, mux loudness-normalised audio.
# Usage (inside work/): bash finish.sh <ffmpeg> <seconds> <poster-time>
set -euo pipefail
FF=$1; DUR=$2; POSTER=$3
"$FF" -y -loglevel error -ss "$POSTER" -i raw.mp4 -frames:v 1 -q:v 2 ../brag.jpg
"$FF" -y -loglevel error -i raw.mp4 -loop 1 -i ../brag.jpg -i music-final.wav \
  -filter_complex "[1:v]format=yuv420p[p];[0:v][p]overlay=0:0:enable='eq(n,0)':shortest=1[v];[2:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 44100 \
  -t "$DUR" -movflags +faststart ../brag.mp4
rm -f raw.mp4
echo "wrote ../brag.mp4 and ../brag.jpg"
