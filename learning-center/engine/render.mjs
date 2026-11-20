// Render one Learning Center video at 2x (592x480) with its audio into ../<slug>/raw2x_L<n>.mp4.
// Usage (inside engine/): node render.mjs <slug> <level> <seconds> [scale=2]
import { chromium } from './pw.mjs';
import { spawn } from 'child_process';
const [,, SLUG, LV, secs, SC = '2'] = process.argv;
const FPS = 30, N = Math.round(FPS * Number(secs)), OUT = `../${SLUG}/raw2x_L${LV}.mp4`;
const ff = spawn('ffmpeg', ['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-i',`../${SLUG}/music-final_L${LV}.wav`,
  '-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',OUT], { stdio: ['pipe','inherit','inherit'] });
const b = await (await chromium()).launch();
const p = await b.newPage({ viewport: { width: 296, height: 240 }, deviceScaleFactor: +SC });
const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
await p.goto(`file://${process.cwd()}/compose.html?idea=${SLUG}&level=${LV}`, { waitUntil: 'networkidle' });
await p.evaluate(() => window.ready);
for (let i = 0; i < N; i++) {
  await p.evaluate(t => window.render(t), i / FPS);
  const buf = await p.screenshot({ type: 'jpeg', quality: 93 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
}
ff.stdin.end(); await b.close(); await new Promise(r => ff.on('close', r));
console.log('done', OUT, N, 'frames', errs.length ? 'ERRORS ' + errs.slice(0, 3).join(' | ') : '');
