// Render compose.html at 2x (592x480) and encode with music-final.wav into raw2x.mp4.
// Usage (inside work/): node render.mjs <ffmpeg> <seconds> [fps=30]
import { chromium } from './pw.mjs';
import { spawn } from 'child_process';
const [,, FF, secs, fps = '30'] = process.argv;
const FPS = +fps, N = Math.round(FPS * Number(secs));
const ff = spawn(FF, ['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-',
  '-i','music-final.wav','-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p',
  '-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','raw2x.mp4'], { stdio: ['pipe','inherit','inherit'] });
const b = await (await chromium()).launch();
const p = await b.newPage({ viewport: { width: 296, height: 240 }, deviceScaleFactor: 2 });
p.on('pageerror', e => console.error('page error:', e.message));
await p.goto('file://' + process.cwd() + '/compose.html', { waitUntil: 'networkidle' });
await p.evaluate(() => window.ready);
for (let i = 0; i < N; i++) {
  await p.evaluate(t => window.render(t), i / FPS);
  const buf = await p.screenshot({ type: 'jpeg', quality: 95 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
}
ff.stdin.end(); await b.close();
await new Promise(r => ff.on('close', r)); console.log('done', N, 'frames');
