// Render compose.html frame by frame and encode with music-final.wav into raw.mp4.
// Usage (run inside the work/ folder): node render.mjs <ffmpeg> <seconds> [width] [height]
import { chromium } from './pw.mjs';
import { spawn } from 'child_process';
const [,, FF, secs, w = '1080', h = '1920'] = process.argv;
const FPS = 30, N = Math.round(FPS * Number(secs));
const ff = spawn(FF, ['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-',
  '-i','music-final.wav','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-profile:v','high',
  '-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','raw.mp4'], { stdio: ['pipe','inherit','inherit'] });
const b = await (await chromium()).launch();
const p = await b.newPage({ viewport: { width: +w, height: +h } });
await p.goto('file://' + process.cwd() + '/compose.html', { waitUntil: 'networkidle' });
await p.evaluate(() => window.ready);
for (let i = 0; i < N; i++) {
  await p.evaluate(t => window.render(t), i / FPS);
  const buf = await p.screenshot({ type: 'jpeg', quality: 95 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
}
ff.stdin.end(); await b.close();
await new Promise(r => ff.on('close', r)); console.log('done', N, 'frames');
