import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const html = fs.readFileSync(`${root}/index.html`, "utf8");

const cards = {
  clever: "assets/img/updated-cards/clever%20little%20tales.png",
  playAndSing: "assets/img/updated-cards/play%20and%20sing%20along%20.png",
  talesOfKindness: "assets/img/updated-cards/tales%20of%20kindness.png",
  raviAndNila: "assets/img/updated-cards/ravi%20and%20nila.png",
};

function imageSources(fragment) {
  return [...fragment.matchAll(/<img\b[^>]*\bsrc="([^"]+)"/g)].map((match) => match[1]);
}

test("card fans preserve their semantic card order", () => {
  const cardFan = html.match(/<span class="cardfan">([\s\S]*?)<\/span>/)?.[1] ?? "";
  const howFan = html.match(/<span class="hb-fan">([\s\S]*?)<\/span>/)?.[1] ?? "";

  assert.deepEqual(imageSources(cardFan), [cards.clever, cards.talesOfKindness, cards.raviAndNila]);
  assert.deepEqual(imageSources(howFan), [cards.clever, cards.playAndSing, cards.talesOfKindness]);
});

test("the insert sequence consistently uses Tales of Kindness", () => {
  assert.match(html, new RegExp(`<img class="hb-drop" src="${cards.talesOfKindness}"`));
  assert.match(html, new RegExp(`<img class="hb-behind" src="${cards.talesOfKindness}"`));
  assert.match(html, /<span class="hb-chip"><i>✦<\/i> Tales of Kindness<\/span>/);
});

test("old card artwork and stale card names are gone from the homepage", () => {
  assert.doesNotMatch(html, /assets\/img\/live\/card-(?:storytime|clever|playsing|ravi)\.jpg/);
  assert.doesNotMatch(html, /Storytime Adventures|Ravi's Wild Journey/);
  assert.match(html, /alt="The Tales of Kindness card"/);
  assert.match(html, /alt="The Ravi and Nila card"/);
});
