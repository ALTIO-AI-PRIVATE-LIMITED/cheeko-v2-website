// V21 Switch On and Learn to Play (Getting Started, part 2 of 4). Cheeko's lines are the device's own recordings
// (cheeko-os-v2 main/assets/common/onb_*.ogg) over the matching first-boot tutorial screens (fw-screens/16_onboarding_*).
window.SPEC = ({L, E, T}) => {
  const HI = (T.vid || '').endsWith('-HI'), tx = (en, hi) => HI ? hi : en;
  const W = 520, X = 280, Y = 330, H = W * 847 / 500, SX = X + W * .5, SY = Y + H * .25;
  return {
    mood: 'calm', capsY: 1330, bubbleY: 1350, badge: tx('GETTING STARTED · <b>2/4</b>', 'शुरुआत · <b>2/4</b>'),
    shots: [
      {t: 0, type: 'device', bg: 'var(--tint)', rays: false, w: 560, x: 260, y: 330, step: tx('STEP <span>1</span>', 'स्टेप <span>1</span>'),
       screens: [[0, '15_home_charging']], callouts: [[.4, 'USB-C', tx('any USB-C charger', 'कोई भी USB-C चार्जर'), .03, .33, 40, 1080]]},
      {t: L(1) - .1, type: 'photo', src: 'live/studio-yellow-side.jpg', pos: '50% 50%', still: true, shade: false, focus: [[L(1) - .1, 560, 780, 1.3]],
       callouts: [[L(1) + .4, tx('Power', 'पावर'), tx('press to switch on', 'दबाकर ऑन करो'), 508, 839, 610, 960]]},
      {t: L(1) + 2.2, type: 'device', bg: 'var(--ink)', rays: false, w: W, x: X, y: Y, screens: [[L(1) + 2.2, 'setup_1_boot']]},
      {t: L(2) - .1, type: 'device', bg: 'var(--sun)', w: W, x: X, y: Y, chipY: Y + H + 25, card: {src: 'cards-shipping/03-play-and-sing-along.jpg', t: L(10) + .6},
       press: [L(5) + .35, L(6) + .25, L(6) + .55],
       screens: [[L(2) - .1, '16_onboarding_1_intro'], [L(4) - .05, '16_onboarding_2_turn'], [L(5) - .05, '16_onboarding_3_press'], [L(6) - .05, '16_onboarding_4_back'],
                 [L(7) - .05, '16_onboarding_5_tap'], [L(8) - .05, '16_onboarding_6_swipe'], [L(9) - .05, '16_onboarding_7_card'], [L(11) - .05, '16_onboarding_8_card_ok'], [L(12) - .05, '16_onboarding_9_done']],
       chips: [[L(4), tx('Turn 🔄', 'घुमाओ 🔄')], [L(5), tx('Press 👆', 'दबाओ 👆')], [L(6), tx('Press twice ↩️', 'दो बार दबाओ ↩️')], [L(7), tx('Tap 👆', 'टैप 👆')],
               [L(8), tx('Swipe up ☝️', 'ऊपर स्वाइप ☝️')], [L(9), tx('Card 🎴', 'कार्ड 🎴')], [L(10), tx('Story or rhyme card 📖🎵', 'कहानी या राइम कार्ड 📖🎵')], [L(12), tx('Ready! 🎉', 'तैयार! 🎉')]],
       confetti: L(11) + .1},
      {t: L(13) - .1, type: 'title', bg: 'var(--brand)', y: 520, size: 140, caps: false,
       html: tx('Turn. Press.<br>Tap. Swipe.<br><span class="hl">Cards.</span> <span class="e">🎴</span>', 'घुमाओ। दबाओ।<br>टैप। स्वाइप।<br><span class="hl">कार्ड।</span> <span class="e">🎴</span>')},
      {t: L(14) - .1, type: 'title', bg: 'var(--purple)', y: 600, size: 140, caps: false, slate: true,
       html: tx('Next:<br><span class="hl">Connect it</span> <span class="e">👉</span><br><span style="font-size:60px">Part 3 of 4</span>', 'अगला:<br><span class="hl">कनेक्ट करो</span> <span class="e">👉</span><br><span style="font-size:60px">भाग 3 / 4</span>')},
    ],
    stickers: [{t: L(4) + .2, until: E(4) + .2, emoji: '🔄', x: SX + 150, y: Y + H*.5, size: 140},
               {t: L(7) + .2, until: E(7) + .2, emoji: '👆', x: SX - 40, y: SY - 10, size: 150},
               {t: L(8) + .2, until: E(8) + .2, emoji: '☝️', x: SX - 40, y: SY - 40, size: 150}],
  };
};
