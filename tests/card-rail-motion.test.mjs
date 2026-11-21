import assert from "node:assert/strict";
import test from "node:test";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { createCardRail, cardsPerView } = require("../assets/js/card-rail.js");

function makeRail(count = 10, width = 1100) {
  const handlers = new Map();
  const arrows = new Map();
  const cards = Array.from({ length: count }, (_, index) => ({
    index,
    dataset: {},
    offsetLeft: index * 110,
    classList: { add() {} },
    setAttribute() {},
    removeAttribute() {},
    cloneNode() { return { ...this }; },
  }));
  const track = {
    children: cards,
    style: { vars: {}, setProperty(name, value) { this.vars[name] = value; } },
    appendChild(card) { this.children.push(card); },
  };
  const wrap = {
    querySelectorAll() { return []; },
    querySelector(sel) {
      const key = sel.includes("prev") ? "prev" : "next";
      return { addEventListener(_, cb) { arrows.set(key, cb); } };
    },
  };
  const rail = {
    scrollLeft: 0,
    clientWidth: width,
    scrollWidth: width * 4,
    parentNode: wrap,
    querySelector() { return track; },
    addEventListener(name, callback) { handlers.set(name, callback); },
    contains() { return false; },
  };
  return { rail, track, handlers, arrows };
}

/* Runs queued animation frames until the animation finishes. */
function frameRunner() {
  let queue = [];
  let time = 0;
  return {
    requestFrame(cb) { queue.push(cb); },
    flush() {
      while (queue.length) {
        const q = queue; queue = []; time += 600;
        q.forEach((cb) => cb(time));
      }
    },
  };
}

test("cards are sized so only whole cards fit the row", () => {
  assert.equal(cardsPerView(1152), 6);
  assert.equal(cardsPerView(800), 5);
  assert.equal(cardsPerView(600), 3);
  assert.equal(cardsPerView(350), 2);
  const { rail, track } = makeRail(10, 1100);
  const frames = frameRunner();
  const api = createCardRail(rail, {
    requestFrame: frames.requestFrame, gap: () => 16,
    eventTarget: { addEventListener() {} }, pageHidden: () => false,
  });
  api.stop();
  assert.equal(track.style.vars["--fcw"], ((1100 - 16 * 5) / 6).toFixed(2) + "px");
  assert.equal(track.children.length, 20);
});

test("arrows move exactly one card and loop in both directions", () => {
  const { rail, arrows } = makeRail(10, 1100);
  const frames = frameRunner();
  const api = createCardRail(rail, {
    requestFrame: frames.requestFrame, gap: () => 16,
    eventTarget: { addEventListener() {} }, pageHidden: () => false,
  });
  api.stop();
  const step = (1100 - 16 * 5) / 6 + 16;
  arrows.get("next")(); frames.flush();
  assert.ok(Math.abs(rail.scrollLeft - step) < 0.01);
  arrows.get("prev")(); frames.flush();
  assert.ok(Math.abs(rail.scrollLeft) < 0.01);
  arrows.get("prev")(); frames.flush();
  assert.ok(Math.abs(rail.scrollLeft - step * 9) < 0.01);
  arrows.get("next")(); frames.flush();
  assert.ok(Math.abs(rail.scrollLeft) < 0.01, "wraps back to the first card");
});

test("autoplay advances only when nobody is interacting; reduced motion leaves a manual row", () => {
  const { rail, handlers } = makeRail(10, 1100);
  const frames = frameRunner();
  let time = 0;
  const api = createCardRail(rail, {
    requestFrame: frames.requestFrame, gap: () => 16, now: () => time,
    eventTarget: { addEventListener() {} }, pageHidden: () => false,
  });
  api.stop();
  handlers.get("mouseenter")();
  api.tick(); frames.flush();
  assert.equal(rail.scrollLeft, 0);
  handlers.get("mouseleave")();
  api.tick(); frames.flush();
  assert.ok(rail.scrollLeft > 0);

  const reduced = makeRail(10, 1100);
  const r = createCardRail(reduced.rail, { reducedMotion: true, gap: () => 16, eventTarget: { addEventListener() {} } });
  r.stop();
  assert.equal(reduced.track.children.length, 10);
});
