// V26 Make Your Own Card (2026-09-30): the whole flow in the app, the card into the back pocket, then why it matters.
// Lines: feature_lines.json V26. App screens: real widgets rendered as iOS (app-shots-ios/myo/, marketing/tools/appshots/tests/myo_shots_test.dart).
// Cheeko's screens: firmware renders; a recording's picture fills the screen while it plays (assets/img/myo/, 296 x 240 like the app's fit).
window.SPEC = ({L, E, T}) => {
  const A = 'app-shots-ios/', M = 'app-shots-ios/myo/', P = 'myo/', CARD = 'cards-shipping/06-make-your-own.jpg';
  const PH = {type: 'phone', bg: 'var(--tint)', w: 540, x: 470, y: 250, ry0: -7, ry1: -3, rx0: 3, rx1: 1, tapColor: 'var(--brand)'};
  const S03 = 15.6, S04 = 37.4;   // scroll (% of the capture) that brings the bottom of the tall captures into view
  return {
    mood: 'bright', capsY: 1450, capMax: 6, capSize: 80, deviceColor: 'yellow',
    outro: {cards: [CARD, 'cards-shipping/01-tales-of-kindness.jpg', 'cards-shipping/10-nani.jpg']},
    shots: [
      // hook: the title rolls, then the card glides into the back pocket and its picture lights the screen
      {t: 0, type: 'dicetitle', bg: 'var(--brand)', words: ['Make Your', 'Own Card'], roll: [.3], size: 132, y: 700, sub: '🎙️ + 🖼️ = ❤️', caps: false},
      {t: 1.35, type: 'device', bg: 'var(--sun)', w: 500, x: 305, y: 400, card: {src: CARD, t: 2.1}, confetti: 2.1,
       screens: [[1.35, '01_menu_1_talk'], [2.2, P + 'castle.png']]},

      // Part 1: the app
      {...PH, t: L(1) - .1,
       screens: [[L(1) - .1, A + '01_home.png'], [L(1) + 1.75, A + '10_profile.png'], [L(1) + 3.2, M + 'myo_01_card.png'],
                 [L(2) + .55, M + 'myo_02_rights.png'], [L(2) + 1.55, M + 'myo_03_selected_full.png', [L(2) + 1.6, L(2) + 2.2, 0, S03]],
                 [L(3) - .1, M + 'myo_07_rec_ready.png'], [L(3) + .55, M + 'myo_08_recording.png'], [L(3) + 1.6, M + 'myo_09_rec_done.png'],
                 [L(4) - .1, M + 'myo_03_selected_full.png', [L(4) - .1, L(4), S03, S03]], [L(4) + .5, M + 'myo_10_editor_top.png'],
                 [L(4) + 1.7, M + 'myo_11_editor_filters.png'],
                 [L(5) - .1, M + 'myo_04_ready_full.png', [L(5) - .1, L(5) + .6, 0, S04]], [L(5) + 1.0, M + 'myo_05_uploading_full.png', [L(5), L(5), S04, S04]],
                 [L(5) + 1.55, M + 'myo_06_saved.png']],
       taps: [[L(1) + 1.45, .8, .925], [L(1) + 2.9, .47, .70],
              [L(2) + .25, .5, .59], [L(2) + .9, .08, .585], [L(2) + 1.25, .8, .813],
              [L(3) + .25, .5, .7], [L(3) + .3, .5, .83], [L(3) + 1.3, .5, .83], [L(3) + 1.95, .72, .907],
              [L(4) + .2, .29, .646], [L(4) + 1.0, .93, .56], [L(4) + 2.0, .4, .78], [L(4) + 2.6, .68, .905],
              [L(5) + .75, .5, .892]],
       callouts: [
         [L(1) + 1.4, 'Profile', '', .8, .925, 40, 1180, L(1) + 2.8],
         [L(1) + 2.85, 'Add Custom Cards', '', .47, .70, 40, 1180, L(1) + 3.6],
         [L(2) + .15, 'Upload Audio', 'MP3 or WAV', .5, .59, 40, 700, L(2) + .55],
         [L(2) + 1.9, 'Ready to upload', '', .45, .78, 40, 1180, E(2) + .25],
         [L(3) + .7, 'Record', 'up to 10 minutes', .5, .52, 40, 470, L(3) + 1.6],
         [L(4) + .7, 'Crop', '', .5, .4, 40, 1180, L(4) + 1.7],
         [L(4) + 1.9, 'Filters', '', .4, .78, 40, 470, E(4) + .2],
         [L(5) + .15, "Fits Cheeko's screen", '', .5, .45, 40, 470, L(5) + .75],
         [L(5) + 1.7, 'Saved', 'Cheeko gets it next tap', .5, .92, 40, 1180, E(5) + .3]]},

      // Part 1: Cheeko. The card into the back pocket, then the picture and the recording
      {t: L(6) - .1, type: 'turntable', tr: 'card', h: 860, y: 330, chipY: 1235, card: {src: CARD, t: L(6) + 1.7},
       views: [[L(6) - .1, 'backcard'], [L(7) - .2, 'front', 'Grandma’s lullaby 🔊']],
       screens: [[L(7) - .2, 'content_play_2b_downloading'], [L(7) + .8, P + 'castle.png']],
       callouts: [[L(6) + .3, 'Card pocket', 'on the back', .5, .62, 40, 1100, L(7) - .2]]},
      {t: L(8) - .1, type: 'device', tr: 'lens', bg: 'var(--sun)', w: 500, x: 305, y: 380, card: {src: CARD, t: L(8) - 1}, press: [L(8) + .55], chipY: 1265,
       screens: [[L(8) - .1, P + 'castle.png'], [L(8) + .75, P + 'peacock.png'], [L(10) + .1, P + 'castle.png'], [L(10) + .5, P + 'crow.png'], [L(10) + .9, P + 'peacock.png'], [L(10) + 1.3, P + 'castle.png']],
       callouts: [[L(8) + .1, 'Turn', 'next or back', .49, .571, 640, 900, E(8) + .25]],
       chips: [[L(9), 'Good morning song ☀️'], [L(10) + .1, '🎵 1 of 10'], [L(10) + .5, '🎵 4 of 10'], [L(10) + .9, '🎵 7 of 10'], [L(10) + 1.3, '🎵 10 of 10 ✨']]},

      // Part 2: why it matters
      {t: L(11) - .15, type: 'title', tr: 'shape', bg: 'var(--purple)', y: 560, size: 136, caps: false,
       html: 'Grandma lives<br><span class="hl">far away?</span><br><span class="e">👵 ✈️</span>'},
      {...PH, t: L(12) - .1, tr: 'whip', x: 270, chipY: 1310,
       screens: [[L(12) - .1, M + 'myo_08_recording.png']], chips: [[L(12) + .4, 'Grandma’s lullaby 👵']]},
      {t: L(13) - .1, type: 'photo', src: 'day_bedtime.jpg', pos: '50% 40%'},
      {t: L(14) - .1, type: 'grid', tr: 'whip', bg: 'var(--pink)',
       items: [[L(14) + .05, P + 'peacock.png', 70, 250, 470, 381, -5], [L(14) + 1.35, 'live/mom-reading.jpg', 520, 420, 480, 600, 4], [L(14) + 2.85, P + 'crow.png', 110, 880, 470, 381, -3]]},
      {t: L(15) - .1, type: 'photo', src: 'live/kid-dance.jpg', pos: '50% 30%'},
      {t: L(16) - .1, type: 'device', tr: 'lens', bg: 'var(--green)', w: 500, x: 305, y: 380, card: {src: CARD, t: L(16) - 1}, chipY: 1265,
       screens: [[L(16) - .1, P + 'crow.png'], [L(16) + .6, P + 'castle.png'], [L(16) + 1.3, P + 'peacock.png'], [L(16) + 2.0, P + 'crow.png'], [L(16) + 2.7, P + 'castle.png'], [L(17) + .6, P + 'peacock.png']],
       chips: [[L(16) + .2, '🔁 2'], [L(16) + .9, '🔁 5'], [L(16) + 1.6, '🔁 12'], [L(16) + 2.3, '🔁 27 😅'], [L(17) + .2, 'Wi-Fi off, still playing ✅']]},
      {t: L(18) - .1, type: 'cardwheel', tr: 'portal', device: '01_menu_1_talk', cy: 800},
      {t: L(19) - .15, type: 'outro', tr: 'shape', caps: false},
    ],
    bubbles: {9: {y: 1370}, 13: {y: 1250}, 15: {y: 1250}},
  };
};
