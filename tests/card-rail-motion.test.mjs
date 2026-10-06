import assert from "node:assert/strict";
import test from "node:test";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { createCardRail } = require("../assets/js/card-rail.js");

function makeRail() {
  const handlers = new Map();
  const cards = Array.from({ length: 3 }, (_, index) => ({
    index,
    dataset: {},
    offsetLeft: index * 110,
    classList: { add() {} },
    setAttribute() {},
    removeAttribute() {},
    cloneNode() { return { ...this, offsetLeft: (index + 3) * 110 }; },
  }));
  const track = {
    children: cards,
    appendChild(card) { this.children.push(card); },
  };
  const rail = {
    scrollLeft: 0,
    querySelector() { return track; },
    addEventListener(name, callback) { handlers.set(name, callback); },
    contains() { return false; },
  };
  return { rail, track, handlers };
}

test("cards move right to left and wrap to the same visual position", () => {
  const { rail, track } = makeRail();
  let frame;
  let time = 0;
  createCardRail(rail, {
    requestFrame(callback) { frame = callback; },
    now() { return time; },
    eventTarget: { addEventListener() {} },
    pageHidden() { return false; },
  });
  assert.equal(track.children.length, 6);
  frame(0);
  frame(1000);
  assert.ok(rail.scrollLeft > 0);
  rail.scrollLeft = 329;
  frame(1100);
  assert.ok(rail.scrollLeft >= 0 && rail.scrollLeft < 30);
});

test("interaction pauses movement and reduced motion leaves a manual row", () => {
  const { rail, track, handlers } = makeRail();
  let frame;
  let time = 0;
  createCardRail(rail, {
    requestFrame(callback) { frame = callback; },
    now() { return time; },
    eventTarget: { addEventListener() {} },
    pageHidden() { return false; },
  });
  frame(0);
  handlers.get("mouseenter")();
  frame(1000);
  assert.equal(rail.scrollLeft, 0);
  handlers.get("mouseleave")();
  time = 3000;
  frame(2000);
  assert.ok(rail.scrollLeft > 0);

  const reduced = makeRail();
  createCardRail(reduced.rail, { reducedMotion: true });
  assert.equal(reduced.track.children.length, 3);
});
