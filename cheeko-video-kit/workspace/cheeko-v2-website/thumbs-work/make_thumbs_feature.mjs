// Reel covers for the one-feature videos V11-V18 (English + Hindi). Usage: node make_thumbs_feature.mjs
import { chromium } from '../brag-output-2026-09-28-reel/work/pw.mjs';
const D = 'dev2/';   // new Cheeko design (Sep 2026): make_dev_v2.py
const dev = (k, x = 470, y = 860, w = 420, r = 5) => ({kind: 'dev', src: D + k + '.png', x, y, w, r});
const card = (src, x = 110, y = 920, w = 310, r = -8) => ({kind: 'card', src: 'cards-shipping/' + src, x, y, w, r});
const pic = (src, x, y, w, h, r, pos) => ({kind: 'photo', src, x, y, w, h, r, pos});
const stk = (emoji, x, y, size = 150) => ({kind: 'sticker', emoji, x, y, size});
const iph = (src, x, y, w = 460, r = 0, scroll = 0) => ({kind: 'iphone', src: 'app-shots-ios/' + src, x, y, w, r, scroll});   // iPhone body (V25+)
const E = s => `<span class="e">${s}</span>`, H = s => `<span class="hl">${s}</span>`;
const T = {
  'parent-app': [{bg: '#1A120C', size: 128, hook: `Their playtime.<br>Your ${H('rules.')} ${E('🔑')}`, pill: 'See every word. Control it from your phone.'}, [pic('app-shots/02_today_chats.png', 70, 900, 440, 700, -6, '50% 8%'), pic('app-shots/06_analytics_week.png', 570, 860, 440, 700, 6, '50% 10%'), stk('🛡️', 460, 1480, 150)]],
  'parent-app-hi': [{bg: '#1A120C', size: 130, hook: `उनका खेल।<br>आपके ${H('नियम।')} ${E('🔑')}`, pill: 'हर शब्द देखो। फ़ोन से कंट्रोल करो।'}, 'parent-app'],
  'meet-cheeko': [{bg: '#FFC81A', size: 150, hook: `Meet<br>${H('Cheeko!')} ${E('🦊')}`, pill: 'Getting started · Part 1 of 4'}, [dev('talk', 300, 860, 480, 0), stk('📖', 110, 950), stk('🎨', 830, 980), stk('🎮', 120, 1330), stk('🗣️', 830, 1360)]],
  'switch-on': [{bg: '#FFC81A', size: 130, hook: `Switch on.<br>${H('Learn to play.')} ${E('🎮')}`, pill: 'Getting started · Part 2 of 4'}, [dev('tutorial', 300, 860, 480, 0), stk('🔄', 120, 960), stk('👆', 830, 980), stk('☝️', 120, 1330), stk('🎴', 830, 1360)]],
  'connect': [{bg: '#6C3DFF', size: 130, hook: `Connect in<br>${H('5 steps')} ${E('📶')}`, pill: 'Getting started · Part 3 of 4'}, [pic('app-shots/setup/s06b_found.png', 70, 880, 440, 720, -6, '50% 5%'), dev('code', 560, 900, 420, 6)]],
  'first-five-minutes': [{bg: '#2F6B4F', size: 130, hook: `Your first<br>${H('5 minutes')} ${E('⏱️')}`, pill: 'Getting started · Part 4 of 4'}, [card('01-tales-of-kindness.jpg'), dev('talk'), stk('🎨', 820, 1330), stk('🎧', 120, 1420, 130)]],
  'app-home': [{bg: '#FFC81A', size: 130, hook: `See their<br>${H('whole day')} ${E('📱')}`, pill: 'App guide · Part 1 of 5'}, [iph('01_home.png', 300, 830, 480, -3), stk('🐝', 110, 1000), stk('🔥', 830, 1300)]],
  'app-device': [{bg: '#F0521D', size: 120, hook: `Cheeko's<br>${H('remote control')} ${E('🎛️')}`, pill: 'App guide · Part 2 of 5'}, [iph('03_device_controls.png', 80, 860, 460, -5), dev('talk', 580, 960, 400, 6)]],
  'app-analytics': [{bg: '#6C3DFF', size: 140, hook: `Watch them<br>${H('grow')} ${E('📈')}`, pill: 'App guide · Part 3 of 5'}, [iph('06_analytics_week.png', 300, 830, 480, 3), stk('🐝', 120, 1320), stk('📊', 830, 1000)]],
  'app-gallery-cards': [{bg: '#2F6B4F', size: 120, hook: `Your voice,<br>${H('on their card')} ${E('🎙️')}`, pill: 'App guide · Part 4 of 5'}, [iph('08_custom_card_list.png', 80, 860, 460, -4), card('06-make-your-own.jpg', 640, 980, 300, 8), stk('🎨', 830, 820)]],
  'app-profile': [{bg: '#231A10', size: 130, hook: `Their playtime.<br>Your ${H('rules.')} ${E('🔑')}`, pill: 'App guide · Part 5 of 5'}, [iph('04_house_rules_bedtime8.png', 300, 830, 480, -3), stk('🏠', 110, 1000), stk('🎂', 830, 1300)]],
  'app-home-hi': [{bg: '#FFC81A', size: 130, hook: `उनका पूरा<br>${H('दिन')} देखो ${E('📱')}`, pill: 'ऐप गाइड · भाग 1 / 5'}, 'app-home'],
  'app-device-hi': [{bg: '#F0521D', size: 120, hook: `Cheeko का<br>${H('रिमोट कंट्रोल')} ${E('🎛️')}`, pill: 'ऐप गाइड · भाग 2 / 5'}, 'app-device'],
  'app-analytics-hi': [{bg: '#6C3DFF', size: 130, hook: `उन्हें<br>${H('बढ़ते')} देखो ${E('📈')}`, pill: 'ऐप गाइड · भाग 3 / 5'}, 'app-analytics'],
  'app-gallery-cards-hi': [{bg: '#2F6B4F', size: 115, hook: `आपकी आवाज़,<br>${H('उनके कार्ड पर')} ${E('🎙️')}`, pill: 'ऐप गाइड · भाग 4 / 5'}, 'app-gallery-cards'],
  'app-profile-hi': [{bg: '#231A10', size: 130, hook: `उनका खेल।<br>आपके ${H('नियम।')} ${E('🔑')}`, pill: 'ऐप गाइड · भाग 5 / 5'}, 'app-profile'],
  'app-guide-full': [{bg: '#F0521D', size: 140, hook: `The whole<br>${H('Cheeko app')} ${E('📱')}`, pill: 'Full app guide · 5 chapters'}, [iph('01_home.png', 40, 930, 380, -9), iph('06_analytics_week_breakdown.png', 660, 930, 380, 9), iph('03_device_controls.png', 320, 850, 440, 0)]],
  'app-guide-full-hi': [{bg: '#F0521D', size: 140, hook: `पूरा<br>${H('Cheeko ऐप')} ${E('📱')}`, pill: 'पूरी ऐप गाइड · 5 भाग'}, 'app-guide-full'],
  'imagine': [{bg: '#6C3DFF', size: 160, hook: `Say it.<br>${H('See it.')} ${E('🎨')}`, pill: 'Your kid says it. Cheeko draws it.'}, [dev('imagine', 330, 880, 420, 4), pic('imagine/im-17.jpg', 60, 980, 330, 250, -8), pic('imagine/im-10.jpg', 700, 1270, 320, 240, 7)]],
  'imagine-hi': [{bg: '#6C3DFF', size: 150, hook: `बोलो।<br>${H('देखो।')} ${E('🎨')}`, pill: 'बच्चा बोलता है, Cheeko ड्रॉ करता है'}, 'imagine'],
  'mitthu': [{bg: '#2F6B4F', size: 118, hook: `Your kid's new<br>English ${H('teacher')} ${E('🦜')}`, pill: 'New English words every day'}, [card('05-mitthu-the-parrot.jpg'), dev('mitthu'), stk('🐘', 820, 1330)]],
  'mitthu-hi': [{bg: '#2F6B4F', size: 130, hook: `नया इंग्लिश<br>${H('टीचर')} ${E('🦜')}`, pill: 'रोज़ नए इंग्लिश वर्ड्स'}, 'mitthu'],
  'grandmas-voice': [{bg: '#FFA9C9', size: 120, hook: `Grandma's voice,<br>${H('on demand')} ${E('💛')}`, pill: 'Record 10 clips. Play them forever.'}, [card('06-make-your-own.jpg'), dev('grandma')]],
  'grandmas-voice-hi': [{bg: '#FFA9C9', size: 130, hook: `दादी की आवाज़,<br>${H('जब चाहो')} ${E('💛')}`, pill: '10 क्लिप रिकॉर्ड करो। हमेशा सुनो।'}, 'grandmas-voice'],
  'games': [{bg: '#6C3DFF', size: 150, hook: `8 games.<br>${H('Zero Wi-Fi.')} ${E('🎮')}`, pill: 'No ads. No in-app purchases.'}, [dev('games', 330, 880, 420, 3), stk('🚀', 110, 930), stk('🎹', 820, 960), stk('🦘', 120, 1300), stk('🎨', 820, 1320)]],
  'games-hi': [{bg: '#6C3DFF', size: 130, hook: `8 गेम्स।<br>${H('वाई फ़ाई ज़ीरो।')} ${E('🎮')}`, pill: 'ना ऐड्स। ऐप में कोई खरीदारी नहीं।'}, 'games'],
  'nani': [{bg: '#3B1F4F', size: 130, hook: `A storyteller<br>who ${H('listens')} ${E('👂')}`, pill: 'Interrupt her mid-story'}, [card('10-nani.jpg'), dev('nani')]],
  'nani-hi': [{bg: '#3B1F4F', size: 118, hook: `कहानी वाली नानी,<br>जो ${H('सुनती')} है ${E('👂')}`, pill: 'बीच में टोको, वो सुनती हैं'}, 'nani'],
  'quizzy': [{bg: '#FFC81A', size: 130, hook: `10 questions.<br>${H('No pressure.')} ${E('🐝')}`, pill: 'Answer in your own words'}, [dev('quizzy', 330, 880, 420, 4), stk('🦎', 800, 1270, 170), stk('🎉', 110, 930)]],
  'quizzy-hi': [{bg: '#FFC81A', size: 130, hook: `रोज़ 10 सवाल।<br>${H('ना प्रेशर।')} ${E('🐝')}`, pill: 'अपने शब्दों में जवाब दो'}, 'quizzy'],
  'talk': [{bg: '#FFC81A', size: 140, hook: `Why is the<br>sky ${H('blue?')} ${E('🤔')}`, pill: 'Ask Cheeko anything'}, [pic('live/kid-beanbag.jpg', 70, 900, 460, 580, -5, '50% 40%'), dev('talk', 570, 900, 380, 6)]],
  'talk-hi': [{bg: '#FFC81A', size: 130, hook: `आसमान नीला<br>${H('क्यों है?')} ${E('🤔')}`, pill: 'Cheeko से कुछ भी पूछो'}, 'talk'],
  'funny-voice': [{bg: '#E5341B', size: 130, hook: `This toy causes<br>${H('giggles')} ${E('😂')}`, pill: 'Five silly voices, no Wi-Fi'}, [pic('live/kid-joy.jpg', 70, 900, 470, 580, -5, '50% 40%'), dev('funny', 570, 900, 380, 6), stk('🐿️', 830, 800, 130), stk('👹', 820, 1400, 130)]],
  'brag-output-2026-09-30-make-your-own': [{bg: '#F0521D', size: 124, hook: `Put ${H('your voice')}<br>on a card ${E('🎙️')}`, pill: 'Make Your Own card · in the box'}, [iph('myo/myo_04_ready_full.png', 70, 860, 440, -5, 25), card('06-make-your-own.jpg', 612, 804, 272, 0), dev('myo', 560, 930, 400, 0), stk('👵', 880, 690, 130)]],
  'funny-voice-hi': [{bg: '#E5341B', size: 118, hook: `इस खिलौने से<br>${H('हँसी')} रुकती नहीं ${E('😂')}`, pill: 'पाँच मज़ेदार आवाज़ें'}, 'funny-voice'],
};
const b = await (await chromium()).launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
const ONLY = process.argv.slice(2);
for (const [slug, [spec, items]] of Object.entries(T)) {
  if (ONLY.length && !ONLY.includes(slug)) continue;
  const full = {...spec, layout: 'hero', hi: slug.endsWith('-hi') ? 1 : 0, items: typeof items === 'string' ? T[items][1] : items};
  await p.goto('file://' + process.cwd() + '/thumb.html#' + encodeURIComponent(JSON.stringify(full)), { waitUntil: 'networkidle' });
  await p.reload({ waitUntil: 'networkidle' }); await p.evaluate(() => window.ready);
  await p.screenshot({ path: `../${slug.startsWith('brag-output') ? slug : 'brag-output-2026-09-29-' + slug}/thumbnail.jpg`, type: 'jpeg', quality: 92 }); console.log('thumb', slug);
}
await b.close();
