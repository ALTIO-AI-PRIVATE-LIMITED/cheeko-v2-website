import assert from "node:assert/strict";
import { createRequire } from "node:module";
import test from "node:test";

const require = createRequire(import.meta.url);
const { createPressRail } = require("../assets/js/press-rail.js");

function emitter(fields = {}) {
  const listeners = new Map();
  return {
    ...fields,
    addEventListener(name, handler) {
      if (!listeners.has(name)) listeners.set(name, []);
      listeners.get(name).push(handler);
    },
    emit(name, event = {}) {
      (listeners.get(name) ?? []).forEach((handler) => handler(event));
    },
  };
}

function fixture(reducedMotion = false) {
  const frames = [];
  const target = emitter();
  let clock = 0;
  let playing = false;
  const track = {
    children: [],
    classList: { contains(name) { return name === "paused" && playing; } },
    insertBefore(node, before) { this.children.splice(this.children.indexOf(before), 0, node); },
  };
  function group() {
    const item = { cloneNode() { return group(); }, setAttribute(name, value) { this[name] = value; } };
    Object.defineProperty(item, "offsetLeft", { get() { return track.children.indexOf(item) * 1000; } });
    return item;
  }
  track.children.push(group(), group());
  const rail = emitter({
    scrollLeft: 0,
    clientWidth: 400,
    get scrollWidth() { return track.children.length * 1000; },
    querySelector() { return track; },
    contains() { return false; },
  });
  const range = emitter({ value: "500", contains() { return false; } });
  createPressRail(rail, range, {
    reducedMotion,
    requestFrame(callback) { frames.push(callback); },
    now() { return clock; },
    eventTarget: target,
    pageHidden() { return false; },
  });
  return {
    rail, range, track, frames, target,
    setClock(value) { clock = value; },
    setPlaying(value) { playing = value; },
    frame(value) { assert.ok(frames.length); frames.shift()(value); },
  };
}

test("the video rail auto-advances through repeated cards and wraps seamlessly", () => {
  const app = fixture();
  assert.equal(app.track.children.length, 3);
  assert.equal(app.rail.scrollLeft, 1000);
  app.frame(0);
  app.frame(50);
  assert.ok(app.rail.scrollLeft > 1000);
  app.rail.scrollLeft = 1499;
  app.frame(100);
  assert.ok(app.rail.scrollLeft >= 500 && app.rail.scrollLeft < 600);
});

test("the visible slider scrolls manually and auto motion resumes after interaction", () => {
  const app = fixture();
  app.range.value = "750";
  app.range.emit("input");
  assert.equal(app.rail.scrollLeft, 1250);
  app.frame(0);
  app.setClock(1000);
  app.frame(50);
  assert.equal(app.rail.scrollLeft, 1250);
  app.setClock(2100);
  app.frame(100);
  assert.ok(app.rail.scrollLeft > 1250);
});

test("playing video pauses automatic scrolling", () => {
  const app = fixture();
  app.frame(0);
  app.setPlaying(true);
  app.frame(50);
  assert.equal(app.rail.scrollLeft, 1000);
  app.setPlaying(false);
  app.frame(100);
  assert.ok(app.rail.scrollLeft > 1000);
});

test("pointer release elsewhere does not pause the video rail", () => {
  const app = fixture();
  app.frame(0);
  app.target.emit("pointerup");
  app.frame(50);
  assert.ok(app.rail.scrollLeft > 1000);
});

test("dragging the rail holds auto motion until after release", () => {
  const app = fixture();
  app.rail.emit("pointerdown");
  app.frame(0);
  app.setClock(2500);
  app.frame(50);
  assert.equal(app.rail.scrollLeft, 1000);
  app.target.emit("pointerup");
  app.setClock(4600);
  app.frame(100);
  assert.ok(app.rail.scrollLeft > 1000);
});

test("reduced motion keeps manual scrolling without animation or extra clones", () => {
  const app = fixture(true);
  assert.equal(app.track.children.length, 2);
  assert.equal(app.frames.length, 0);
  app.range.value = "500";
  app.range.emit("input");
  assert.equal(app.rail.scrollLeft, 800);
});
