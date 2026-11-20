// YouTube copy: render compose.html (optional ?query) at a big device scale (default 4.5 -> 1332x1080) with the given audio.
// Usage (inside work/): node yt_render.mjs <ffmpeg> <seconds> <audio.wav> <out.mp4> [query, e.g. level=2] [scale]
import { chromium } from './pw.mjs';
import { spawn } from 'child_process';
const [,, FF, secs, AUD, OUT, Q = '', SC = '4.5'] = process.argv;
const FPS = 30, N = Math.round(FPS * Number(secs));
const ff = spawn(FF, ['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-i',AUD,
  '-vf','scale=trunc(iw/2)*2:trunc(ih/2)*2','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',
  '-af','loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000','-c:a','aac','-b:a','192k','-ac','2','-shortest','-movflags','+faststart',OUT], { stdio: ['pipe','inherit','inherit'] });
const b = await (await chromium()).launch();
const p = await b.newPage({ viewport: { width: 296, height: 240 }, deviceScaleFactor: +SC });
await p.goto('file://' + process.cwd() + '/compose.html' + (Q ? '?' + Q : ''), { waitUntil: 'networkidle' });
await p.evaluate(() => window.ready);
for (let i = 0; i < N; i++) {
  await p.evaluate(t => window.render(t), i / FPS);
  const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
}
ff.stdin.end(); await b.close(); await new Promise(r => ff.on('close', r)); console.log('done', OUT);
