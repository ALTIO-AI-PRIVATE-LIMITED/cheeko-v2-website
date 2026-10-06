# Local Video Marquee Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the homepage Instagram reel embeds with six unique, playable local Cheeko videos in a seamless right-to-left marquee.

**Architecture:** Keep the existing static HTML/CSS/JavaScript structure. Both marquee groups contain playable video cards so every card visible during the seamless loop remains interactive. A small Node built-in test suite checks the section contract and playback safeguards without adding dependencies.

**Tech Stack:** HTML5 video, CSS animation, vanilla JavaScript, Node.js `node:test`, FFmpeg

---

### Task 1: Add the marquee contract tests

**Files:**
- Create: `tests/video-marquee.test.mjs`
- Test: `tests/video-marquee.test.mjs`

- [ ] **Step 1: Write the failing static contract tests**

Create a Node test file that reads `index.html`, `assets/css/premium.css`, and `assets/js/playbold.js`; isolates the Press play section; and asserts the following exact contract:

```js
import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const html = fs.readFileSync(`${root}/index.html`, "utf8");
const css = fs.readFileSync(`${root}/assets/css/premium.css`, "utf8");
const js = fs.readFileSync(`${root}/assets/js/playbold.js`, "utf8");
const section = html.match(/<!-- press play -->([\s\S]*?)<!-- honest screen -->/)?.[1] ?? "";
const primary = section.match(/<div class="press-group">([\s\S]*?)<div class="press-group" data-marquee-copy>/)?.[1] ?? "";
const duplicate = section.match(/<div class="press-group" data-marquee-copy>([\s\S]*)/)?.[1] ?? "";

const videos = [
  "assets/vid/V01%20Everything%20Cheeko%20Does%20-%20video.mp4",
  "assets/updated-vids/V02%20Hand%20Them%20Cheeko%20-%20video.mp4",
  "assets/updated-vids/V03%20No%20Tantrum%20-%20video.mp4",
  "assets/updated-vids/V04%20Built%20to%20END%20-%20video.mp4",
  "assets/updated-vids/V06%20Five%20Minutes%20-%20video.mp4",
  "assets/updated-vids/V19%20Parent%20App%20-%20video.mp4",
];

test("Press play uses every unique local video and no Instagram embeds", () => {
  for (const src of videos) assert.match(primary, new RegExp(`src="${src}"`));
  assert.equal((primary.match(/<video\b/g) ?? []).length, videos.length);
  assert.doesNotMatch(section, /instagram\.com|<iframe\b/i);
});

test("each primary video card has a poster and labeled play button", () => {
  assert.equal((primary.match(/poster="[^"]+"/g) ?? []).length, videos.length);
  assert.equal((primary.match(/class="play-badge"/g) ?? []).length, videos.length);
  assert.equal((primary.match(/aria-label="Play [^"]+"/g) ?? []).length, videos.length);
  assert.doesNotMatch(section, /press-caption/);
});

test("the seamless duplicate remains fully playable", () => {
  assert.equal((duplicate.match(/<video\b/g) ?? []).length, videos.length);
  assert.equal((duplicate.match(/class="play-badge"/g) ?? []).length, videos.length);
  assert.doesNotMatch(duplicate, /<iframe\b/i);
});

test("marquee moves right to left without caption overlays", () => {
  assert.match(css, /@keyframes pressflow\{from\{transform:translateX\(0\)\}to\{transform:translateX\(calc\(-50% - var\(--press-gap\)\/2\)\)\}\}/);
  assert.doesNotMatch(css, /\.press-caption\{/);
});

test("playback is unmuted and failed play requests recover", () => {
  assert.match(js, /video\.muted = false/);
  assert.match(js, /playRequest\.catch/);
  assert.match(js, /badge\.classList\.remove\("hidden"\)/);
});
```

- [ ] **Step 2: Run the test and verify RED**

Run: `node --test tests/video-marquee.test.mjs`

Expected: failures for missing local video cards, remaining Instagram iframes, the old animation direction, and forced-muted playback.

### Task 2: Build the local-video markup and motion

**Files:**
- Use: `assets/updated-vids/V19 Parent App - thumbnail (1).jpg`
- Modify: `index.html:430-467`
- Modify: `assets/css/premium.css:123-142`
- Test: `tests/video-marquee.test.mjs`

- [ ] **Step 1: Verify the supplied Parent App poster**

Run:

```bash
ffprobe -v error -show_entries stream=codec_name,width,height "assets/updated-vids/V19 Parent App - thumbnail (1).jpg"
```

Expected: one 1080x1920 MJPEG image beside the Parent App MP4.

- [ ] **Step 2: Replace Instagram embeds with local video cards**

Update the section label to `Cheeko videos`. Build six `.press-card.press-film[data-film]` entries in each loop group, each containing its local `<video>` and a `.play-badge` button with a specific accessible label. Do not add visible caption overlays.

- [ ] **Step 3: Reverse and harden the marquee CSS**

Use a single media rule for every card's video or poster and reverse the keyframes:

```css
.press-film video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
@keyframes pressflow{from{transform:translateX(0)}to{transform:translateX(calc(-50% - var(--press-gap)/2))}}
```

Delete obsolete `.press-reel`, iframe, source, and open-link rules.

- [ ] **Step 4: Run the contract tests**

Run: `node --test tests/video-marquee.test.mjs`

Expected: markup and CSS tests pass; playback JavaScript test still fails.

### Task 3: Fix video playback and verify the complete feature

**Files:**
- Modify: `assets/js/playbold.js:31-54`
- Test: `tests/video-marquee.test.mjs`

- [ ] **Step 1: Implement recoverable, unmuted playback**

Within the existing `[data-film]` initializer, pause other videos before starting, set `video.muted = false`, add controls, and store `video.play()` as `playRequest`. Hide the badge in the `play` event only. If the promise rejects, remove the hidden state and keep controls available. On `ended`, remove controls, show the badge, reset `currentTime` to zero, and reload the poster frame.

- [ ] **Step 2: Run the complete static test suite**

Run: `node --test tests/video-marquee.test.mjs`

Expected: 5 tests pass, 0 fail.

- [ ] **Step 3: Run syntax and media verification**

Run:

```bash
node --check assets/js/playbold.js
for file in assets/vid/V01\ Everything\ Cheeko\ Does\ -\ video.mp4 assets/updated-vids/*-\ video.mp4; do ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height -of csv=p=0 "$file"; done
```

Expected: JavaScript syntax exits 0; every unique MP4 reports H.264 video at 1080x1920.

- [ ] **Step 4: Inspect the focused diff**

Run: `git diff --check && git diff -- index.html assets/css/premium.css assets/js/playbold.js tests/video-marquee.test.mjs`

Expected: no whitespace errors, no Instagram embed in the section, no unrelated changes introduced by this implementation.
