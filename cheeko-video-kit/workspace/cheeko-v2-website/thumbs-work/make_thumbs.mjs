// Render a Reel cover (1080x1920) for every video. Usage: node make_thumbs.mjs
// Instagram's profile grid shows the centre 3:4 (y 240-1680), so the hook and visual stay inside it.
import { chromium } from '../brag-output-2026-09-28-reel/work/pw.mjs';
const T = [
  ['brag-output', { bg: '#F0521D', layout: 'features', size: 118, hook: 'It talks. <span class="e">🗣️</span><br>It draws.<br><span class="hl">It plays.</span>', pill: '₹5,999 · 10 cards in the box' }],
  ['brag-output-2026-09-28-095057', { bg: '#FFC81A', layout: 'cards', size: 128, hook: 'Kid bored? <span class="e">🥱</span><br><span class="hl">Skip the phone</span>', pill: 'Hand them Cheeko instead' }],
  ['brag-output-2026-09-28-reel', { bg: '#6C3DFF', layout: 'tantrum', size: 168, hook: '<span class="hl">NO</span> tantrum?! <span class="e">😳</span>', pill: 'We took the phone away 📵' }],
  ['brag-output-2026-09-28-made-to-end', { bg: '#231A10', layout: 'end', size: 170, hook: 'Built to<br><span class="hl">END</span> <span class="e">✋</span>', pill: 'Your phone never stops. This does.' }],
  ['brag-output-2026-09-28-made-in-india', { bg: '#F0521D', layout: 'sound', size: 150, hook: 'Guess this<br><span class="hl">sound!</span> <span class="e">👂</span>', pill: 'Made in India for Indian kids' }],
  ['brag-output-2026-09-28-reel-hi', { hi: 1, bg: '#6C3DFF', layout: 'tantrum', size: 132, hook: 'कोई रोना-धोना<br><span class="hl">नहीं?!</span> <span class="e">😳</span>', pill: 'फ़ोन ले लिया, फिर भी!' }],
  ['brag-output-2026-09-28-made-to-end-hi', { hi: 1, bg: '#231A10', layout: 'end', size: 140, hook: 'ये <span class="hl">रुकना</span><br>जानता है <span class="e">✋</span>', pill: 'फ़ोन कभी नहीं रुकता. Cheeko रुकता है.' }],
  ['brag-output-2026-09-28-made-in-india-hi', { hi: 1, bg: '#F0521D', layout: 'sound', size: 140, hook: 'ये आवाज़<br><span class="hl">पहचानो!</span> <span class="e">👂</span>', pill: 'भारतीय बच्चों के लिए, भारत में बना' }],
  ['brag-output-2026-09-29-five-minutes', { bg: '#5B7CFA', layout: 'phonepov', size: 124, hook: "POV: you're the<br><span class=\"hl\">family phone</span> <span class=\"e\">📱</span>", pill: 'Then Cheeko showed up 😤' }],
  ['brag-output-2026-09-29-tiny-adults', { bg: '#6C3DFF', layout: 'tinyadults', size: 128, hook: "7 going on <span class=\"hl\">40</span> <span class=\"e\">😳</span>", pill: 'Give kids kid things 🧸' }],
];
const b = await (await chromium()).launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
// node make_thumbs.mjs [folder] renders just that video's cover
for (const [dir, spec] of T.filter(([d]) => !process.argv[2] || d === process.argv[2])) {
  await p.goto('file://' + process.cwd() + '/thumb.html#' + encodeURIComponent(JSON.stringify(spec)), { waitUntil: 'networkidle' });
  await p.reload({ waitUntil: 'networkidle' });
  await p.evaluate(() => window.ready);
  await p.screenshot({ path: `../${dir}/thumbnail.jpg`, type: 'jpeg', quality: 92 });
  console.log('thumb', dir);
}
await b.close();
