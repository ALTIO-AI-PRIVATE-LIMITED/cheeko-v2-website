// Screenshot a local HTML page (full page). Usage: node shot.mjs page.html out.png [width]
import { chromium } from './pw.mjs';
const [,, page, out, w = '1860'] = process.argv;
const b = await (await chromium()).launch(); const p = await b.newPage({ viewport: { width: +w, height: 800 } });
await p.goto('file://' + process.cwd() + '/' + page, { waitUntil: 'networkidle' });
await p.screenshot({ path: out, fullPage: true }); await b.close();
