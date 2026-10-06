# Meet the Device Animation Implementation Plan

> **For agentic workers:** Execute inline in this session; no subagents are requested. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the home page's static device image with the supplied working animation.

**Architecture:** Keep the provided animation's CSS, JavaScript and WebP assets inside `assets/cheeko-device-animation/`. Embed the supplied widget markup directly into the existing `#device` section, with image paths rebased from `img/` to `assets/cheeko-device-animation/img/`. Load its font families and local CSS/JS from `index.html`.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Node's built-in test runner.

---

### Task 1: Assert the home page uses the animation

**Files:** Create `tests/device-animation.test.mjs`.

- [x] Write a Node test that reads `index.html`, extracts the `#device` section, asserts it contains `id="devanim"`, a `.dm-knob` button, six `.dm-scr` images, all seven labels, and no `hero-image-labels.png` reference there.
- [x] Verify the page references `assets/cheeko-device-animation/device-anim.css` and `assets/cheeko-device-animation/device-anim.js`, and verify every referenced widget image exists under the supplied `img/` directory.
- [x] Run `node --test tests/device-animation.test.mjs` and observe the expected failure on the current static image.

### Task 2: Integrate the supplied markup

**Files:** Modify `index.html` near lines 19, 120, and the closing scripts.

- [x] Add `Gochi Hand` and `Patrick Hand` to the existing Google Fonts request; add `<link rel="stylesheet" href="assets/cheeko-device-animation/device-anim.css?v=1" />` after `premium.css`.
- [x] Replace the one-image `.devmap` with the exact `snippet.html` widget structure, retaining its `#devanim`, screen ordering, `data-*` arrow coordinates, labels and button. Prefix all `img/` URLs with `assets/cheeko-device-animation/`.
- [x] Load `<script src="assets/cheeko-device-animation/device-anim.js?v=1" defer></script>` with the other bottom scripts.
- [x] Run the focused test and expect it to pass.

### Task 3: Verify behavior and regressions

**Files:** Test `index.html` and supplied animation files; modify only if a verification failure identifies a defect.

- [x] Run `node --check assets/cheeko-device-animation/device-anim.js` and `node --test tests/*.test.mjs`.
- [x] Run `git diff --check` and inspect the `#device` section diff for unintended changes.
- [x] Attempt browser verification; headless Chrome exited 134 in this sandbox, so desktop/mobile visual checks remain unverified. Runtime dial and visibility behavior were exercised by a Node VM test.
