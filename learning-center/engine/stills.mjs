// Save stills (2x) of one video at the given times: node stills.mjs <slug> <level> <outprefix> t1 t2 ...
import { chromium } from './pw.mjs';
const [,, SLUG, LV, PRE, ...ts] = process.argv;
const b = await (await chromium()).launch(); const p = await b.newPage({ viewport: { width: 296, height: 240 }, deviceScaleFactor: 2 });
const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
await p.goto(`file://${process.cwd()}/compose.html?idea=${SLUG}&level=${LV}`, { waitUntil: 'networkidle' }); await p.evaluate(() => window.ready);
for (const t of ts) { await p.evaluate(t => window.render(t), +t); await p.screenshot({ path: `${PRE}${(+t).toFixed(2).padStart(7, '0')}.png` }); }
await b.close(); if (errs.length) console.log('ERRORS', errs.slice(0, 5));
