# Cheeko Video Kit

Everything we use to make Cheeko marketing videos, packed so another AI workspace (Claude Code, Codex, Cursor, Windsurf) or a person can carry on. It covers V01 to V25 and their Hindi versions, the skills we wrote, the tools, the rules and every video's source.

Built 2026-09-30 from Ravi's Mac. Company: Altio AI Pvt. Ltd. Product: Cheeko, an AI learning device for kids aged 3 to 10.

---

## 1. What engine is this? (Not HyperFrames)

It is **not HyperFrames, Remotion or After Effects**. It is our own small pipeline, and the whole idea fits in one sentence:

> Each video is one HTML page with a function `render(t)` that draws the frame at time `t`. A Node script opens the page in headless Chrome, calls `render` for every frame, screenshots it and pipes the frames into ffmpeg.

```
 lines.json ──TTS, one clip per line──> build_vo.py / build_feature.py ──> vo-tight.wav + timing
                                                                             │
 compose.html (or the feature template + spec.js)  <─────────────────────────┘
      │  window.render(t) for every frame: t = 0, 1/30, 2/30 and so on   (Playwright + headless Chromium)
      ▼
 JPEG frames ──> ffmpeg (H.264, 30 fps, 1080x1920) ──> raw.mp4 ──finish.sh──> brag.mp4
                                          ▲                       (poster as frame 0, -14 LUFS)
 synth.py (numpy music + sfx) or mix.py (licensed track) ──> music-final.wav
```

