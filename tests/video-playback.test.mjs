import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const script = fs.readFileSync(fileURLToPath(new URL("../assets/js/playbold.js", import.meta.url)), "utf8");

function classes() {
  const values = new Set();
  return {
    add(name) { values.add(name); },
    remove(name) { values.delete(name); },
    contains(name) { return values.has(name); },
  };
}

function setupFilms() {
  const track = { classList: classes() };
  const frames = Array.from({ length: 3 }, () => {
    const listeners = new Map();
    const attributes = new Set();
    const video = {
      paused: true,
      ended: false,
      currentTime: 0,
      muted: true,
      addEventListener(type, listener) { listeners.set(type, listener); },
      setAttribute(name) { attributes.add(name); },
      removeAttribute(name) { attributes.delete(name); },
      hasAttribute(name) { return attributes.has(name); },
      play() {
        this.paused = false;
        listeners.get("playing")();
        return Promise.resolve();
      },
      pause() {
        if (this.paused) return;
        this.paused = true;
        listeners.get("pause")();
      },
      load() {},
    };
    const badge = {
      classList: classes(),
      addEventListener(type, listener) { listeners.set(`badge:${type}`, listener); },
      click() { listeners.get("badge:click")(); },
    };
    return {
      video,
      badge,
      querySelector(selector) { return selector === "video" ? video : badge; },
      closest() { return track; },
    };
  });
  const document = {
    querySelectorAll(selector) { return selector === "[data-film]" ? frames : []; },
    querySelector() { return null; },
    getElementById() { return null; },
  };
  const window = { matchMedia() { return { matches: true }; } };
  vm.runInNewContext(script, { document, window, Date });
  return { frames, track };
}

test("starting another rail video pauses the previous one and restores its orange play button", () => {
  const { frames, track } = setupFilms();
  const [first, second] = frames;

  first.badge.click();
  assert.equal(first.badge.classList.contains("hidden"), true);
  second.badge.click();

  assert.equal(first.video.paused, true);
  assert.equal(first.badge.classList.contains("hidden"), false);
  assert.equal(first.video.hasAttribute("controls"), false);
  assert.equal(second.video.paused, false);
  assert.equal(second.badge.classList.contains("hidden"), true);
  assert.equal(track.classList.contains("paused"), true);
});

test("native video controls cannot leave two rail videos playing", () => {
  const { frames } = setupFilms();
  const [first, second] = frames;

  first.badge.click();
  second.video.play();

  assert.equal(first.video.paused, true);
  assert.equal(first.badge.classList.contains("hidden"), false);
  assert.equal(second.video.paused, false);
});

test("pausing a rail video restores its orange play button", () => {
  const { frames, track } = setupFilms();
  const first = frames[0];

  first.badge.click();
  first.video.pause();

  assert.equal(first.badge.classList.contains("hidden"), false);
  assert.equal(first.video.hasAttribute("controls"), false);
  assert.equal(track.classList.contains("paused"), false);
});
