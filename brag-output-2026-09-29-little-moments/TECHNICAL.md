# V07 Little Moments, More Connection

27-second vertical motion-graphics reel, 1080x1920, 30 fps. Built using the local Cheeko video skill and its Playwright/FFmpeg pipeline.

## Creative sources
- User-approved family situation sheet, copied intact to `work/assets/family-situations.png`. Scenes are displayed through CSS cropping, not redrawn.
- User's hardware reference, preserved in `work/assets/product-reference.jpeg`.
- Real current yellow device from the website's `assets/img/device_current.png`, included for the two hardware close-ups.
- The illustrated family scenes are stylized; their small product details are not exact firmware demonstrations.
- This is animated illustration editing, not generated live-action footage or articulated character animation.

## Audio and timing
- MiniMax speech-2.8-hd, English_Upbeat_Woman, one emotion-tagged take per line.
- 14 takes transcribed with Sarvam. All wording matched; the recognizer spells Cheeko as Chico.
- Script: `work/voice-lines.json`. Takes: `work/vo/clips/`. Final voice: `work/vo/vo-tight.wav`.
- `work/warp.json` maps storyboard timing to the recorded voice. Captions are anchored to each take, with estimated within-line word timings weighted by word length. They are not forced-aligned word timestamps.
- Original synthesized D-major, 120 BPM mallet-pop music, soft matching effects and voice ducking. No licensed stock music used.
- Final mix normalized toward -14 LUFS, true peak limited to -1.5 dBTP.

## Rebuild
Run inside this video's `work` directory, with Node/Playwright, FFmpeg and the website `.venv` available:

```sh
../../.venv/bin/python synth.py
node qa.mjs
node render.mjs /opt/homebrew/bin/ffmpeg 26.82
bash finish.sh /opt/homebrew/bin/ffmpeg 26.82 0.7
```

The composition expects the `assets/` directory next to it. `synth.py` generates `timeline.js` from the voice script and warp. `qa.mjs` captures each scene and early transition and makes `thumbnail.jpg`. The original full-resolution inputs are included for review. No website code was changed.

## Checks
36 scene/transition frames inspected; no browser errors or caption/title overflow. Voice transcription reviewed. Final MP4 verified: H.264, 1080x1920, 30 fps, 26.82 seconds, AAC stereo 44.1 kHz, 8,229,234 bytes. Full-file decoding passed. Measured loudness -13.96 LUFS, true peak -1.50 dBTP. The poster is baked into frame zero by the existing skill finishing script.
