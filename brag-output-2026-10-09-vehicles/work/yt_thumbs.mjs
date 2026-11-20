// Render the four YouTube thumbnails (1280x720 JPG) from yt_thumb.html.
import { chromium } from './pw.mjs';
const b = await (await chromium()).launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
const out = { v30: '../../brag-output-2026-10-08-ocean-animals/youtube/Cheeko_V30_Ocean_Animals_10_thumbnail.jpg',
  l1: '../youtube/Cheeko_V31.1_Guess_the_Vehicle_Level_1_thumbnail.jpg', l2: '../youtube/Cheeko_V31.2_Guess_the_Vehicle_Level_2_thumbnail.jpg', l3: '../youtube/Cheeko_V31.3_Guess_the_Vehicle_Level_3_thumbnail.jpg' };
for (const [v, f] of Object.entries(out)) {
  await p.goto('file://' + process.cwd() + '/yt_thumb.html?v=' + v, { waitUntil: 'networkidle' }); await p.evaluate(() => window.ready);
  await p.screenshot({ path: f, type: 'jpeg', quality: 90 });
}
await b.close(); console.log('ok');
