// Render every Learning shelf thumbnail from specs.json at exactly 208 x 116 (JPEG), next to its video.
// Usage (from thumbs/): /usr/bin/python3 thumb_specs.py && node make_thumbs.mjs
import { chromium } from '../engine/pw.mjs';
import { readFileSync } from 'fs';
const specs = JSON.parse(readFileSync('specs.json', 'utf8'));
const b = await (await chromium()).launch();
const p = await b.newPage({ viewport: { width: 208, height: 116 }, deviceScaleFactor: 1 });
for (const s of specs) {
  await p.goto(`file://${process.cwd()}/thumb.html#` + encodeURIComponent(JSON.stringify(s)), { waitUntil: 'networkidle' });
  await p.reload({ waitUntil: 'networkidle' });                 // the page reads its spec from the hash on load
  await p.evaluate(() => window.ready);
  await p.screenshot({ path: s.out, type: 'jpeg', quality: 92 });
  console.log(s.out.split('/').pop());
}
await b.close();
