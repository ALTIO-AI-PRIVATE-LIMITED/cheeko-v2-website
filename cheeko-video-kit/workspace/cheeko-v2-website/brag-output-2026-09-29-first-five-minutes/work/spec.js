// V23 Your First Five Minutes (Getting Started, part 4 of 4). Device screens: real firmware renders; app: real widget render.
window.SPEC = ({L, E, T}) => {
  const HI = (T.vid || '').endsWith('-HI'), tx = (en, hi) => HI ? hi : en;
  const W = 520, X = 280, Y = 330;
  return {
    mood: 'calm', capsY: 1330, bubbleY: 1300, badge: tx('GETTING STARTED · <b>4/4</b>', 'शुरुआत · <b>4/4</b>'),
    shots: [
      {t: 0, type: 'device', bg: 'var(--sun)', w: W, x: X, y: Y, screens: [[0, 'setup_8b_ready_home_after_banner']], chips: [[.2, tx('Try this first ✨', 'पहले ये करो ✨')]]},
      {t: L(1) - .1, type: 'device', bg: 'var(--green)', w: W, x: X, y: Y, card: {src: 'cards-shipping/01-tales-of-kindness.jpg', t: L(1) + 1.0}, chipY: 1215,
       screens: [[L(1) - .1, '00_home_clock'], [L(1) + 1.0, '14_card_reveal_discover'], [L(1) + 1.8, 'cards-shipping/large/01-tales-of-kindness.jpg']],
       chips: [[L(1) + 1.9, tx('Story time 📖', 'कहानी शुरू 📖')]]},
      {t: L(2) - .1, type: 'device', bg: 'var(--sun)', w: W, x: X, y: Y, press: [L(2) + 1.2, L(3) - .35],
       screens: [[L(2) - .1, '01_menu_1_talk'], [L(2) + 1.2, '02_talk_picker_1_cheeko'], [L(3) - .3, '03_talk_1_cheeko_4_listening'], [E(3) + .05, '03_talk_1_cheeko_5_thinking'], [L(4) - .05, '03_talk_1_cheeko_6_talking']]},
      {t: L(5) - .1, type: 'device', bg: 'var(--purple)', w: W, x: X, y: Y, press: [L(5) + 1.2], confetti: E(6) + .35,
       screens: [[L(5) - .1, '01_menu_2_imagine'], [L(5) + 1.2, 'imagine_mango_1_listening'], [L(6) + .3, 'imagine_mango_2_listening_transcript'], [E(6) + .05, 'imagine_mango_3_painting'], [E(6) + .35, 'imagine_mango_5_result']]},
      {t: L(7) - .1, type: 'grid', bg: 'var(--brand)', items: [[L(7), 'fw-screens/04_games_menu_4_jump.png', 60, 280, 520, 422, -5], [L(7) + .7, 'fw-screens/07_funny_voice_1_chipmunk.png', 500, 620, 520, 422, 5]]},
      {t: L(8) - .1, type: 'title', bg: 'var(--ink)', y: 420, size: 88, caps: false,
       html: tx('<span class="hl">No Wi-Fi?</span> <span class="e">✅</span><br><span style="font-size:70px">Cards · Games<br>Funny Voice</span><br><br><span class="hl">Needs Wi-Fi</span> <span class="e">📶</span><br><span style="font-size:70px">Talk · Imagine</span>',
                '<span class="hl">बिना वाई फ़ाई</span> <span class="e">✅</span><br><span style="font-size:70px">कार्ड · गेम्स<br>फ़नी वॉइस</span><br><br><span class="hl">वाई फ़ाई चाहिए</span> <span class="e">📶</span><br><span style="font-size:70px">टॉक · इमैजिन</span>')},
      {t: L(9) - .1, type: 'device', bg: 'var(--tint)', rays: false, w: 560, x: 260, y: 300, screens: [[L(9) - .1, 'cards-shipping/large/03-play-and-sing-along.jpg']],
       callouts: [[L(9) + .1, tx('Headphone jack', 'हेडफ़ोन जैक'), tx('for quiet time 🎧', 'शांत समय के लिए 🎧'), .03, .455, 40, 1100]]},
      {t: L(10) - .1, type: 'device', bg: 'var(--ink)', rays: false, w: W, x: X, y: Y, screens: [[L(10) - .1, '00_home_clock']], dim: [L(10) - .1, L(10) + .5], press: [L(10) + 1.55],
       chips: [[L(10) + .1, tx('Nap time 😴', 'झपकी 😴')], [L(10) + 1.5, tx('Press the knob 👆', 'नॉब दबाओ 👆')]]},
      {t: L(10) + 1.9, type: 'device', bg: 'var(--sun)', w: W, x: X, y: Y, screens: [[L(10) + 1.9, 'setup_1_boot'], [L(10) + 2.5, '00_home_clock']]},
      {t: L(11) - .1, type: 'phone', w: 500, y: 150, ry0: -22, ry1: -8, screens: [[L(11) - .1, 'app-shots/01_home.png']],
       tags: [[L(11) + .6, tx('Today: 48 min 📊', 'आज: 48 मिनट 📊'), 560, 420, 'var(--sun)', 'var(--ink)', 4]]},
      {t: L(12) - .15, type: 'outro', caps: false},
    ],
    outro: {cards: ['cards-shipping/01-tales-of-kindness.jpg', 'cards-shipping/03-play-and-sing-along.jpg', 'cards-shipping/10-nani.jpg'], send: tx('Save this for day one 📌', 'पहले दिन के लिए सेव करो 📌')},
    bubbles: {3: {y: 1300}, 4: {y: 1300}, 6: {y: 1300}},
  };
};
