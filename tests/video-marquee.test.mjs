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
const cdnBase = "https://dsmzc13oafp54.cloudfront.net/website-media/cheekoai.in/";

const videos = [
  "v01-everything-cheeko-does.mp4",
  "v02-hand-them-cheeko.mp4",
  "v03-no-tantrum.mp4",
  "v04-built-to-end.mp4",
  "v06-five-minutes.mp4",
  "v19-parent-app.mp4",
].map((name) => cdnBase + name);
const posters = [
  "v01-everything-cheeko-does-thumbnail.jpg",
  "v02-hand-them-cheeko-thumbnail.jpg",
  "v03-no-tantrum-thumbnail.jpg",
  "v04-built-to-end-thumbnail.jpg",
  "v06-five-minutes-thumbnail.jpg",
  "v19-parent-app-thumbnail.jpg",
].map((name) => cdnBase + name);

test("all seven video and thumbnail pairs use direct CloudFront URLs", () => {
  const imagineVideo = `${cdnBase}v12-imagine.mp4`;
  const imaginePoster = `${cdnBase}v12-imagine-thumbnail.jpg`;
  assert.ok(html.includes(`<img src="${imaginePoster}" alt=""`));
  assert.ok(html.includes(`<video id="vplayer" src="${imagineVideo}" poster="${imaginePoster}"`));
  assert.doesNotMatch(html, /assets\/videos\/|media-cdn\.js/);
});

test("Press play uses every unique CDN video and no Instagram embeds", () => {
  for (const src of videos) assert.ok(primary.includes(`src="${src}"`));
  assert.equal((primary.match(/<video\b/g) ?? []).length, videos.length);
  assert.doesNotMatch(section, /instagram\.com|<iframe\b/i);
});

test("each primary video card has the requested poster and a labeled play button", () => {
  for (const poster of posters) assert.ok(primary.includes(`poster="${poster}"`));
  assert.equal((primary.match(/class="play-badge"/g) ?? []).length, videos.length);
  assert.equal((primary.match(/aria-label="Play [^"]+"/g) ?? []).length, videos.length);
  assert.doesNotMatch(section, /press-caption/);
});

test("the seamless duplicate remains fully playable", () => {
  for (const src of videos) assert.ok(duplicate.includes(`src="${src}"`));
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

test("CDN playback is unmuted and failed play requests recover", () => {
  assert.match(js, /video\.muted = false/);
  assert.match(js, /video\.addEventListener\("playing"/);
  assert.doesNotMatch(js, /video\.addEventListener\("play"/);
  assert.match(js, /badge\.classList\.remove\("hidden"\)/);
  assert.match(js, /badge\.addEventListener\("click"[\s\S]*?track\.classList\.add\("paused"\)[\s\S]*?video\.play\(\)/);
  assert.match(js, /playRequest\.catch\([\s\S]*?video\.load\(\)/);
  assert.match(js, /vplayer\.play\(\)/);
  assert.doesNotMatch(js, /CheekoMediaCdn/);
  assert.match(js, /video\.addEventListener\("ended"[\s\S]*?track\.classList\.remove\("paused"\)/);
});

test("updated marquee assets use fresh cache versions", () => {
  const cssVersion = html.match(/assets\/css\/premium\.css\?v=(\d+)/);
  const scriptVersion = html.match(/assets\/js\/playbold\.js\?v=(\d+)/);
  assert.ok(cssVersion && Number(cssVersion[1]) >= 66);
  assert.ok(scriptVersion && Number(scriptVersion[1]) >= 12);
});
