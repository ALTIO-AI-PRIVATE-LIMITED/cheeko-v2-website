// Album and song covers for Cheeko Lullabies from art/lul_*.jpg: square 1500x1500 (library/app), wide 1280x720 (YouTube), device 296x240 (Cheeko screen, art only).
// Usage (from this folder): node make_covers.mjs   ->  out/<file>.jpg / .png
import { chromium } from '../../engine/pw.mjs';
import { mkdirSync } from 'fs';
mkdirSync('out', { recursive: true });
const ALBUM = { en: 'Cheeko Lullabies', hi: 'चीको की लोरियाँ' };
const ITEMS = [
  { key: 'album', file: 'Cheeko_Lullabies_Album', en: 'Cheeko Lullabies', hi: 'चीको की लोरियाँ', sub: { en: 'Goodnight songs', hi: 'शुभ रात्रि गीत' } },
  { key: 'song1', n: 1, file: 'Cheeko_Lullaby_1_Moon_Keeps_Watch', en: 'The Moon Keeps Watch', hi: 'चाँद जागे', pos: '50% 30%', al: 'left' },
  { key: 'song2', n: 2, file: 'Cheeko_Lullaby_2_Everyone_Is_Home', en: 'Everyone Is Home', hi: 'सब घर आए', pos: '50% 42%' },
  { key: 'song3', n: 3, file: 'Cheeko_Lullaby_3_Soft_Rain', en: 'Soft Rain', hi: 'धीमी बारिश', pos: '55% 60%' },
];
const b = await (await chromium()).launch();
async function shot(k, w, h, scale, params, out) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
  await p.goto(`file://${process.cwd()}/cover.html?` + new URLSearchParams({ k, ...params }), { waitUntil: 'networkidle' });
  await p.evaluate(() => window.ready);
  await p.screenshot({ path: out, type: out.endsWith('.png') ? 'png' : 'jpeg', ...(out.endsWith('.jpg') ? { quality: 92 } : {}) });
  await p.close(); console.log(out);
}
for (const it of ITEMS) {
  const art = `art/lul_${it.key}.jpg`;
  for (const lang of ['en', 'hi']) {
    const L = lang === 'en' ? 'English' : 'Hindi';
    const sub = it.sub ? it.sub[lang] : ALBUM[lang];
    const foot = it.n ? (lang === 'en' ? `Song ${it.n} of 3` : `गीत ${it.n} / 3`) : (lang === 'en' ? '3 original lullabies' : '3 नई लोरियाँ');
    const P = { lang, art, title: it[lang], sub, num: it.n ? String(it.n) : '', foot, al: it.al || '' };
    await shot('square', 750, 750, 2, P, `out/${it.file}_${L}_cover_1500.jpg`);
    await shot('wide', 640, 360, 2, P, `out/${it.file}_${L}_youtube_1280x720.jpg`);
  }
  await shot('device', 296, 240, 1, { art, pos: it.pos || '50% 60%' }, `out/${it.file}_device_296x240.png`);
}
await b.close();
