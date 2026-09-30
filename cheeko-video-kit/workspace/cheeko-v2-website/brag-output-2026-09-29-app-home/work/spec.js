// V25.1 App Guide: Home (part 1 of 5). Real app screens (Flutter widgets, iOS) on an iPhone.
window.SPEC = ({L, E, T}) => {
  const HI = (T.vid || '').endsWith('-HI'), tx = (en, hi) => HI ? hi : en, A = 'app-shots-ios/';
  const PH = {type: 'phone', bg: 'var(--tint)', w: 540, x: 470, y: 250, ry0: -7, ry1: -3, rx0: 3, rx1: 1, tapColor: 'var(--brand)', focusAt: [640, 700]};
  const NAV = {src: A + '01_home.png', clip: 'inset(86.6% 4.8% 4.5% 4.8% round 7%)'};   // the floating tab bar, pinned while Home scrolls
  const tab = (t0, t1, name, px) => [t0, name, '', px, .915, 40, 1030, t1];
  return {
    mood: 'calm', capsY: 1440, capMax: 6, capSize: 80, badge: tx('APP GUIDE · <b>1/5 HOME</b>', 'ऐप गाइड · <b>1/5 होम</b>'),
    shots: [
      {...PH, t: 0,
       screens: [[0, A + '01_home.png'], [L(3) + .75, A + '02_today_chats.png'], [L(4) + .75, A + '02_today_chats_nani.png'],
                 [L(5) - .1, A + '01_home.png'], [L(6) + 1.25, A + '05_streak_screen.png'],
                 [L(7) - .1, A + '01_home_full.png', [L(7) + .2, E(7) + .4, 45, 54.4], NAV]],
       focus: [[L(1), .5, .9, 1.35], [L(2) + .2, .45, .4, 1.75], [L(3) + .8, .5, .45, 1.45], [L(4) + .05, .5, .24, 1.6],
               [L(5) - .05, .55, .63, 1.7], [L(6), .45, .76, 1.6], [L(6) + 1.3, .5, .35, 1.35], [L(7) - .15, .5, .5, 1]],
       taps: [[L(3) + .3, .786, .41], [L(4) + .3, .5, .19], [L(6) + .85, .37, .787]],
       callouts: [
         tab(L(1) + .15, L(1) + .8, tx('Home', 'होम'), .173), tab(L(1) + .8, L(1) + 1.45, tx('Device', 'डिवाइस'), .391),
         tab(L(1) + 1.45, L(1) + 2.1, tx('Analytics', 'एनालिटिक्स'), .608), tab(L(1) + 2.1, E(1) + .3, tx('Profile', 'प्रोफ़ाइल'), .824),
         [L(2) + .9, tx('48 min', '48 मिनट'), tx('played today', 'आज खेले'), .186, .333, 40, 470, L(2) + 2.8],
         [L(2) + 2.8, '5 · 4 · 3', tx('talks, cards, games', 'बातें, कार्ड, गेम्स'), .52, .472, 40, 820, E(2) + .3],
         [L(3) + 1.5, tx('Their question', 'उनका सवाल'), '', .72, .38, 40, 560, L(3) + 2.9],
         [L(3) + 2.9, tx("Cheeko's answer", 'Cheeko का जवाब'), '', .35, .52, 40, 1040, E(3) + .25],
         [L(4) + 1.0, tx('Just Nani', 'सिर्फ़ नानी'), '', .5, .19, 40, 330, E(4) + .25],
         [L(5) + .25, '7 / 10', tx('quiz answers right', 'सही जवाब'), .768, .65, 40, 860, E(5) + .25],
         [L(6) + .15, tx('5 days', '5 दिन'), tx('in a row 🔥', 'लगातार 🔥'), .37, .787, 40, 1060, L(6) + 1.25]]},
      {t: L(8) - .1, type: 'title', bg: 'var(--brand)', y: 600, size: 130, caps: false, slate: true,
       html: tx('Next:<br><span class="hl">Device</span> <span class="e">👉</span><br><span style="font-size:60px">Part 2 of 5</span>',
                'अगला:<br><span class="hl">डिवाइस</span> <span class="e">👉</span><br><span style="font-size:60px">भाग 2 / 5</span>')},
    ],
  };
};
