// Renders the 16:9 side panels (one per chapter) and the 16:9 YouTube thumbnail for stitch_series.py.
// usage: node frames.mjs <config.json> <out dir>
import { readFileSync } from 'fs';
import { chromium } from '../../../cheeko-v2-website/brag-output-2026-09-28-reel/work/pw.mjs';
const [cfgPath, out] = process.argv.slice(2), C = JSON.parse(readFileSync(cfgPath, 'utf8'));
const page = await (await (await chromium()).launch()).newPage({ viewport: { width: 1920, height: 1080 } });
const shot = async (spec, path, type = 'png') => {
  await page.goto('file://' + new URL('series_frame.html', import.meta.url).pathname + '#' + encodeURIComponent(JSON.stringify(spec)), { waitUntil: 'networkidle' });
  await page.reload({ waitUntil: 'networkidle' }); await page.evaluate(() => window.ready);
  await page.screenshot({ path, type, ...(type === 'jpeg' ? { quality: 92 } : {}) });
};
for (let k = 0; k < C.chapters.length; k++)
  await shot({ mode: 'chapter', title: C.title, sub: C.sub, pill: C.pill, chapters: C.chapters, cur: k, hi: C.hi }, `${out}/ch_${k}.png`);
await shot({ mode: 'thumb', hook: C.hook, pill: C.thumbPill, shots: C.thumbShots, hi: C.hi }, `${out}/thumbnail-16x9.jpg`, 'jpeg');
process.exit(0);
