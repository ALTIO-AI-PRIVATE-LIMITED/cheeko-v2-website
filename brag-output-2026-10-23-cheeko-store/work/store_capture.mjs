// V55: captures the REAL Cheeko Store page (cheeko-app-store-web, branch fix/store-on-manager-api, web/) at iPhone size.
// Nothing is redrawn: the store's own HTML/CSS/JS runs against a stand-in for manager-api that answers with the live
// store's data as read on 2026-10-23 (same featured drops and artwork, same 8 games and 44 videos, sizes and lengths),
// a demo parent and one online Cheeko. Firebase sign-in is stubbed so the page opens signed in.
// Usage: node store_capture.mjs <web dir> <out dir>
import {chromium} from 'playwright';
import fs from 'fs';
import path from 'path';

const [WEB, OUT] = process.argv.slice(2);
const ART = path.resolve('store-art'), DEV = path.resolve('device-videos');
fs.mkdirSync(OUT, {recursive: true});
const ORIGIN = 'http://localhost:8123';

const VIDEOS = `A for Apple Level 1|1:23|3.8|V37-1
A for Apple Level 2|1:32|4.2|V37-2
A for Apple Level 3|1:33|4.3|V37-3
Baby and Mummy|2:11|6.2|V36
Big or Small|2:22|6.7|V45
Cheekos Riddles Level 1|2:28|5.4|V49-1
Cheekos Riddles Level 2|2:34|5.5|V49-2
Emoji Words|2:09|5.7|V53
Famous Places of India Level 1|1:42|7.2|V51-1
Famous Places of India Level 2|1:53|8.3|V51-2
Guess the Dinosaur Level 1|1:42|4.8|V50-1
Guess the Dinosaur Level 2|1:53|5.3|V50-2
Guess the Fruit Level 1|1:32|4.4|V33-1
Guess the Fruit Level 2|1:42|5|V33-2
Guess the Fruit Level 3|1:53|5.2|V33-3
Guess the Instrument Level 1|2:08|6.8|V46-1
Guess the Instrument Level 2|2:19|7.2|V46-2
Guess the Vehicle Level 1|1:50|6.1|V31-1
Guess the Vehicle Level 2|2:01|6.7|V31-2
Guess the Vehicle Level 3|2:12|7|V31-3
How Does Cheeko Feel|1:35|5|V40
How Many Level 1|1:46|4.2|V38-1
How Many Level 2|2:10|5.5|V38-2
Indian Birds Level 1|1:40|4.9|V44-1
Indian Birds Level 2|1:51|5.1|V44-2
Ocean Animals 10|1:50|8.2|V30
Odd One Out Level 1|2:02|8.1|V48-1
Odd One Out Level 2|2:15|8.7|V48-2
Shadow Match Level 1|1:31|4|V39-1
Shadow Match Level 2|1:41|4.4|V39-2
Shadow Match Level 3|1:52|4.4|V39-3
Shapes Around Us Level 1|1:52|6.6|V41-1
Shapes Around Us Level 2|2:05|7.2|V41-2
Sounds Around the House Level 1|2:09|5|V43-1
Sounds Around the House Level 2|2:17|5.2|V43-2
Space Quiz|2:14|5.8|V47
Touch Your Nose|2:05|6.4|V35
What Colour Is It Level 1|1:37|5.1|V34-1
What Colour Is It Level 2|1:48|5.7|V34-2
What Is Missing|2:24|7.1|V52
Who Helps Us Level 1|1:53|5.5|V42-1
Who Helps Us Level 2|2:04|6.1|V42-2
Who Says That Level 1|1:54|5.8|V32-1
Who Says That Level 2|2:07|6.2|V32-2`.split('\n').map(l => l.split('|'));
const GAMES = [['Find the pairs', 768, 'PAIRS'], ['How many?', 576, 'HOWMANY'], ['Jump', 576, 'JUMP'], ['Paint', 448, 'PAINT'],
  ['Piano', 384, 'PIANO'], ['Space', 640, 'SPACE'], ['Trace', 512, 'TRACE'], ['Who says what?', 896, 'WHOSAYS']];
