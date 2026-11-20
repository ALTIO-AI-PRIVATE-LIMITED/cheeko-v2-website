// Save window.CUES from compose.html to cues.json (run inside a video's work/ folder).
import { chromium } from './pw.mjs';
import { writeFileSync } from 'fs';
const b = await (await chromium()).launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('file://' + process.cwd() + '/compose.html', { waitUntil: 'networkidle' }); await p.evaluate(() => window.ready);
writeFileSync('cues.json', JSON.stringify(await p.evaluate(() => window.CUES), null, 1)); await b.close(); console.log('cues.json');