- `render(t)` is a **pure function of time**. The same `t` always gives the same frame, so renders are exact and repeatable, and you can jump to any second to check it.
- `window.ready` resolves once fonts and images have loaded. Nothing is captured before that.
- All motion is plain HTML, CSS, SVG and JavaScript: no framework, no build step. An AI can make or fix a video by editing one file.
- The renderer is about 20 lines: `skills/cheeko-video/scripts/render.mjs` (the same file sits in every video's `work/`).
- HyperFrames and Remotion do the same job ("HTML in, MP4 out") as full frameworks. If you ever move to one of them, `compose.html` ports easily, because `render(t)` is already what they call a composition.

---

## 2. What is in the zip

```
cheeko-video-kit/
  START-HERE.md        this file
  AGENTS.md            instructions any AI agent reads first (Codex, Cursor, Windsurf, Copilot read it automatically)
  CLAUDE.md            the same for Claude Code (it imports AGENTS.md)
  setup.sh             one-time setup (paths, Playwright + Chromium, Python venv)
  selftest.sh          renders a 2 second test video to prove the setup works
  selftest/            the test composition (a good minimal example of the method)
  skills/
    cheeko-video/      THE skill we made: hard rules, voices, workflow (SKILL.md)
    brag-slim/         the general creative method it builds on (plan, build, check, render, deliver)
  docs/
    plan/              video tracker, all 28 ideas, feature video scripts, voiceover text, video list (from Drive "00 Plan")
    decisions/         Ravi's decisions and corrections, one note each (style, voices, cards, the new device design and more)
  workspace/           a copy of the "Cheeko Master" folder, same layout as on Ravi's Mac
    marketing/tools/   all pipeline tools (see section 6), HOW-WE-MAKE-VIDEOS.md, production-rules.md
    marketing/*.md     plans: device refresh, app walkthrough, getting-started series, feature videos and more
    marketing/web-components/cheeko-device-animation/   the animated "Meet the device" website section
    cheeko-v2-website/
      .claude/skills/  the project copies of the skills, with the render scripts (scripts/)
      brag-output*/    the SOURCE of every video made so far (compose.html, spec.js, synth.py, lines, timing)
      thumbs-work/     thumbnail (Reel cover) builders
      assets/img/      device-v2 renders (yellow, pink, white; 4 views), fw-screens (180 real device screens),
                       cards-shipping (the 10 real cards), app, myo
    cheeko-os-v2/main/assets/common/   real Cheeko sounds (card insert, knob click, success and more)
```

**cheeko-video-kit-extra-assets.zip** (optional, 140 MB) unzips over the same folder and adds the full-size device renders (needed for thumbnails) and the parent app screenshots (needed for the app videos V19 to V25).

---

## 3. Set up in a new workspace (about 15 minutes)

Needs: macOS or Linux, Node 22+, Python 3.10+, ffmpeg, git and rsync (only for `--with-site`).

```bash
unzip cheeko-video-kit.zip && cd cheeko-video-kit
unzip ../cheeko-video-kit-extra-assets.zip -d ..     # optional, see above
bash setup.sh --with-site                            # --with-site also pulls the website's photos from GitHub
bash selftest.sh                                     # should end with "OK: .../selftest.mp4"
```

What `setup.sh` does:
1. The docs and scripts were written with the path `/Users/ravikumar/Cheeko Master`. It rewrites that to this kit's `workspace/` folder everywhere. Run it again after moving the folder. If you skip setup, read that path as `workspace/`.
2. `--with-site` clones the public website repo (Craftech360-projects/cheeko-v2-website) and adds its images (the kids photos in `assets/img/live`, the `imagine/` drawings, the logo and more) without overwriting anything. Most older videos need these.
3. Installs Playwright 1.58 + Chromium in `workspace/cheeko-v2-website/node_modules`.
4. Makes the Python venv `workspace/cheeko-v2-website/.venv` with numpy, Pillow, requests, websocket-client.

---

## 4. Use it with your AI tool

**Claude Code**
- Copy the skills: `cp -R skills/* ~/.claude/skills/` (or into `<project>/.claude/skills/`).
- Open the kit folder. `CLAUDE.md` is read automatically. The skill loads when you ask for a Cheeko video.

**Codex (OpenAI)**
- Open the kit folder. `AGENTS.md` is read automatically.
- If your Codex version supports skills, copy `skills/*` into its skills folder (`~/.codex/skills/`). If not, AGENTS.md already tells it to read `skills/cheeko-video/SKILL.md`.

**Cursor, Windsurf, Copilot, others**
- Open the kit folder. Most read `AGENTS.md`. If yours doesn't, add AGENTS.md and `skills/cheeko-video/SKILL.md` as project rules.

**Chat only (ChatGPT, claude.ai, Gemini)**
- Upload START-HERE.md, `skills/cheeko-video/SKILL.md`, `workspace/marketing/tools/HOW-WE-MAKE-VIDEOS.md` and `production-rules.md`.
- A chat can write scripts, voice lines and `compose.html`, but it cannot render. Render on a machine with this kit.

**First message to paste into the AI:**

```
Read AGENTS.md, then skills/cheeko-video/SKILL.md, workspace/marketing/tools/HOW-WE-MAKE-VIDEOS.md
and workspace/marketing/tools/production-rules.md. Then look at docs/plan/Video tracker.md to see what exists.
Make a new Cheeko Instagram Reel about <topic>. Show me the script and the shot list first, and wait for my OK
before recording voices or rendering.
```

---

## 5. Voices (you need your own API keys)

Voices are recorded one line at a time, each line with its own emotion, then checked with speech-to-text. On Ravi's setup this ran on the dev box (`vo_rec.py`, `feature_rec.py`). Anywhere else use **`workspace/marketing/tools/voice/rec_anywhere.py`**, which reads keys from environment variables and never writes them to disk:

```bash
export MINIMAX_API_KEY=...   # MiniMax speech-2.8-hd via Tencent TokenHub (see tools/voice/tts_test.py)
export QWEN_API_KEY=...      # only for Qwen voices (Mitthu, Quizzy in English)
export SARVAM_API_KEY=...    # optional: speech-to-text check of every clip
cd workspace/marketing/tools
../../cheeko-v2-website/.venv/bin/python voice/rec_anywhere.py feature_lines.json V12 clips/V12 --dry   # preview
../../cheeko-v2-website/.venv/bin/python voice/rec_anywhere.py feature_lines.json V12 clips/V12         # record
```

It takes both line formats (`vo_lines.json` and `feature_lines.json`); add `--lang=hi` for Hindi. Never put keys in a file, a script or a chat.

| Who | Voice |
|---|---|
| Narrator (English) | MiniMax `English_Upbeat_Woman` |
| Cheeko | MiniMax `English_PlayfulGirl` |
| Nani | MiniMax `English_Graceful_Lady` |
| Mitthu | Qwen `loongnorahu` |
| Quizzy | Qwen `loongivyhu` |
| Kid | MiniMax `English_LovelyGirl` |
| Hindi narrator / Quizzy / grandma | MiniMax `hindi_male_1_v2` / `hindi_female_1_v2` / `hindi_female_2_v1` |

---

## 6. The tools (workspace/marketing/tools)

| Tool | What it does |
|---|---|
| `HOW-WE-MAKE-VIDEOS.md` | The full process, step by step, and every mistake we made once. **Read first.** |
| `production-rules.md` | Style, facts and the never-do list. **Read second.** |
| `feature/` | Template for one-feature Reels: `setup.sh <video dir>` copies it; you only write `work/spec.js` (a list of shots). Also `synth.py`, `cues.mjs`, `make_hindi_feature.py`. |
| `build_vo.py`, `build_feature.py` | Turn recorded clips into `vo-tight.wav` plus timing, so scenes follow the voice |
| `vo_lines.json`, `feature_lines.json` (+ `_hi`) | The voice lines of every video, English and Hindi |
| `voice/rec_anywhere.py`, `voice/tts_test.py` | Record voices on any machine (keys from env vars) |
| `make_hindi.py`, `captions_clean.py` | Hindi versions; remove AI-looking punctuation and add emojis to captions |
| `stitch_series.py`, `stitch/` | Join series parts into one film, plus a 16:9 YouTube version with chapters |
| `fwsim/` | Renders the real device screens from the firmware source (needs the private cheeko-os-v2 repo). The 180 screens it made are already in `assets/img/fw-screens/`. |
| `appshots/` | Renders parent app screens (needs the private Flutter app repo). Results are in the extra assets zip. |
| `device_v2_mask.py`, `device_anim_assets.py` | Screen mask for the new device; assets for the website's device animation |
| `publish_to_drive.py`, `master_sheet.py`, `library_page.py`, `deploy_library.sh`, `collect_assets.py` | Publishing to Ravi's Google Drive and the team page. **Only work on Ravi's Mac.** Elsewhere, send the finished files instead. |
| `make_video_kit.py` | Builds this kit again |

Inside every video's `work/` folder: `render.mjs` (render), `stills.mjs` + `sheet.py` (check frames before rendering), `finish.sh` (final file), `synth.py` or `mix.py` (music).

---

## 7. The rules that matter most

The full list is in `production-rules.md` and the skill. These are the ones people got corrected on:

- **Instagram Reels first:** hook in the first second, a new shot every 1 to 2 seconds, word-synced captions, fun and energetic, about 20 to 35 seconds. Slow brand films were rejected.
- **No AI tells anywhere people read or hear:** no em dashes, no ellipsis character, no curly quotes. Write like a person.
- **Emojis** in captions and thumbnails, never in voice text. **Every video gets a thumbnail** (1080x1920).
- **Voice:** one clip per line, each with its own emotion. A single take sounds flat.
- **Device:** only the NEW design (`assets/img/device-v2/`), screens only from `fw-screens/`, clipped by the screen mask, never blank. Cards slide into the pocket on the BACK with the top third showing, never into the top.
- **Cards:** only the 10 shipping cards in `assets/img/cards-shipping/`.
- **Facts:** Rs 5,999 for the device + 10 cards, free delivery across India, 12-month warranty, 6-hour battery, English + 10 Indian languages, 8 offline games, Talk and Imagine free for 3 months then an optional plan, new cards 5 for Rs 499. Never say "once" or "one-time" about the price. No certification claims. No Indian flag, other brands or characters.
- **Never the same child twice in one video.** Check every transition mid-wipe and every device screen close up.
- **Hindi versions:** Hindi voice, captions and on-screen text. The device itself cannot show Hindi text (its fonts have no Devanagari), so Hindi on the device screen shows blank. Show it as it is.

---

## 8. Not in the kit

- **API keys** (MiniMax, Qwen, Sarvam): set them as environment variables (section 5).
- **Finished videos, voice takes, licensed music and per-video stickers:** in Ravi's Google Drive "cheeko ai videos" (each video's `2 Voice`, `4 Final` and `5 Source`). The video folders here hold only the text source, so to re-render an old video, first copy its `work/vo/`, music and stickers from Drive.
- **Licensed Envato music:** licences are per video. Search Envato, pick with Ravi, download under his account.
- **Firmware and app source** (for `fwsim` and `appshots`): private repos. Their output is included.
- **Rendered test frames and build output:** re-create them with `stills.mjs` and `render.mjs`.

---

## 9. Where the originals live

- Tools, plans, the kit builder: Ravi's Mac `Cheeko Master/marketing/`
- Video source: `Cheeko Master/cheeko-v2-website/brag-output*/` (GitHub repo `Craftech360-projects/cheeko-v2-website`, which is **public**, so never commit keys or unreleased plans there)
- Finished videos and team copies: Google Drive "cheeko ai videos"
- Team video page: https://craftech360-projects.github.io/cheeko-video-library/