const thumbs = fs.readdirSync(path.join(ART, 'videos'));
const thumbFor = v => thumbs.find(f => f.startsWith(`Cheeko_${v.replace('-', '.')}_`) || f.startsWith(`Cheeko_${v}_`));
const items = [
  ...GAMES.map(([title, kb, b]) => ({id: `app:${b.toLowerCase()}`, kind: 'game', title, description: null, size: kb * 1024, version: '0.1.3',
    icon_url: `${ORIGIN}/art/games/${b}.png`})),
  ...VIDEOS.map(([title, dur, mb, v]) => { const [m, s] = dur.split(':').map(Number);
    return {id: `pack:${v}`, kind: 'video', title, description: null, size: Math.round(mb * 1048576), seconds: m * 60 + s,
      icon_url: `${ORIGIN}/art/videos/${thumbFor(v)}`, video_url: `${ORIGIN}/media/${v}.mp4`}; }),
];
const byTitle = t => items.find(i => i.title === t);
const FEATURED = [
  ['Let the Music Begin!', 'Explore sounds, rhythms and melodies with Cheeko.', 'MUSIC TIME', 'Make Some Music', '7d54119c-1ce2-48e2-ab0c-af80d4c7456b', ['Piano', 'Guess the Instrument Level 1', 'Guess the Instrument Level 2']],
  ['Playtime Just Got More Fun!', 'Discover exciting new games for your little', 'NEW GAMES', 'Explore Games', '459e30f1-90c6-4057-9bf5-326122577014', ['How many?', 'How Many Level 1', 'How Many Level 2']],
  ['Storytime, Smiles & Surprises', 'Watch fun learning videos filled with animals, riddles and amazing facts.', 'VIDEO PICKS', 'Watch Now', '4bb428e7-18bd-4381-9501-28771d5b00b8', ['Who says what?', 'Cheekos Riddles Level 1', 'Ocean Animals 10']],
  ['Blast Off on a Space Adventure!', 'Explore the universe with fun games and curious discoveries.', 'FEATURED ADVENTURE', 'Explore Space', 'd5ad6927-1a24-4877-a5ca-f697b35db9a0', ['Space', 'Space Quiz']],
  ['Little Minds, Big Discoveries', 'Learn numbers, letters, shapes and more through play.', 'LEARN & PLAY', 'Start Learning', '10545ecc-a9bc-4e0f-a4cf-0011b2bd83cf', ['Jump', 'A for Apple Level 1']],
].map(([title, subtitle, badge_text, cta_label, art, linked], i) => {
  const rows = linked.map((t, k) => { const it = byTitle(t); return {id: it.id, content_type: it.kind, title: it.title, image_url: it.icon_url, display_order: k}; });
  return {id: `campaign-${i + 1}`, title, subtitle, badge_text, cta_label, text_theme: 'light', action_type: 'NONE',
    artwork_url: `${ORIGIN}/art/featured/${art}.jpg`, primary_content: rows[0], items: rows};
});
const DEVICE = 'e8:9f:6d:42:19:c0';
const state = {installed: {}, job: null};
const ok = data => ({status: 200, contentType: 'application/json', body: JSON.stringify({code: 0, msg: 'success', data})});
const TYPES = {'.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.mjs': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.mp4': 'video/mp4'};
const file = p => ({status: 200, contentType: TYPES[path.extname(p)] || 'application/octet-stream', body: fs.readFileSync(p)});
const FIREBASE_APP = `export function initializeApp(c){return {c}}`;
const FIREBASE_AUTH = `const user={uid:'demo-parent',email:'parent@example.com',getIdToken:async()=>'demo-token'};
export function getAuth(){return {}}
export function onAuthStateChanged(a,cb){setTimeout(()=>cb(user),50);return ()=>{}}
export async function signOut(){}
export class GoogleAuthProvider{setCustomParameters(){}}
export class OAuthProvider{addScope(){}}
export async function signInWithPopup(){return {user}}`;

const browser = await chromium.launch();
const ctx = await browser.newContext({viewport: {width: 393, height: 793}, deviceScaleFactor: 3, isMobile: true, hasTouch: true,
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'});
await ctx.route('**/*', async route => {
  const u = new URL(route.request().url()), m = route.request().method();
  if (u.hostname === 'www.gstatic.com' && u.pathname.includes('firebasejs')) {
    return route.fulfill({status: 200, contentType: 'text/javascript', headers: {'Access-Control-Allow-Origin': '*'},
      body: u.pathname.endsWith('firebase-auth.js') ? FIREBASE_AUTH : FIREBASE_APP});
  }
  if (u.origin !== ORIGIN) return route.continue();   // Google Fonts
  const p = u.pathname;
  if (p === '/' || p === '/index.html') return route.fulfill(file(path.join(WEB, 'storefront.html')));
  if (p.startsWith('/assets/')) return route.fulfill(file(path.join(WEB, p.slice(8))));
  if (p.startsWith('/art/')) return route.fulfill(file(path.join(ART, decodeURIComponent(p.slice(5)))));
  if (p.startsWith('/media/')) return route.fulfill(file(path.join(DEV, 'dino.mp4')));
  if (p === '/toy/api/mobile/parent-profile') return route.fulfill(ok({fullName: 'Demo Parent', phoneNumber: '9000000000'}));
  const A = '/toy/api/mobile/cheeko-store';
  if (p === A + '/catalog') return route.fulfill(ok({items}));
  if (p === A + '/featured-drops') return route.fulfill(ok(FEATURED));
  if (p === A + '/devices') return route.fulfill(ok([{device: DEVICE, alias: 'Cheeko', online: true, installed: state.installed}]));
  if (p === A + '/installable') return route.fulfill(ok({items: items.map(i => i.id)}));
  if (p === A + '/installs' && m === 'POST') { const b = JSON.parse(route.request().postData());
    state.job = {id: 'job-1', item: b.id, device: b.device, status: 'queued', progress: 0, message: ''}; return route.fulfill(ok(state.job)); }
  if (p.startsWith(A + '/installs/')) return route.fulfill(ok(state.job));
  return route.fulfill({status: 404, body: 'not found'});
});
const page = await ctx.newPage(); page.on('console', m => console.log('console:', m.type(), m.text().slice(0, 200))); page.on('pageerror', e => console.log('pageerror:', e.message)); page.on('requestfailed', r => console.log('failed:', r.url().slice(0, 120)));
const GEO = {};
const rects = async (key, sels) => { GEO[key] = await page.evaluate(sels => Object.fromEntries(Object.entries(sels).map(([k, q]) => { const e = document.querySelector(q); if (!e) return [k, null]; const r = e.getBoundingClientRect(); return [k, [Math.round(r.left), Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)]]; })), sels); };
const shot = async (name, opts = {}) => { await page.waitForTimeout(400); await page.screenshot({path: path.join(OUT, name + '.png'), ...opts}); console.log('saved', name); };
const ready = async () => { await page.waitForFunction(() => !document.getElementById('storeApp').inert && !document.querySelector('#videos [aria-busy="true"]'), null, {timeout: 20000});
  await page.evaluate(() => document.fonts.ready); await page.evaluate(() => document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; })); await page.waitForFunction(() => [...document.images].filter(i => i.offsetParent).every(i => i.complete && i.naturalWidth)); };

