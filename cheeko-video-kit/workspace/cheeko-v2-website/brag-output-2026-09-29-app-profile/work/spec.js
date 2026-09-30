// V25.5 App Guide: Profile (part 5 of 5). Real app screens (Flutter widgets, iOS) on an iPhone.
window.SPEC = ({L, E, T}) => {
  const HI = (T.vid || '').endsWith('-HI'), tx = (en, hi) => HI ? hi : en, A = 'app-shots-ios/';
  const PH = {type: 'phone', bg: 'var(--tint)', w: 540, x: 470, y: 250, ry0: -7, ry1: -3, rx0: 3, rx1: 1, tapColor: 'var(--brand)', focusAt: [640, 700]};
  const NAV = {src: A + '10_profile.png', clip: 'inset(86.6% 4.8% 4.5% 4.8% round 7%)'};
  return {
    mood: 'calm', capsY: 1440, capMax: 6, capSize: 80, badge: tx('APP GUIDE · <b>5/5 PROFILE</b>', 'ऐप गाइड · <b>5/5 प्रोफ़ाइल</b>'),
    shots: [
      {...PH, t: 0,
       screens: [[0, A + '01_home.png'], [.9, A + '10_profile.png'], [2.6, A + '11_kid_profile.png'],
                 [L(2) - .1, A + '04_house_rules_bedtime8.png'], [L(3) - .1, A + '04_house_rules_upcoming.png'],
                 [L(4) - .1, A + '10_profile_full.png', [L(4) - .1, L(4) + .5, 0, 38.6], NAV], [L(4) + 1.2, A + '12_notifications.png']],
       taps: [[.5, .824, .915], [2.2, .5, .365], [L(4) + .8, .5, .238]],
       focus: [[1.0, .5, .45, 1.2], [2.6, .5, .3, 1.35], [L(1) + 1.6, .5, .5, 1.3], [L(1) + 3.2, .45, .7, 1.4],
               [L(2) - .1, .5, .35, 1.4], [L(2) + 3.2, .45, .65, 1.4], [L(3) - .1, .5, .78, 1.45], [L(4) - .1, .5, .5, 1], [L(4) + 1.3, .55, .22, 1.5]],
       callouts: [
         [L(1) + .2, tx('Photo', 'फ़ोटो'), '', .5, .21, 40, 430, L(1) + 1.6],
         [L(1) + 1.6, tx('Birthday', 'जन्मदिन'), '', .73, .45, 40, 430, L(1) + 3.2],
         [L(1) + 3.2, tx('What they love', 'उन्हें क्या पसंद है'), '', .73, .71, 40, 1080, E(1) + .25],
         [L(2) + .6, tx('No scary stories', 'डरावनी कहानियाँ नहीं'), '', .82, .4, 40, 1080, L(2) + 2.0],
         [L(2) + 2.0, tx('Bedtime', 'सोने का समय'), '8 PM', .66, .32, 40, 1080, L(2) + 3.3],
         [L(2) + 3.3, tx('Languages', 'भाषाएँ'), '', .19, .53, 40, 1100, L(2) + 4.6],
         [L(2) + 4.6, tx('Topics to skip', 'इनसे बचें'), '', .25, .76, 40, 430, E(2) + .25],
         [L(3) + .6, tx('Big days', 'खास दिन'), tx('Science exam, 14 Oct', 'साइंस एग्ज़ाम, 14 अक्टूबर'), .36, .78, 40, 430, E(3) + .25],
         [L(4) + 1.6, tx('Notifications', 'नोटिफ़िकेशन'), tx('on', 'ऑन'), .87, .205, 40, 1080, L(4) + 2.6]]},
      {t: L(4) + 2.6, type: 'notif', clock: '10:00', day: tx('Tuesday, 29 September', 'मंगलवार, 29 सितंबर'), title: "Today's Cheeko recap 📊", body: 'Cheeko played for 48 minutes across 5 sessions today.'},
      {...PH, t: L(5) - .1,
       screens: [[L(5) - .1, A + '10_profile.png'], [L(6) - .1, A + '10_profile_full.png', [L(6) - .1, L(6) + .5, 0, 38.6], NAV]],
       taps: [[L(6) + 1.0, .5, .338]],
       focus: [[L(5) + .2, .5, .68, 1.3], [L(6) - .1, .5, .5, 1], [L(6) + .6, .5, .34, 1.35]],
       callouts: [
         [L(5) + .3, tx('Add Device', 'डिवाइस जोड़ें'), '', .5, .59, 40, 430, L(5) + 1.6],
         [L(5) + 1.6, 'Wi-Fi', tx('change network', 'नेटवर्क बदलें'), .5, .79, 40, 1080, E(5) + .25],
         [L(6) + .7, tx('Help & Support', 'मदद'), '', .5, .338, 40, 1080, E(6) + .3]]},
      {t: L(7) - .15, type: 'outro', caps: false},
    ],
    outro: {cards: ['cards-shipping/06-make-your-own.jpg', 'cards-shipping/01-tales-of-kindness.jpg', 'cards-shipping/10-nani.jpg'],
            l1: tx('Their playtime.', 'उनका खेल।'), l2: tx('Your <span class="hlb">rules.<b></b></span> 🔑', 'आपके <span class="hlb">नियम।<b></b></span> 🔑'),
            price: tx('Cheeko app on iPhone and Android', 'Cheeko ऐप iPhone और Android पर'), send: tx('Save this for later 📌', 'बाद के लिए सेव करो 📌'), pill: tx('Link in bio 👆', 'लिंक बायो में 👆')},
  };
};
