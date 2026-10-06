# V08 Tiny CEO

Original sarcastic Cheeko Reel, 1080x1920 at 30 fps, 33.79 seconds. Audience: parents. Fictional premise: a five-year-old inherits an adult feed and becomes a tiny executive with a three-crayon portfolio.

## Research and writing
See `brag-plan.md` for source links and the shot list, and `script.md` for the clean script. The Moonshot research informed broad techniques: product-based absurdity, deadpan seriousness, escalating jokes and a callback. This is an original concept, with no copied campaign dialogue, footage or celebrity imitation. The adult phone feed is a generic fictional interface, not an actual app or a claim about a specific platform. No medical, financial or developmental promises are made.

## Art and product
`work/assets/tiny-ceo-sprites.png` was generated with the built-in image tool against Ravi's family illustration reference. The four poses are shown through CSS cropping; the original transparent sheet remains intact. All Cheeko product shots use the real `device_current.png` and its current firmware display, not a generated device. Three card visuals are shipping cards: Tales of Kindness, Dreamy Melodies and Sounds Around Me. This is 2D motion-graphics editing with illustrated characters, not articulated character animation or live-action footage.

## Voice and music
MiniMax speech-2.8-hd, English_Upbeat_Woman. Seventeen individual takes with per-line emotions, verified with Sarvam transcription. The product reveal was re-recorded with a pause to separate Meet and Cheeko. Sarvam spells the brand as Chico. No credentials were copied off the recording server. `voice-lines.json` controls the narration; `warp.json` maps storyboard to actual voice timing. Captions are take-aligned with estimated word emphasis, not forced-aligned word timestamps.

Original 120 BPM D-major comedy score synthesized with NumPy: pizzicato chords, light bass, desk bells, a short silence on Brilliant and a falling sting for the portfolio callback. No licensed or commercial music borrowed.

## Rebuild
Run in `work/`:

```sh
../../.venv/bin/python synth.py
node qa.mjs
node render.mjs /opt/homebrew/bin/ffmpeg 33.79
bash finish.sh /opt/homebrew/bin/ffmpeg 33.79 0.8
```

The skill's finishing script replaces frame zero with the settled hook poster. `qa.mjs` also creates the separate Reel cover. `synth.py` regenerates `timeline.js`, full audio and music-only audio. Assets are beside the source in `work/assets/`.

## Checks
34 scene and transition frames inspected. No browser exceptions or text overflow found. Final-file verification passed: H.264 1080x1920 30 fps, AAC 44.1 kHz, 33.79 seconds, 7,100,190 bytes. Full-file decoding passed. Measured final audio: -14.17 LUFS, -1.37 dBTP, 2.40 LU loudness range.
