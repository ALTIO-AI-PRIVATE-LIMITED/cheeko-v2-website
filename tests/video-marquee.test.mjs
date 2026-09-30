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
const posters = [
  "assets/img/V01%20Everything%20Cheeko%20Does%20-%20thumbnail.jpg",
  "assets/updated-vids/V02%20Hand%20Them%20Cheeko%20-%20thumbnail.jpg",
  "assets/updated-vids/V03%20No%20Tantrum%20-%20thumbnail.jpg",
  "assets/updated-vids/V04%20Built%20to%20END%20-%20thumbnail.jpg",
  "assets/updated-vids/V06%20Five%20Minutes%20-%20thumbnail.jpg",
  "assets/updated-vids/V19%20Parent%20App%20-%20thumbnail%20%281%29.jpg",
];

test("Press play uses every unique local video and no Instagram embeds", () => {
  for (const src of videos) assert.match(primary, new RegExp(`src="${src}"`));
  assert.equal((primary.match(/<video\b/g) ?? []).length, videos.length);
  assert.doesNotMatch(section, /instagram\.com|<iframe\b/i);
});

test("each primary video card has the requested poster and a labeled play button", () => {
  for (const poster of posters) assert.match(primary, new RegExp(`poster="${poster}"`));
  assert.equal((primary.match(/class="play-badge"/g) ?? []).length, videos.length);
  assert.equal((primary.match(/aria-label="Play [^"]+"/g) ?? []).length, videos.length);
  assert.doesNotMatch(section, /press-caption/);
});

test("the seamless duplicate remains fully playable", () => {
  for (const src of videos) assert.match(duplicate, new RegExp(`src="${src}"`));
  assert.equal((duplicate.match(/<video\b/g) ?? []).length, videos.length);
  assert.equal((duplicate.match(/class="play-badge"/g) ?? []).length, videos.length);
  assert.equal((duplicate.match(/aria-label="Play [^"]+"/g) ?? []).length, videos.length);
  assert.doesNotMatch(duplicate, /<iframe\b/i);
});

test("video cards have a visible manual scroll control as well as auto movement", () => {
  assert.match(section, /class="press-marquee"[^>]*role="region"[^>]*tabindex="0"/);
  assert.match(section, /<input[^>]*class="press-scroll"[^>]*type="range"[^>]*aria-label="Scroll Cheeko videos"/);
  assert.match(css, /\.press-marquee\{[^}]*overflow-x:auto/);
  assert.match(css, /\.press-scroll\{/);
  assert.doesNotMatch(css, /@keyframes pressflow/);
  assert.match(html, /press-rail\.js\?v=\d+" defer><\/script>\s*<script src="assets\/js\/playbold\.js/);
  assert.doesNotMatch(css, /\.press-caption\{/);
});

test("the Imagine rail omits the school-bag drawing from both matching halves", () => {
  const strip = html.match(/<div class="imstrip"[\s\S]*?<\/div><\/div>/)?.[0] ?? "";
  const sources = [...strip.matchAll(/<img src="([^"]+)"/g)].map((match) => match[1]);
  assert.equal(sources.length, 22);
  assert.deepEqual(sources.slice(0, 11), sources.slice(11));
  assert.ok(sources.every((source) => !source.endsWith("im-15.jpg")));
});

test("playback is unmuted and failed play requests recover", () => {
  assert.match(js, /video\.muted = false/);
  assert.match(js, /playRequest\.catch/);
  assert.match(js, /video\.addEventListener\("playing"/);
  assert.doesNotMatch(js, /video\.addEventListener\("play"/);
  assert.match(js, /badge\.classList\.remove\("hidden"\)/);
  assert.match(js, /playRequest\.catch\([\s\S]*?video\.load\(\)/);
  assert.match(js, /badge\.addEventListener\("click"[\s\S]*?track\.classList\.add\("paused"\)[\s\S]*?video\.play\(\)/);
  assert.match(js, /video\.addEventListener\("ended"[\s\S]*?track\.classList\.remove\("paused"\)/);
});

test("updated marquee assets use fresh cache versions", () => {
  const cssVersion = html.match(/assets\/css\/premium\.css\?v=(\d+)/);
  const scriptVersion = html.match(/assets\/js\/playbold\.js\?v=(\d+)/);
  assert.ok(cssVersion && Number(cssVersion[1]) >= 66);
  assert.ok(scriptVersion && Number(scriptVersion[1]) >= 12);
});
