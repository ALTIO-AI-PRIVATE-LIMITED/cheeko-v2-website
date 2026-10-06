import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const html = fs.readFileSync(`${root}/index.html`, "utf8");
const css = fs.readFileSync(`${root}/assets/css/premium.css`, "utf8");
const section = html.match(/<div class="decktrain"[\s\S]*?<\/div>\s*<p class="rv" style="text-align:center;margin-top:18px;"/)?.[0] ?? "";

test("the card carousel has ten unique cards without visible inventory numbers or flip prompts", () => {
  assert.equal((section.match(/class="fcardw rv"/g) ?? []).length, 10);
  assert.doesNotMatch(section, /aria-hidden="true"|class="cardno"|N&ordm;|TAP TO FLIP BACK/);
  assert.equal((section.match(/class="fface back"/g) ?? []).length, 10);
});

test("the card row supports manual scrolling and right-to-left auto movement", () => {
  assert.match(css, /\.decktrain\{[^}]*overflow-x:auto/);
  assert.match(css, /\.decktrain::\-webkit-scrollbar\{display:none\}/);
  assert.match(css, /\.decktrain\{[^}]*scrollbar-width:none/);
  assert.doesNotMatch(css, /animation:decktrain|@keyframes decktrain/);
  assert.match(html, /card-rail\.js\?v=\d+" defer><\/script>/);
  assert.match(css, /@media \(hover:hover\) and \(pointer:fine\)\{\.fcardw:hover \.flip/);
  assert.match(css, /\.fcardw\.flipped \.flip\{transform:rotateY\(180deg\)\}/);
});
