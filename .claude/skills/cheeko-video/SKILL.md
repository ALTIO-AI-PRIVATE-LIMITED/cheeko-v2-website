---
name: cheeko-video
description: Make short launch or social videos (Reels, Shorts, YouTube) for Cheeko, the AI learning device for kids, from this website repo's own copy and images, with original synthesised music. Use when someone asks for a Cheeko video, a launch video, a reel, "/brag" or "brag about this", a feature explainer video, or wants to redo, re-roll or edit one of the videos in brag-output*/. Builds on the /brag-slim skill in .claude/skills/brag-slim, adding Cheeko's brand, asset map, rules and a working render pipeline.
---

# Cheeko video

Follow `.claude/skills/brag-slim/SKILL.md` for the creative method: inspect, plan, build, check, render, deliver. This file adds what is specific to Cheeko and the pipeline that already works in this repo. Three finished examples are in the repo. Read the closest one before building, because each `work/compose.html` is a complete, working composition to adapt:

| Folder | Video | Style |
|---|---|---|
| `brag-output/` | All features in 22s: Cards, Talk, Imagine, Games, Languages, Radio, Funny Voice, Parent app | Fast, fun, colour-block scenes at 120 BPM |
| `brag-output-2026-09-28-095057/` | One feature, the cards: "Kid bored? Skip the phone. Hand them Cheeko." | Story in three acts, a bored intro then 120 BPM |
| git history of `brag-output/` (first commit) | Polished 5-scene version | Slow, elegant, 96 BPM |

Put each new video in a new timestamped folder (`brag-output-YYYY-MM-DD-HHMMSS/`) so earlier ones are kept. Deliverables go in that folder (`brag.mp4`, `brag.jpg`, `share-copy.txt`, `brag-plan.md`). Sources go in its `work/` folder (`compose.html`, `synth.py`). Don't commit renders, stills or WAVs from `work/`.

## Product facts (from `index.html`; re-check it, since the site changes)

- Cheeko is India's AI learning device for ages 3–10, by Altio AI. It costs **₹5,999 for the device and 10 cards**, with free delivery across India, a 6-month warranty and 7-day returns. The site is cheekoai.in.
- Headline: **"Less screen, more childhood."** Manifesto: "No video. No feed. No ads. All play."
- Cards: "Insert a card and stories play." "Insert. Play. Repeat." Ten cards come in the box: stories, rhymes, games, characters, and Make Your Own. 15 more cards launch at ₹199–₹299.
- Talk: "Ask anything." Imagine: "Say a wish, see it drawn" / "Say it. See it." Games: "8 built-in, all offline". Languages: "English + 10 Indian". Radio: "Kid-safe channels". Funny Voice: "Instant giggles". Parent app: "You see everything".

## Rules (the owner asked for these)

- **Never say "once" or "one-time" about the price.** Talk and Imagine are free for 3 months, then an optional plan. Write "₹5,999 · Device + 10 cards".
- **No dates that have passed.** The site's "Ships by 25 September" is stale, so leave it out.
- **Every claim, number and line comes from the site.** Nothing invented: no testimonials and no stats.
- **The device screen must match what is happening.** `assets/img/device_live.png` always shows the **Talk** home menu. That's fine when the device is idle, but wrong once a card is playing. When a card is in, cover the screen with that card's world art (see "Device screen" below). This matches the real device photo `assets/img/live/kid-rhymes-screen.jpg`.
- The owner liked **fast, fun, bright** videos best. Default to vertical 1080×1920, about 20–23s, 120 BPM, bouncy pops, slide cuts and confetti. Use polished and slow only if asked.

## Brand (`assets/css/premium.css`)

- Colours: orange `#F0521D`, sun `#FFC81A`, ink `#231A10`, tint `#FFF4E3`, cream text `#FFF6E8`, green `#2F6B4F`, purple `#6C3DFF`, and pink `#FFA9C9` (from the pink colourway).
- Fonts: Gabarito (display, 800–900) and Hanken Grotesk (body), loaded from Google Fonts. Indic scripts need Noto Sans Devanagari, Kannada, Tamil, Telugu and Bengali.
- The yellow sun highlight behind a word ("more **childhood.**", "**All play.**") is the site's signature. Reuse it.

## Asset map (`assets/img/`)

