# Instructions for AI agents: Cheeko videos

You are helping Altio AI make marketing videos (mostly Instagram Reels, some 16:9 films) for **Cheeko**, an AI learning device for kids aged 3 to 10, sold in India. The owner is Ravi.

## Read these first, in this order
1. `START-HERE.md` (what the kit is, setup, what is missing)
2. `skills/cheeko-video/SKILL.md` (hard rules, voices, workflow)
3. `workspace/marketing/tools/HOW-WE-MAKE-VIDEOS.md` (the pipeline step by step, with commands)
4. `workspace/marketing/tools/production-rules.md` (style, facts, never-do list)
5. `docs/plan/Video tracker.md` (which videos exist) and `docs/decisions/` (Ravi's past corrections)

For the general creative method (plan, build, check, render, deliver) see `skills/brag-slim/SKILL.md`.

## Paths
Docs and scripts mention `/Users/ravikumar/Cheeko Master`. After `bash setup.sh` they point at this kit's `workspace/` folder. If setup has not run, read that path as `workspace/`. Anything under `~/Library/CloudStorage/...` is Ravi's Google Drive and does not exist here.

## How a video is built
One HTML page per video (`work/compose.html`, or the feature template plus `work/spec.js`) exposes `window.render(t)` (a pure function of time) and `window.ready`. `render.mjs` renders it frame by frame with Playwright + Chromium into ffmpeg. Music is `synth.py` (numpy) or `mix.py` (licensed track). Check with `stills.mjs` + `sheet.py` before any full render. `bash selftest.sh` proves the setup works.

## Rules you must not break
- Reels style: hook in the first second, new shot every 1 to 2 seconds, word-synced captions, energetic, 20 to 35 seconds.
- No em dashes, no ellipsis character, no curly quotes in anything people read or hear, and in your replies to Ravi. Emojis in captions and thumbnails only, never in voice text.
- Device: new design only (`assets/img/device-v2/`), real screens only (`assets/img/fw-screens/`), clipped by the screen mask, never blank. Cards go into the back pocket, top third showing. Only the 10 cards in `assets/img/cards-shipping/`.
- Facts only from `production-rules.md`. Never "once" or "one-time" about price, no certifications, no Indian flag, no other brands or characters, no invented testimonials or numbers.
- Never the same child twice in one video.
- Hindi versions: Hindi voice and captions; the device screen cannot show Hindi text.

## Working with Ravi
- Show the script and shot list first. Record voices and render only after his OK.
- Voice keys come from environment variables (`MINIMAX_API_KEY`, `QWEN_API_KEY`, `SARVAM_API_KEY`). Never write a key into a file, script, commit or message. Never ask him to paste one into chat.
- Do not buy or download licensed music without his yes for each item.
- `workspace/cheeko-v2-website` mirrors a **public** GitHub repo. Do not commit keys, drafts or unreleased plans there, and do not push without asking.
- Publishing scripts (`publish_to_drive.py`, `deploy_library.sh`, `master_sheet.py`) only work on Ravi's Mac. Here, hand over the finished files: the video, the thumbnail and the Instagram caption.
- New videos go in a new folder `workspace/cheeko-v2-website/brag-output-<date>-<slug>/`; check `docs/plan/Video tracker.md` for the next free ID.