await page.goto(ORIGIN + '/#home'); await ready();
await shot('01_home'); await rects('home', {brand: '.brand', videosNav: '.main-nav [data-view=videos]', header: '.site-header', picker: '#devicePicker', featured: '.featured-card'});
await shot('02_home_full', {fullPage: true});
await page.click('#devicePicker'); await shot('03_device_menu'); await page.click('#devicePicker');
await page.goto(ORIGIN + '/#videos'); await ready(); await page.evaluate(() => window.scrollTo(0, 0));
await shot('04_videos'); await rects('videos', {header: '.site-header', heading: '#videosHeading', dino: '[data-item-id="pack:V50-1"]', riddles: '[data-item-id="pack:V49-1"]', emoji: '[data-item-id="pack:V53"]', first: '.video-card'});
await shot('05_videos_full', {fullPage: true});
await page.goto(ORIGIN + '/#home'); await ready(); await page.evaluate(() => window.scrollTo(0, 0));
await page.click('.mobile-search'); await page.type('#searchInput', 'Dinosaur', {delay: 30}); await shot('06_search_dinosaur');
await page.fill('#searchInput', ''); await page.keyboard.press('Escape'); await page.evaluate(() => document.activeElement.blur());
await page.goto(ORIGIN + '/#home'); await ready();
await page.goto(ORIGIN + '/#video/' + encodeURIComponent('pack:V50-1')); await ready(); await page.evaluate(() => window.scrollTo(0, 0));
await shot('07_dino_detail'); await rects('detail', {art: '.detail-art', title: '#detailTitle', preview: '[data-detail-action=preview]', send: '[data-detail-action=install]', note: '[data-install-note]', header: '.site-header'});
await page.click('[data-detail-action="install"]'); await page.waitForTimeout(300);
await shot('08_dino_queued');
state.job = {...state.job, status: 'sending', progress: .4}; await page.waitForTimeout(2600);
await shot('09_dino_sending40');
state.job = {...state.job, status: 'sending', progress: .85}; await page.waitForTimeout(2200);
await shot('10_dino_sending85');
state.installed = {'pack:V50-1': 'installed'}; state.job = {...state.job, status: 'done', progress: 1}; await page.waitForTimeout(3000);
await shot('11_dino_sent');
await page.click('#accountButton'); await page.click('#downloadedToggle'); await page.waitForTimeout(300);
await shot('12_downloaded_menu');
fs.writeFileSync(path.join(OUT, 'geometry.json'), JSON.stringify(GEO, null, 1)); await browser.close();
