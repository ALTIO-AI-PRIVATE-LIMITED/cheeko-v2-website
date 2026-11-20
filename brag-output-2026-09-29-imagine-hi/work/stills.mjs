// Save still-<t>.png for each time given, to check layouts before a full render.
// Usage (inside work/): node stills.mjs 0.5 3.2 6.0 ...   (set W/H env vars for non-vertical)
import { chromium } from './pw.mjs';
const times = process.argv.slice(2).map(Number);
const b = await (await chromium()).launch();
const p = await b.newPage({ viewport: { width: +(process.env.W || 1080), height: +(process.env.H || 1920) } });
await p.goto('file://' + process.cwd() + '/compose.html', { waitUntil: 'networkidle' });
await p.evaluate(() => window.ready);
for (const t of times) {
  await p.evaluate(t => window.render(t), t);
  await p.screenshot({ path: `still-${t.toFixed(2)}.png` });
}
await b.close();