| Need | Use |
|---|---|
| Device, transparent, front | `device_live.png` (500×847, Talk menu on screen) |
| Real card fronts (760×1196) | `live/card-storytime.jpg` (stories), `card-ravi.jpg`, `card-clever.jpg`, `card-nani.jpg`, `card-mitthu.jpg` (spelling), `card-playsing.jpg` (rhymes), `card-dreamy.jpg`, `card-lava.jpg` (game), `card-makeyourown.jpg` |
| Card worlds (screen and background) | `bg_stories.jpg` (jungle lion), `rhymes_world.jpg` (cow over the moon, portrait), `bg_games.jpg` (glowing games world), `bg_rhymes.jpg` (moonlit night) |
| Fox mascot art, transparent | `live/menu-talk.png`, `menu-games.png` (controller), `menu-radio.png` (headphones), `menu-funny.png` (megaphone), `menu-imagine.png`, `char-cheeko.png` |
| Characters | `live/char-quizzy.png`, `char-nani.png`, `char-mitthu.png`, `char-chanda.png`, `char-masti.png`, `char-tara.png` |
| Imagine drawings (320×240, small) | `imagine/im-05.jpg` tiger on a bicycle, `im-07` auto rickshaw to the moon, `im-17` robot cooking dosa, and more; captions are in `index.html` |
| Real kids (Bengaluru shoot) | `live/hero-1.jpg` (family), `hero-kid-slot.jpg` / `slot-card-boy.jpg` / `s3-tap-card.jpg` (inserting a card), `kid-dance.jpg`, `s2-child-holding.jpg`, `use-1..9.jpg` |
| The phone problem | `problem1_v2.jpg` (kid glued to a phone, mum watching), `phone_problem.png` (darker) |
| Parent app | `live/s2-manage-content.jpg` |
| Logo | `logo.png` (transparent) |

### Device screen

In `device_live.png` the screen sits at **x 118–418, y 94–334** (inside the bezel, radius about 28px). Scale it with the device. Wrap the device image and a `#scr` overlay in one container so they squash together. `brag-output-2026-09-28-095057/work/compose.html` shows the full pattern: `#devwrap`, `#scr`, and a circle-reveal of each card's world as it lands.

## Pipeline

It needs Node 22+, Playwright with Chromium, ffmpeg and Python 3 with numpy.
- **In the cloud container:** run `pip install imageio-ffmpeg numpy pillow`, then get ffmpeg's path with `python3 -c "import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())"`. Chromium is preinstalled.
- **On your own computer:** install ffmpeg and playwright normally.

1. **Plan:** write `brag-plan.md` with the angle, a storyboard with times on a 0.5s beat grid, the sound and an honesty check.
2. **Compose:** write `work/compose.html` so that `window.render(t)` is a pure function of time and `window.ready` resolves after fonts and images decode. Reference assets as `../../assets/img/...`.
3. **Music:** write `work/synth.py`, adapted from an example (it writes `music-final.wav`). All music and sound effects are synthesised with numpy in one key. It can't be listened to in the cloud, so check the level of each second instead. The intro must not be louder than the main groove, and sound effects must sit under the music.
4. **Check:** copy the scripts in, then run `node stills.mjs <times...>` and `python3 sheet.py <cols>`. Look at `sheet.png` for every scene and mid-transition. Known traps:
   - Give every scene layer `z-index:0`. Without it, children with a z-index paint over later scenes.
   - A child with `visibility:visible` ignores a hidden parent, so gate child visibility by scene time too.
   - White text needs its dark background fully in place first.
5. **Render:** run `node render.mjs <ffmpeg> <seconds>`. It takes about 1 minute for 22s.
6. **Finish:** run `bash finish.sh <ffmpeg> <seconds> <poster-time>`. The poster is the strongest settled frame and is baked in as frame 0.
7. **Deliver:** write `share-copy.txt` (1–3 sentences, no "once"). Send the video and poster to the user, give one line on the angle, and offer to redo a scene.

Copy the scripts into `work/` from `.claude/skills/cheeko-video/scripts/` (`pw.mjs`, `render.mjs`, `stills.mjs`, `sheet.py`, `finish.sh`).

Note: Netlify publishes the repo root (`netlify.toml`: `publish = "."`), so `brag-output*/` folders are public on the live site once merged.
