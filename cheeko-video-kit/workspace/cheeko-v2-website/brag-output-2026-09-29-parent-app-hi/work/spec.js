// V19 Parent App: "Their playtime. Your rules." Premium dark style (Ravi's references: motionin.design).
// App screens are the real Flutter widgets rendered with sample data (assets/img/app-shots, commit d49af42).
window.SPEC_EN = ({L, E, T}) => {
  const HI = (T.vid || '').endsWith('-HI');
  const tx = (en, hi) => HI ? hi : en;
  const AS = 'app-shots/';
  const DARK = '#1A120C';
  return {
    mood: 'calm', capsY: 1350,
    shots: [
      {t: 0, type: 'photo', src: 'live/hero-kid-joy.jpg', pos: '50% 35%'},
      {t: L(1) - .15, type: 'phone', w: 500, y: 150, screens: [[L(1) - .15, AS + '02_today_chats.png']], ry0: -26, ry1: -10,
       tags: [[L(1) + .6, tx('Every word 👀', 'हर शब्द 👀'), 60, 330, 'var(--sun)'], [L(1) + .9, tx('Both sides', 'दोनों तरफ़'), 700, 820, '#fff', 'var(--ink)', 5]]},
      {t: L(2) - .1, type: 'device', bg: DARK, rays: false, w: 500, y: 430, press: [L(2) + 1.2], screens: [[L(2) - .1, '01_menu_1_talk'], [L(2) + 1.2, '03_talk_1_cheeko_4_listening']]},
      {t: L(3) - .1, type: 'stamps', caps: false, items: [[L(3) - .1, tx('No<br>camera. 📷', 'ना<br>कैमरा। 📷'), '#231A10'], [L(3) + .85, tx('No wake<br>word. 🤫', 'ना वेक<br>वर्ड। 🤫'), '#F0521D']]},
      {t: L(4) - .1, type: 'title', bg: '#2F6B4F', y: 560, size: 130, caps: false,
       html: tx('Child-safety<br>filters <span class="hl">built in</span> <span class="e">🛡️</span>', 'चाइल्ड सेफ़्टी<br>फ़िल्टर <span class="hl">मौजूद</span> <span class="e">🛡️</span>')},
      {t: L(5) - .15, type: 'phone', w: 500, y: 150, ry0: 22, ry1: 8,
       screens: [[L(5) - .15, AS + '03_device_controls.png'], [L(5) + 1.15, AS + '03_device_controls_adjusted.png']], taps: [[L(5) + 1.0, .5, .165]],
       tags: [[L(5) + 1.15, tx('Volume 🔉', 'वॉल्यूम 🔉'), 620, 260, 'var(--sun)', 'var(--ink)', 4]]},
      {t: L(6) - .1, type: 'device', bg: DARK, rays: false, w: 500, y: 430, screens: [[L(6) - .1, '12_settings_brightness']], dim: [L(6) + 1.1, E(6) + .1]},
      {t: L(7) - .15, type: 'phone', w: 500, y: 150, ry0: -24, ry1: -8, screens: [[L(7) - .15, AS + '04_house_rules.png']],
       tags: [[L(7) + .5, tx('House rules 📏', 'घर के नियम 📏'), 60, 300, 'var(--sun)'], [L(7) + 1.3, tx('No scary stories', 'डरावनी कहानी नहीं'), 600, 700, '#fff', 'var(--ink)', 5]]},
      {t: L(8) - .15, type: 'phone', w: 500, y: 150, ry0: 22, ry1: 8, screens: [[L(8) - .15, AS + '04_house_rules_events.png']],
       tags: [[L(8) + .7, tx('Maths exam 📚', 'मैथ्स एग्ज़ाम 📚'), 620, 980, 'var(--sun)', 'var(--ink)', 4], [L(8) + 1.5, tx('All the best! 🍀', 'ऑल द बेस्ट! 🍀'), 60, 1120, '#2F6B4F', '#fff', -5]]},
      {t: L(9) - .15, type: 'flow', speed: 1.35, items: [AS + '01_home.png', AS + '06_analytics_day.png', AS + '06_analytics_week.png', AS + '06_analytics_week_breakdown.png', AS + '06_analytics_day_quiz.png']},
      {t: L(10) - .15, type: 'phone', w: 500, y: 150, ry0: -22, ry1: -8, screens: [[L(10) - .15, AS + '07_gallery.png']],
       tags: [[L(10) + .7, tx('Saved 🎨', 'सेव 🎨'), 640, 420, 'var(--sun)', 'var(--ink)', 5]]},
      {t: L(11) - .15, type: 'notif', clock: '10:00', day: tx('Tuesday, 29 September', 'मंगलवार, 29 सितंबर'), title: "Today's Cheeko recap 📊", body: 'Cheeko played for 48 minutes across 5 sessions today.'},
      {t: L(11) + 1.45, type: 'phone', w: 500, y: 150, ry0: 22, ry1: 8, screens: [[L(11) + 1.45, AS + '05_streak_screen.png']],
       tags: [[L(11) + 1.8, tx('5 days 🔥', '5 दिन 🔥'), 620, 360, 'var(--sun)', 'var(--ink)', 4]]},
      {t: L(12) - .15, type: 'title', bg: DARK, y: 560, size: 150, caps: false,
       html: tx('Their playtime.<br>Your <span class="hl">rules.</span> <span class="e">🔑</span>', 'उनका खेल।<br>आपके <span class="hl">नियम।</span> <span class="e">🔑</span>')},
      {t: L(13) - .15, type: 'outro', caps: false},
    ],
    outro: {cards: ['cards-shipping/06-make-your-own.jpg', 'cards-shipping/10-nani.jpg', 'cards-shipping/05-mitthu-the-parrot.jpg'],
            price: tx('Parent app on iPhone and Android', 'पेरेंट ऐप iPhone और Android पर')},
  };
};

window.SPEC = h => { const s = window.SPEC_EN(h); s.outro = Object.assign({}, s.outro || {}, {"l1": "कम स्क्रीन।", "l2": "ज़्यादा <span class=\"hlb\">बचपन।<b></b></span> 🧡", "pill": "लिंक बायो में 👆", "send": "ये उस पेरेंट को भेजो जिसे इसकी ज़रूरत है 👀"}); s.who = {kid: ['🧒 बच्चा', '#FFFFFF', '#6C3DFF']}; return s; };
