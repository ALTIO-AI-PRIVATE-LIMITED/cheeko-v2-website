---
name: cheeko-video
description: Make, change, re-voice, translate or publish marketing videos for Cheeko (Altio AI's kids' learning device) - Instagram Reels, films, Hindi versions, thumbnails, voiceovers, captions and the "cheeko ai videos" Google Drive. Use whenever Ravi asks for a Cheeko video, reel, short, ad, thumbnail, voiceover, Hindi/regional version, caption, "next video from the list", "ready to post", or to fix anything in V01, V02, V03... (including "the voice sounds flat", "there's a gap", "screen corners wrong"). Also use before claiming what the Cheeko device can do on screen.
---

# Cheeko video

Ravi (firmware lead, Altio AI) uses one thread for all Cheeko videos. Everything below was learned making V01 to V05 and V03-HI to V05-HI on 2026-09-28. The full, current process is in these files; read the first two before doing anything:

1. `/Users/ravikumar/Cheeko Master/marketing/tools/HOW-WE-MAKE-VIDEOS.md` - pipeline, tools, where everything lives, past mistakes
2. `/Users/ravikumar/Cheeko Master/marketing/tools/production-rules.md` - style, facts, never-do list
3. `/Users/ravikumar/Cheeko Master/marketing/cheeko-video-ideas.md` - the 28 video ideas and which are done
4. Drive `cheeko ai videos/00 Plan/Video tracker.md` - IDs, lengths, final file names

Each finished video also has `TECHNICAL.md` in its Drive folder with its lines, assets and rebuild commands.

## Hard rules (Ravi's feedback, each one was a correction)

