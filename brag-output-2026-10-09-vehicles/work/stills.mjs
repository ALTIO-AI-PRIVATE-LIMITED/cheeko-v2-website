// Save still-<t>.png (2x, 592x480) for each time given. Usage (inside work/): LEVEL=1 node stills.mjs 0.5 3.2 ...
import { chromium } from './pw.mjs';
const times = process.argv.slice(2).map(Number);
const b = await (await chromium()).launch();
const p = await b.newPage({ viewport: { width: 296, height: 240 }, deviceScaleFactor: 2 });
p.on('pageerror', e => console.error('page error:', e.message));
await p.goto('file://' + process.cwd() + '/compose.html?level=' + (process.env.LEVEL || '1'), { waitUntil: 'networkidle' });
await p.evaluate(() => window.ready);
for (const t of times) { await p.evaluate(t => window.render(t), t); await p.screenshot({ path: `still-${t.toFixed(2)}.png` }); }
await b.close();
