// V20 Meet Cheeko (Getting Started, part 1 of 4). NEW DESIGN (Sep 2026 renders) + Ravi's motion picks.
// Lines: feature_lines.json V20 (line 8 re-recorded for the back pocket, line 11 new: the three colours). Device screens: real firmware renders.
window.SPEC = ({L, E, T}) => {
  const HI = (T.vid || '').endsWith('-HI'), tx = (en, hi) => HI ? hi : en;
  const R = 3619 / 2162, DX = 260, DY = 300, DW = 560, DH = DW * R;       // the tour device (new render proportions)
  const P = (fx, fy) => [DX + DW*fx, DY + DH*fy];
  return {
    mood: 'calm', capsY: 1330, deviceColor: 'yellow', badge: tx('GETTING STARTED · <b>1/4</b>', 'शुरुआत · <b>1/4</b>'),
    shots: [
      {t: 0, type: 'device', bg: 'var(--sun)', w: 520, y: 340, confetti: .35,
       screens: [[0, '00_home_clock'], [L(1) - .1, '03_talk_1_cheeko_6_talking']]},
      {t: L(2) - .1, type: 'grid', tr: 'whip', bg: 'var(--brand)', items: [[L(2), 'live/hero-1.jpg', 70, 250, 560, 420, -5], [L(2) + .35, 'live/kid-dance.jpg', 520, 520, 460, 460, 5], [L(2) + .7, 'live/quizzy-girl.jpg', 130, 830, 440, 400, -3]]},
      {t: L(3) - .1, type: 'device', tr: 'lens', bg: 'var(--tint)', rays: false, w: DW, x: DX, y: DY, press: [L(5) + 1.75],
       screens: [[L(3) - .1, '01_menu_1_talk'], [L(5) + .55, '01_menu_2_imagine'], [L(5) + 1.0, '01_menu_3_games'], [L(5) + 1.8, '04_games_menu_1_animal']],
       callouts: [[L(4), tx('Screen', 'स्क्रीन'), tx("Cheeko's face, never videos", 'Cheeko का चेहरा, वीडियो नहीं'), .5, .24, 520, 200, E(4) + .15],
                  [L(5), tx('Knob', 'नॉब'), tx('turn and press', 'घुमाओ और दबाओ'), .49, .571, 620, 880]],
       focus: [[L(4), ...P(.5, .25), 1.25], [L(5), 540, 960, 1]]},
      // A2 turntable: right side (power, volume), the back with the card sliding into the pocket, the front with the card's top above the head,
      // the speaker, the left side (headphone jack, USB-C), then the front charging
      {t: L(6) - .1, type: 'turntable', h: 900, y: 380, chipY: 1292, capsY: 1395, card: {src: 'cards-shipping/01-tales-of-kindness.jpg', t: L(8) + 1.0},
       views: [[L(6) - .1, 'right'], [L(8) - .05, 'backcard'], [L(8) + 2.1, 'front'], [L(9) + 1.35, 'left'], [L(10) + 2.1, 'front', tx('6 hours of play 🔋', '6 घंटे खेल 🔋')]],
       screens: [[L(6) - .1, '01_menu_1_talk'], [L(8) + 2.1, '14_card_reveal_discover'], [L(8) + 2.7, 'cards-shipping/large/01-tales-of-kindness.jpg'], [L(10) + 2.0, '15_home_charging']],
       callouts: [[L(6) + .1, tx('Power', 'पावर'), tx('on and off', 'ऑन और ऑफ़'), .62, .434, 700, 860, L(7)],
                  [L(7) + .05, tx('Volume', 'वॉल्यूम'), tx('up and down', 'ज़्यादा और कम'), .61, .283, 700, 420, L(8) - .05],
                  [L(8) + .3, tx('Card pocket', 'कार्ड पॉकेट'), tx('the card slides in here', 'कार्ड यहाँ जाता है'), .5, .62, 40, 1130, L(8) + 2.1],
                  [L(9) + .1, tx('Speaker', 'स्पीकर'), '', .5, .843, 720, 1120, L(9) + 1.35],
                  [L(9) + 1.45, tx('Headphone jack', 'हेडफ़ोन जैक'), tx('for quiet time', 'शांत समय के लिए'), .415, .51, 40, 500, L(10)],
                  [L(10) + .1, 'USB-C', tx('any USB-C charger', 'कोई भी USB-C चार्जर'), .40, .325, 40, 980, L(10) + 2.1]]},
      {t: L(11) - .1, type: 'trio', tr: 'shape', bg: 'var(--tint)', labels: [tx('Pink', 'पिंक'), tx('Yellow', 'येलो'), tx('White', 'व्हाइट')]},
      {t: L(12) - .1, type: 'cardwheel', tr: 'card', device: '01_menu_1_talk', cy: 800},
      {t: L(13) - .1, type: 'device', tr: 'lens', bg: 'var(--green)', w: 480, y: 400, chipY: 1215, card: {src: 'cards-shipping/03-play-and-sing-along.jpg', t: L(13) + .3},
       screens: [[L(13) - .1, '01_menu_1_talk'], [L(13) + .3, 'cards-shipping/large/03-play-and-sing-along.jpg']],
       chips: [[L(13) + .2, tx('Stories 📖', 'कहानियाँ 📖')], [L(13) + 1.0, tx('Rhymes 🎵', 'राइम्स 🎵')], [L(13) + 1.8, tx('Games 🎮', 'गेम्स 🎮')]]},
      {t: L(14) - .1, type: 'device', bg: 'var(--purple)', w: 520, y: 420, press: [L(14) + .1],
       screens: [[L(14) - .1, '03_talk_1_cheeko_4_listening'], [L(14) + .9, '03_talk_1_cheeko_6_talking'], [L(14) + 2.0, 'imagine_tiger_1_listening'], [L(14) + 3.0, 'imagine_tiger_5_result']],
       popout: {t: L(14) + 3.15, src: 'imagine/im-05.jpg', to: [240, 130, 600]}},
      {t: L(15) - .1, type: 'grid', tr: 'portal', bg: 'var(--sun)', items: [[L(15), 'fw-screens/04_games_menu_1_animal.png', 60, 250, 520, 422, -5], [L(15) + .6, 'fw-screens/07_funny_voice_2_monster.png', 500, 560, 520, 422, 5], [L(15) + 1.4, 'app-shots-ios/01_home.png', 300, 780, 330, 715, -3]]},
      {t: L(16) - .1, type: 'stamps', tr: 'whip', caps: false, items: [[L(16) - .1, tx('No<br>video.', 'ना<br>वीडियो।'), '#F0521D'], [L(16) + .85, tx('No<br>feed.', 'ना<br>फ़ीड।'), '#6C3DFF'], [L(16) + 1.8, tx('No<br>ads.', 'ना<br>ऐड्स।'), '#2F6B4F']]},
      {t: L(17) - .1, type: 'title', tr: 'shape', bg: 'var(--brand)', y: 600, size: 140, caps: false, slate: true,
       html: tx('Next:<br><span class="hl">Set it up</span> <span class="e">👉</span><br><span style="font-size:60px">Part 2 of 4</span>', 'अगला:<br><span class="hl">सेटअप</span> <span class="e">👉</span><br><span style="font-size:60px">भाग 2 / 4</span>')},
    ],
    bubbles: {1: {y: 1330}},
  };
};
