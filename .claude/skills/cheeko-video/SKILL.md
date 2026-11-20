---
name: cheeko-video
description: Make short launch or social videos (Reels, Shorts, YouTube) for Cheeko, the AI learning device for kids, from this website repo's own copy and images, with original synthesised music. Use when someone asks for a Cheeko video, a launch video, a reel, "/brag" or "brag about this", a feature explainer video, or wants to redo, re-roll or edit one of the videos in brag-output*/. Builds on the /brag-slim skill in .claude/skills/brag-slim, adding Cheeko's brand, asset map, rules and a working render pipeline.
---

# Cheeko video

## Latest process (updated 2026-09-28, read this first)

Videos V01 to V05 and Hindi V03-HI to V05-HI were made with a newer pipeline than the one described below. The full guide is `HOW WE MAKE CHEEKO VIDEOS.md` and the style rules are `Production rules.md`, both in the Google Drive folder "cheeko ai videos/00 Plan" (all scripts are in `00 Plan/Pipeline code`). On Ravi's Mac the same files are in `/Users/ravikumar/Cheeko Master/marketing/tools/`, and a user-level skill `~/.claude/skills/cheeko-video` summarises them. The short version:

- Reels first: hook in the first second, a new shot every 1-2 s, word-synced captions with emojis, about 20-35 s, plus a designed thumbnail (1080x1920).
- Voiceover recorded one line at a time with its own emotion: MiniMax `speech-2.8-hd`, English voice `English_Upbeat_Woman`, Hindi voice `hindi_male_1_v2`. Lines live in `vo_lines.json` / `vo_lines_hi.json`; `build_vo.py` writes the voice and `work/warp.json`, and each `compose.html` follows the voice through a time-warp script.
- No em dashes, no ellipsis character, no curly quotes in anything people read or hear. Emojis in captions, never in voice text.
- Only the 10 shipping cards (`assets/img/cards-shipping/`), the current device image (`assets/img/device_current.png`) and real firmware screens (`assets/img/fw-screens/`, rendered from cheeko-os-v2). Never `device_live.png`, `live/card-*.jpg` or the July design-handoff screenshots.
- The firmware cannot display Hindi text, so Hindi transcripts and captions show blank on the device.
- Finals are published by `publish_to_drive.py` to Drive, including `Ready to post/English|Hindi/<video>/` (video, thumbnail, caption).

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
| Device, transparent, front | **`device_current.png`** (500×847) — the current firmware home screen (light "Sunny" theme, TALK) composited into the screen. `device_live.png` shows the OLD dark UI: don't use it |
| Current device screens | `fw-screens/*.png` (296×240) rendered from the firmware itself (b05c95d, FW 2.4.311) with `marketing/tools/fwsim`: every menu item, Talk states for all 7 characters, all 8 games, Funny Voice, Radio, Imagine (plus `imagine_tiger_*` / `imagine_rickshaw_*` with real drawings), settings, card reveal, charging, tutorial. Put them on the device through the `.scr` mask. The Talk picker only offers Cheeko and Quizzy |
| **Shipping cards (use these)** | `cards-shipping/01-tales-of-kindness.jpg`, `02-floor-is-lava`, `03-play-and-sing-along`, `04-dreamy-melodies`, `05-mitthu-the-parrot`, `06-make-your-own`, `07-clever-little-tales`, `08-ravi-and-nila`, `09-sounds-around-me`, `10-nani` (760×1196; full-size art for backgrounds in `cards-shipping/large/`). These are the 10 cards that actually ship (Ravi, 2026-09-28); originals and a README are in `Cheeko Master/marketing/cards-shipping/`. |
| Old website card fronts (do not use) | `live/card-*.jpg` — "Storytime Adventures", "Ravi's Wild Journey" and "Around the House" do not ship |
| Card worlds (screen and background) | `bg_stories.jpg` (jungle lion), `rhymes_world.jpg` (cow over the moon, portrait), `bg_games.jpg` (glowing games world), `bg_rhymes.jpg` (moonlit night) |
| Fox mascot art, transparent | `live/menu-talk.png`, `menu-games.png` (controller), `menu-radio.png` (headphones), `menu-funny.png` (megaphone), `menu-imagine.png`, `char-cheeko.png` |
| Characters | `live/char-quizzy.png`, `char-nani.png`, `char-mitthu.png`, `char-chanda.png`, `char-masti.png`, `char-tara.png` |
| Imagine drawings (320×240, small) | `imagine/im-05.jpg` tiger on a bicycle, `im-07` auto rickshaw to the moon, `im-17` robot cooking dosa, and more; captions are in `index.html` |
| Real kids (Bengaluru shoot) | `live/hero-1.jpg` (family), `hero-kid-slot.jpg` / `slot-card-boy.jpg` / `s3-tap-card.jpg` (inserting a card), `kid-dance.jpg`, `s2-child-holding.jpg`, `use-1..9.jpg` |
| The phone problem | `problem1_v2.jpg` (kid glued to a phone, mum watching), `phone_problem.png` (darker) |
| Parent app | `live/s2-manage-content.jpg` |
| Logo | `logo.png` (transparent) |

### Device screen

The screen is not a plain rounded rectangle: its corners are uneven, so a CSS `border-radius` box pokes out past the bezel (Ravi caught this on a phone). Always clip screen content with the measured mask `assets/img/device_live_screen_mask.png` (312×254, the dark screen area of `device_live.png` at **x 112–424, y 88–342**). Size the overlay in percentages so it scales with any device size, and inline the mask as a `data:` URI, because Chromium refuses CSS masks loaded from `file://` and silently hides the element instead:

```css
.scr{position:absolute;left:22.4%;top:10.39%;width:62.4%;height:29.99%;overflow:hidden;
  -webkit-mask:url(data:image/png;base64,...) 0 0/100% 100% no-repeat; mask:url(data:image/png;base64,...) 0 0/100% 100% no-repeat}
```

Put the device image and the `.scr` overlay in one container so they squash together. Never leave the screen blank or black while the device is on camera: the idle screen is the Talk menu (it is baked into `device_live.png`), so only cover it when something else is really on screen. `brag-output-2026-09-28-made-to-end/work/compose.html` has the full pattern (menus flipping, the screen dimming to sleep); `brag-output-2026-09-28-reel/work/compose.html` has a card's world and an Imagine drawing appearing on screen.

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
