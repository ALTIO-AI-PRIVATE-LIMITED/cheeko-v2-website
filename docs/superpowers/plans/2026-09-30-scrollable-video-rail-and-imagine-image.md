# Scrollable Video Rail and Imagine Image Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Keep the homepage video cards moving automatically while allowing manual horizontal scrolling, and remove the school-bag picture from the Imagine rail.

**Architecture:** Use the video rail's native `scrollLeft` instead of CSS transform animation. Add a visible range control synchronized with the rail. Keep repeated video groups for seamless looping and pause automatic motion during interaction or playback. Remove both matching Imagine figures from the duplicated image sequence.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Node's built-in test runner.

---

### Task 1: Video-rail behavior

**Files:** `tests/video-marquee.test.mjs`, `tests/press-rail.test.mjs`, `assets/js/press-rail.js`, `assets/js/playbold.js`, `assets/css/premium.css`, `index.html`.

- [x] Add tests requiring a visible range control, native horizontal overflow, scroll-position-based animation, and pause during video playback and reduced motion.
- [x] Run `node --test tests/video-marquee.test.mjs`; confirm these tests fail because the new behavior is missing.
- [x] Replace `.press-track` transform animation with native horizontal overflow in `.press-marquee`; style `.press-scroll` as an always-visible control.
- [x] Add the range input after `.press-marquee` in `index.html` with an accessible label.
- [x] Initialize the rail in a focused `press-rail.js` loaded before `playbold.js`: create a third repeated group, start at the middle copy, advance `scrollLeft` with `requestAnimationFrame`, wrap at a half-group boundary, synchronize range input, and pause during user interaction/video playback. With reduced motion, omit the auto-advance and keep manual scrolling.
- [x] Run `node --test tests/video-marquee.test.mjs`; confirm all assertions pass.

### Task 2: Imagine rail content

**Files:** `tests/video-marquee.test.mjs`, `index.html`.

- [x] Add a test that the `.imtrack` image source list has no `im-15.jpg` and its two halves are identical.
- [x] Run `node --test tests/video-marquee.test.mjs`; confirm the new Imagine assertion fails.
- [x] Remove both school-bag `<figure>` elements from `.imtrack`, retaining all other figures and the image asset.
- [x] Run `node --test tests/video-marquee.test.mjs`; confirm the Imagine assertion passes.

### Task 3: Regression verification

**Files:** `index.html`, `assets/css/premium.css`, `assets/js/playbold.js`, `tests/video-marquee.test.mjs`.

- [x] Run `node --test tests/*.test.mjs` and `python3 -m unittest discover -s tests`.
- [x] Run `node --check assets/js/playbold.js` and inspect `git diff --check` plus the focused diff.
- [x] Confirm both videos and the visible range control remain functional at narrow widths and with reduced-motion styles by reviewing the responsive rules.
