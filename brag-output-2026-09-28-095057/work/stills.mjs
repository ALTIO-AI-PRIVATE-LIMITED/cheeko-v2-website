import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const times = process.argv.slice(2).map(Number);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('file://' + process.cwd() + '/compose.html', { waitUntil: 'networkidle' });
await p.evaluate(() => window.ready);
for (const t of times) {
  await p.evaluate(t => window.render(t), t);
  await p.screenshot({ path: `still-${t.toFixed(2)}.png` });
}
await b.close();