- **Reels first.** Hook in the first second, a new shot every 1-2 s, word-synced captions, fun and energetic, about 20-35 s. Slow, calm brand films were rejected.
- **Voice:** one clip per line, each with its own emotion. English MiniMax `speech-2.8-hd` voice `English_Upbeat_Woman`; Hindi MiniMax `hindi_male_1_v2` (Qwen multilingual garbled Hindi). A single-emotion take sounds flat.
- **No AI tells anywhere people read or hear:** no em dashes, no ellipsis character, no curly quotes. Write like a person. This applies to your chat replies too.
- **Emojis** in on-screen captions (after key words, never on a line's first word), Instagram captions and thumbnails. Never in voice text.
- **Every video gets a thumbnail** (1080x1920 Reel cover, key content inside the centre 3:4).
- **Every Hindi video:** Hindi voice, Hindi captions and on-screen text, the child's Imagine wish in Hindi too (the device takes any language). Write Cheeko as चीको for TTS and avoid hyphens inside Hindi phrases (they cause pauses).
- **Device: the NEW design (Sep 2026) only.** Renders in `assets/img/device-v2/` (yellow hero, pink, white; front, right, left, back), screen mask `device-v2/screen_mask.png` (RGBA: CSS masks use alpha), firmware screens from `assets/img/fw-screens/` (made by `marketing/tools/fwsim`). The old `device_current.png` and `device_live.png` are retired; never a blank screen. Card art on the screen is cropped, never stretched.
- **Cards go into the pocket on the BACK**, never the top: 68% of Cheeko's width, centred on the body, the top third showing above the head; cards have the same art on both sides. Photos of people with the earlier device stay in use (Ravi).
- **Motion:** Ravi's picks are built into the template (transitions `tr`: circle, lens, card, portal, whip, shape; shot types turntable, cardwheel, deck, dicetitle, vortex, trio, device `popout`). See `marketing/device-refresh-plan.md`.
- **Cards:** only the 10 shipping cards in `assets/img/cards-shipping/` (Tales of Kindness, Floor is Lava!, Play & Sing Along, Dreamy Melodies, Mitthu the Parrot, Make Your Own, Clever Little Tales, The Adventures of Ravi & Nila, Sounds Around Me, Nani). Sounds Around Me includes the pressure cooker and doorbell.
- **Facts:** Rs 5,999 for device + 10 cards, free delivery across India, 12-month warranty, 6-hour battery, English + 10 Indian languages, 8 offline games, Talk and Imagine free for 3 months then optional plan. New cards are 5 for Rs 499. Mitthu = English learning teacher; Nani = storyteller (incl. bedtime). Dropped from the list: Radio, Bedtime (Chanda), The honest bill. Never say "once"/"one-time" about price. No certifications claimed. No Indian flag, other brands or characters (the Imagine demo video shows Spider-Man: don't use it).
- **The device cannot display Hindi text** (no Devanagari glyphs in the firmware fonts): Hindi transcripts and captions render blank on screen. Show exactly that; mention it to Ravi if relevant.
- **Never the same child twice in one video.** Check every transition mid-wipe and every device screen in close-up before rendering.

## Character voices (Ravi, 2026-09-29)

Cheeko = MiniMax `English_PlayfulGirl`; Mitthu = Qwen `loongnorahu` (Lively & Spirited); Nani = MiniMax `English_Graceful_Lady`; Quizzy = Qwen `loongivyhu` (Confident & Poised); narrator = MiniMax `English_Upbeat_Woman`; kid = MiniMax `English_LovelyGirl` (voice + speech bubble). Hindi versions use MiniMax for everyone (narrator `hindi_male_1_v2`, Quizzy `hindi_female_1_v2`, grandma `hindi_female_2_v1`) because Qwen garbles Hindi. Quiz questions come from the real quiz bank (dev DB `quiz_question`). For one-feature videos use the feature template (`marketing/tools/feature`, see HOW-WE-MAKE-VIDEOS.md): you only write `spec.js`.

## Workflow

Script (`vo_lines.json` / `vo_lines_hi.json`) -> record lines on the dev box (`root@64.227.170.31`, `/root/tts-compare/tts_test.py`, keys read from the `ui.py` process env, never copied off the box) -> check each clip with Sarvam speech-to-text -> copy clips to the Mac -> `build_vo.py` (voice + `warp.json`) -> `compose.html` (+ `make_hindi.py`, `captions_clean.py`) -> `synth.py` (music) -> stills + contact sheet -> `render.mjs` + `finish.sh` -> `thumbs-work/make_thumbs.mjs` -> add the video to `VIDEOS` in `publish_to_drive.py` and run it. Details and exact commands are in HOW-WE-MAKE-VIDEOS.md.

New videos take the next ID (V06, V07...) in a new `cheeko-v2-website/brag-output-<date>-<slug>/` folder; Hindi copies end in `-hi` and get IDs like `V06-HI`. Save each test render into the video's `3 Test` folder.

## Drive

"cheeko ai videos" (https://drive.google.com/drive/folders/1UKxS504Qrz3kz__yzoQxep8K_Viz4-BR) is synced at `~/Library/CloudStorage/GoogleDrive-ravi.ramp36@gmail.com/My Drive/cheeko ai videos`. `publish_to_drive.py` builds everything: `00 Plan`, `01 Shared assets` (all repo media, current firmware screens, real device sounds, shipping cards, Music), one folder per video (1 Script, 2 Voice, 3 Test, 4 Final, 5 Source, TECHNICAL.md), and `Ready to post/English|Hindi/<video>/` with only the video, thumbnail and caption. A series gets its own folder instead (`Onboarding Cheeko/` for the Getting Started parts V20-V24): README, `00 Plan and scripts/` (plan + series code), each part with all five stages plus `5 Source/assets used (assets-img)/`, and its own `Ready to post/`. Add new series to `SERIES` in `publish_to_drive.py`.

## Music and stock assets

Music is synthesised per video (`synth.py`). For licensed music, search Envato (MCP at `https://mcp.envato.com/mcp`, no sign-in; or call it with curl JSON-RPC), give Ravi 3-5 links, and download only after he says yes for each item in the built-in browser where he is signed in; register the licence to the video name. Never enter his password.

## Before you finish

Send the video(s) with SendUserFile, publish to Drive, update the tracker/ideas list, and tell Ravi what changed in plain words, without em dashes.

After publishing, the master sheet (`cheeko ai videos/Cheeko Video Master Sheet.xlsx`) is rebuilt automatically; add a one-line `ABOUT` entry for each new video in `marketing/tools/master_sheet.py`, then run `marketing/tools/deploy_library.sh` to update the team page https://craftech360-projects.github.io/cheeko-video-library/ (GitHub Pages).


## Using this skill outside Ravi's Mac (Cheeko Video Kit)

- Paths above that start with `/Users/ravikumar/Cheeko Master` mean the kit's `workspace/` folder (`bash setup.sh` rewrites them).
- The dev box and its recorders (`vo_rec.py`, `feature_rec.py`) are not available. Record with `workspace/marketing/tools/voice/rec_anywhere.py`, which takes `MINIMAX_API_KEY`, `QWEN_API_KEY` and `SARVAM_API_KEY` from environment variables.
- Google Drive publishing, the master sheet and the team page only work on Ravi's Mac. Hand over the finished video, thumbnail and caption instead.
- The render scripts are in `scripts/` next to this file (`render.mjs`, `stills.mjs`, `sheet.py`, `finish.sh`, `pw.mjs`).
