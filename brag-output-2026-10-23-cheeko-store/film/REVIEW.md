# V55 Cheeko Store launch: review notes (v1, 2026-10-23)

## Creative calls
- Storyline A "Done. Done. Done." (Ravi's pick). Not built: B "Rewind" (one continuous pull-back from inside the quiz) and C "Seven new tricks" (music-led kinetic type). Both are in STORYLINES.md.
- The store is the REAL page (cheeko-app-store-web, branch fix/store-on-manager-api) running its own code against a stand-in backend with the live store's data (work/store_capture.mjs). Nothing in the store UI is redrawn.
- The film opens the store on its Videos page, not Home: Home shows the game tiles and game-led Featured Drops, and Ravi said no games. Older videos are only seen blurred while the list scrolls.
- Cheeko's download screen is the firmware's own content-download UI (SetDownloadProgress), rendered by fwsim with the title "Guess the Dinosaur Level 1" (new `--download` option in marketing/tools/fwsim/harness/main.cc). The stock render said "Getting Dadi's story ready", which would have been wrong here.
- Voices: MiniMax English_Upbeat_Woman (narrator, 1.05x), English_PlayfulGirl (Cheeko), English_Strong-WilledBoy for the boy's "T-Rex!" (median pitch 324 Hz, reads as a small boy). Every line checked with Sarvam speech-to-text.
- Music and effects: our synth.py (no drums until the store appears, no drums under the quiz's own sound), real card-insert sound when the card lands in Cheeko.

## Measured
- `hyperframes check`: no errors. Warnings kept on purpose: the finger parks off-screen between taps (#s2-finger), nested media timing is local to each scene (intended), the two fox images in S3's bubbles share a source.
- Audio: -13.5 LUFS integrated, -1.4 dBTP. Measured, not heard by me.
- Review sheets: every beat frame, every cut strip, phone width.

## Weakest shots
- The scroll (7.9 to 9.4 s) passes older videos; they are blurred, but a paused frame could show a title.
- The duo shot (15.85 to 18.4 s): the small phone's text is too small to read; it works as "the phone sent it", not as a read.
- Stickers are about 450 px source art shown at 560 to 620 px: slightly soft.

## Next
- Ravi's notes on v1, then the 16:9 version (about 60 s) with more of the store (Featured Drops, a video preview, two toys, Update, Downloaded on Cheeko).
