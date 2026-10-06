# How we make Cheeko videos (reference for the next AI or person)

Written 2026-09-28 after making V01 to V05 (English) and V03-HI to V05-HI (Hindi). Read this first, then `Production rules.md` (style, facts, never-do list). Every video folder in Drive also has its own `TECHNICAL.md` with the exact files and commands for that video.

## Where things live

| What | Where |
|---|---|
| Video source (one folder per video) | `/Users/ravikumar/Cheeko Master/cheeko-v2-website/brag-output*/` (git repo `Craftech360-projects/cheeko-v2-website`, PR 9 branch `claude/website-launch-video-3xp8rq`). `work/` holds the source, the folder root holds `brag.mp4`, `brag.jpg`, `thumbnail.jpg`, `share-copy.txt`, `brag-plan.md`. Hindi copies end in `-hi`. |
| Shared tools | `/Users/ravikumar/Cheeko Master/marketing/tools/` (copied to Drive `00 Plan/Pipeline code`) |
| Video skill (method and brand) | `cheeko-v2-website/.claude/skills/cheeko-video/SKILL.md` and `.claude/skills/brag-slim/SKILL.md` |
| Assets | `cheeko-v2-website/assets/img/` (website), `assets/img/cards-shipping/` (the 10 real cards), `assets/img/fw-screens/` (real device screens), `assets/img/device_current.png` (device with the current home screen), `assets/img/device_live_screen_mask.png` |
| Drive (the team's copy) | "cheeko ai videos" = `~/Library/CloudStorage/GoogleDrive-ravi.ramp36@gmail.com/My Drive/cheeko ai videos`, synced by Google Drive for desktop. `Ready to post/English` and `Ready to post/Hindi` have one folder per video with just its video, thumbnail and caption. |
| Voices | Dev box `root@64.227.170.31`, lab `/root/tts-compare` (`tts_test.py` has `tts()` for MiniMax and `qwen_tts()`). API keys are read from the running `ui.py` process environment on the box and never leave it. Sarvam speech-to-text on the same box checks every take. |

Needs on the Mac: Node 22, Playwright 1.58 (in the repo's `node_modules`), ffmpeg, the Python venv `cheeko-v2-website/.venv` (numpy, Pillow). Path gotcha: builds break on the space in "Cheeko Master" for the firmware renderer only; the video pipeline is fine.

## The pipeline, step by step

1. **Script.** Write the lines in `marketing/tools/vo_lines.json` (English) and `vo_lines_hi.json` (Hindi). Each line: emotion, text, `old` start time (where the line sits in the composition's own timeline), `gap` (silence before it). Split a line wherever something on screen must land on a word ("No videos." / "No reels." / "No ads." are three lines). No em dashes, no ellipsis character, no curly quotes, no emojis in voice text.
2. **Voice.** Record one clip per line on the dev box with MiniMax `speech-2.8-hd`: English voice `English_Upbeat_Woman`, Hindi voice `hindi_male_1_v2` (`language_boost` Hindi), a different `emotion` per line (happy, surprised, calm, fluent...). Write Cheeko as चीको in Hindi. Avoid hyphens inside Hindi phrases (माता-पिता made a half-second pause). Check every clip with Sarvam `saarika:v2.5` speech-to-text. Never join audio on the dev box (an ffmpeg `apad` without a duration once wrote 2.5 GB); copy clips to the Mac.
3. **Assemble the voice.** `python build_vo.py <clips dir> [vo_lines_hi.json -hi]` trims each clip, adds the gaps, writes `work/vo/vo-tight.wav` and `work/warp.json` (anchor pairs: new voice time and old composition time).
4. **Composition.** `work/compose.html` is one HTML page where `window.render(t)` draws the frame at time `t` and `window.ready` resolves after fonts and images load. A `<script id="warp">` block at the end maps real time to the composition's own timeline using `warp.json`, so scenes follow the voice without re-timing by hand. Put anything on the device screen in a `.scr` element clipped by the screen mask (inlined as a data URI, because Chromium blocks CSS masks from `file://`). Word captions live in `const CAPS` (`[start, end, [[word, time, highlight?], ...]]`); emojis are extra tokens with class `emo`.
5. **Hindi version.** Copy the English folder to `<dir>-hi`, then run `build_vo.py <clips> vo_lines_hi.json -hi` and `make_hindi.py`: Devanagari font fallback, Hindi captions from the Hindi lines, translated stamps and outro, Hindi warp.
6. **Clean text and emojis.** `captions_clean.py` removes dashes, ellipses and curly quotes and adds emojis after key words (map `EMOJI`, never on a line's first word).
7. **Music.** `work/synth.py` synthesises original music and sound effects with numpy in D major, places them through the warp (the groove keeps a steady tempo), ducks the music under the voice and writes `music-final.wav`. Real device sounds are in Drive `01 Shared assets/Sounds` if needed.
8. **Check.** `node stills.mjs <times>` then `python sheet.py <cols>`; look at every scene and every transition (mid-wipe frames catch black gaps and double exposures). Close-up any device screen.
9. **Render.** `node render.mjs ffmpeg <seconds>` (about 1 minute per 25 s), then `bash finish.sh ffmpeg <seconds> <poster time>` (bakes the poster as frame 0, loudness -14 LUFS).
10. **Thumbnail.** `cheeko-v2-website/thumbs-work/make_thumbs.mjs` renders `thumb.html` with a spec per video (hook text, colour, layout) to `<dir>/thumbnail.jpg`, 1080x1920, key content inside the centre 3:4 area.
11. **Publish.** `python publish_to_drive.py` rebuilds every video folder in Drive (1 Script, 2 Voice, 3 Test, 4 Final, 5 Source, TECHNICAL.md), the tracker, and `Ready to post`. Add a new video to its `VIDEOS` list first.


## Feature Reels template (V11-V18, 2026-09-29)

A faster path for one-feature videos, with character voices, used for V11 to V18 and their Hindi versions:

1. Lines in `tools/feature_lines.json` (English) or `feature_lines_hi.json` (Hindi): `[speaker, emotion, text, gap, options]`. Speakers and voices are listed at the top of each file: narrator N, cheeko, nani, mitthu, quizzy, kid, grandma. Options: `emoji` (word -> emoji for captions and bubbles), `hl` (highlighted words), `show` (text on screen if different from the spoken text). `fx:<effect>` lines replay another line through a Funny Voice effect.
2. Record on the dev box (MiniMax `tts()` or Qwen `qwen_tts()` with an inline `[emotion]` tag), check every clip with Sarvam speech-to-text, copy to the Mac.
3. `python build_feature.py <clips> [VIDS] [--lines feature_lines_hi.json --suffix=-hi]` writes `vo/vo-tight.wav`, `timing.json` and `timing.js` for each video (the Qwen voices are sped up 8-15% there).
4. `tools/feature/setup.sh <video dir>` copies the template (`feature/feature.html` -> `compose.html`, with the screen mask inlined) and the scripts. The only file you write is `work/spec.js`: a list of shots (`photo`, `device` with firmware screens over time, `app`, `glyphs`, `stamps`, `letters`, `grid`, `title`, `outro`), each starting at a voice line (`L(i)` start, `E(i)` end). Narrator lines become word captions, other speakers become speech bubbles automatically.
5. Hindi: `python feature/make_hindi_feature.py <slug>` reuses the English shot list with Hindi text and the `*_hi_*` Imagine screens.
6. `node cues.mjs` (cues for the music) -> `python synth.py` (music, real device sounds for card insert and knob) -> `node render.mjs ffmpeg <dur>` -> `bash finish.sh ffmpeg <dur> <poster>`.
7. Thumbnails: `cheeko-v2-website/thumbs-work/make_thumbs_feature.mjs` (device images with the right screen in `thumbs-work/dev/`).

## Real device screens

The device UI is drawn by the firmware (`Craftech360-projects/cheeko-os-v2`). `marketing/tools/fwsim` compiles the firmware's own LVGL UI code on the Mac and saves every screen as PNG (copy it to a path without spaces, then `./render.sh <commit>`). 180 screens from commit b05c95d (FW 2.4.311) are in `assets/img/fw-screens/` and Drive `01 Shared assets/Device screens/Current firmware screens`. Custom Imagine screens with our prompts and drawings are the `imagine_tiger_*` and `imagine_rickshaw_*` files. The firmware cannot show Devanagari (no glyphs in any built-in font), so Hindi text on the device shows as blank; the `*_hi_*` renders show exactly that.

Do not use: `device_live.png` (old dark UI), `live/card-*.jpg` and `card_habits.jpg` (old website cards), anything in `Old UI (DO NOT USE)`, the Imagine demo video (it shows Spider-Man).

## Things that went wrong once (so they don't again)

- A single-emotion voice take sounded flat. Record per line.
- Qwen-Audio's multilingual voice garbled Hindi. Use MiniMax Hindi voices.
- A plain rounded rectangle over the device screen poked out at the corners. Always use the mask.
- The device screen was left blank for a second. Never show an empty screen.
- The same child appeared twice in one collage. Check photo sets.
- Em dashes and "..." in captions read as AI-written. Clean them.
- Stills from earlier runs mixed into contact sheets. Delete `still-*.png` before checking (`find . -name 'still-*.png' -delete`; zsh errors on a bare `rm still-*` when none exist).

## Sticker animation videos (V06 onwards)

Quirky, sarcastic story ads (a narrator character, punchlines) are made as 2D sticker animation in the same pipeline. V06 "Five Minutes" is the reference.

- **Art.** Ravi's family sticker pack is `~/Documents/cheeko-home-sticker-sheet.svg` (45 named symbols, manifest `~/Documents/assets.json`) plus his 16-panel storyboard image. Both come from about 200 px art, so keep stickers at half-screen size or smaller. `work/cut_panels.py` cuts storyboard panels off their white background. Never use the pack's device art or its `device_live.png` link: the device is always `device_current.png` with real `fw-screens`.
- **Sticker look.** Done in the browser: the `#stk` SVG filter (alpha threshold, `feMorphology` dilate for the white die-cut border, soft shadow), a small 8 fps "boil" wobble on every sticker, pop-ins with a bounce, `slam()` for rubber stamps with a screen shake. Hidden scenes use `display:none` as well as `visibility:hidden` (a 3D-rotated sticker kept painting otherwise).
- **Voices.** Several voices are fine: `vo_lines.json` takes `"voices": {"<line>": "<voice id>"}` for extra characters and `"tempo"` to speed up the main voice (`build_vo.py`, run with `VIDS=V06`). Record with `vo_rec.py` on the dev box (`python3 vo_rec.py vo_lines.json V06 [lines]`); it checks each clip with Sarvam speech-to-text. For Hindi words inside English (Nani's "Arre"), use a Hindi voice: `hindi_female_2_v1` says it properly, English voices say "array". MiniMax sound tags that worked: (laughs), (chuckle), (gasps), (sighs).
- **Audio.** `work/mix.py` mixes the voice, real Cheeko sounds (`work/sfx/`: doorbell, clock, battery_low, charge_full, card_insert, success, popup) and synthesised pops and stamps, plus the licensed track at `work/music-src.*` (`MUSIC_START` picks the offset; place it so the track's real ending lands on the end card).
- **Envato music.** Search with the Envato MCP, give Ravi 3 to 5 links, download only after his yes, in the built-in browser where he is signed in (the new Envato app downloads straight away with a Lifetime Commercial License, no project-name step).
- **Speed.** Show Ravi one still per scene (`review_sheet.py`) before recording or rendering. A 34 s sticker video renders in about 5 minutes. Keep `raw-keep.mp4` so a music change only needs `mix.py` and `finish.sh`.

## Series folders and callouts (2026-09-29)

- A series (for now `Onboarding Cheeko`, V20-V24) lives in its own Drive folder built by `publish_to_drive.py` from the `SERIES` map: README, `00 Plan and scripts/` with the series code, every part with all five stages and `5 Source/assets used (assets-img)/` (each image its spec.js shows), and a separate `Ready to post/`.
- Feature template callouts: `[t0, label, sub, px, py, lx, ly, until, bow]`. The arrow is a curved marker line (ink, white halo) that draws itself from the label to the part, lands with a chevron head, and a ring pulses on the target. `bow` is optional (signed fraction of the arrow length); short arrows curve more by default. Ravi asked for this instead of straight dotted lines.

## App walkthroughs (V25 Cheeko App Guide, 2026-09-29)

- **iPhone everywhere:** `makeIphone()` in the feature template draws an iPhone 16 body (titanium frame, bezel, Dynamic Island, side buttons) with the iOS status bar and home bar. Used by the phone, flow and duo shots. App screens come from `assets/img/app-shots-ios/`, rendered as iOS by `appshots/tests/run.sh` (debugDefaultTargetPlatformOverride = iOS, SF as the fallback font). The older `app-shots/` stays for V19 and V22.
- **Phone shot options:** `screens: [[t, src, scroll, pin, tone]]` where `scroll = [t0, t1, y0%, y1%]`, `pin = {src, clip}` keeps the floating tab bar fixed while a tall capture scrolls, `tone = 'light'` turns the status bar white on dark screens. `focus: [[t, px, py, zoom]]` grows the iPhone around a point on its screen (fractions) and `focusAt: [x, y]` slides that point to a spot clear of the captions. `taps` and `callouts` on phone shots use screen fractions and follow the zoom and 3D tilt (`screenPoint()`). Duo shots take fractions too when both values are 1.5 or less.
- **Captions:** `capMax: 6` pages long narrator lines into short chunks (breaks at sentence ends and commas), `capSize: 80` sets the font.
- **Cheeko's theme on screen:** `fwsim/render.sh` now also renders home and menu with `--theme 1|2|3` (Night, Ocean, Candy) as `theme<N>_*.png`; the parent app's theme writes NVS `cheeko/ui_theme`. Settings reach Cheeko only after Save, so show the change on the Save tap.
- **Firmware facts used:** the app's Sleep mode sends `sleep_enabled`, which switches Cheeko's idle timer (dims at 2 min, screen off at 5, naps at 30). It does not put Cheeko to sleep at once.
- **Full films from series parts:** `stitch_series.py stitch/<config>.json` cuts each part 1.2 s after its last line (its "Next" card becomes the chapter card), joins them with short audio fades, and writes `brag.mp4` (vertical) plus `brag-16x9.mp4` (the vertical film centred in a Cheeko frame: title left, chapter list right, lit per chapter; `stitch/series_frame.html`), `thumbnail-16x9.jpg` (YouTube) and `work/chapters.txt` (YouTube chapters). Configs: `stitch/app-guide.json`, `stitch/app-guide-hi.json`. Use the same for the onboarding film (V24). `publish_to_drive.py` copies the 16:9 files and chapters into 4 Final and Ready to post.
- **Hindi series parts:** Hindi lines in `feature_lines_hi.json` (TTS text with चीको, `show` for captions with Cheeko and the English button names), record with `hindi_male_1_v2`, check with Sarvam hi-IN, `build_feature.py ... --lines feature_lines_hi.json --suffix=-hi`, then copy the English `spec.js` into the `-hi` work folder: its `tx(en, hi)` labels switch on the `-HI` vid. Don't use `make_hindi_feature.py` for these (it would override the outro text).

## Master sheet and video library (2026-09-29)

- `master_sheet.py` writes `cheeko ai videos/Cheeko Video Master Sheet.xlsx` (Drive link https://drive.google.com/file/d/1lb_iDUqt2RSnbe0heZl-DkjeKOsL_KEK/view): every video with Watch, 16:9, Thumbnail, Ready to post, All files and Script links (Drive IDs read with `xattr -p com.google.drivefs.item-id#S`), the caption, and sheets "Folders and plans" and "Coming next" (edit `ABOUT` and `COMING` in the script). `publish_to_drive.py` rebuilds it at the end of every full run.
- `library_page.py <out.html>` builds the team's web page from the same data (thumbnails embedded). Hosted for the team on GitHub Pages: https://craftech360-projects.github.io/cheeko-video-library/ (public repo Craftech360-projects/cheeko-video-library, Ravi's choice 2026-09-29; the page has noindex; Drive links still need folder access). After each publish run `marketing/tools/deploy_library.sh` (rebuilds `marketing/library-site/index.html` with `--site`, commits and pushes). A private claude.ai copy also exists: https://claude.ai/artifact/EVVNtCcjfm5gCatVq2d31c.
