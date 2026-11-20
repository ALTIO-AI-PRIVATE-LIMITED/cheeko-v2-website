// Refresh 2026-09-30 (group 4): new device, motion picks, photo swaps.
// V21 Switch On and Learn to Play (Getting Started, part 2 of 4). Cheeko's lines are the device's own recordings
// (cheeko-os-v2 main/assets/common/onb_*.ogg) over the matching first-boot tutorial screens (fw-screens/16_onboarding_*).
window.SPEC = ({L, E, T}) => {
  const HI = (T.vid || '').endsWith('-HI'), tx = (en, hi) => HI ? hi : en;
  const W = 520, X = 280, Y = 330, H = W * 3619 / 2162, SX = X + W * .5, SY = Y + H * .25;
  return {
    mood: 'calm', capsY: 1330, bubbleY: 1350, badge: tx('GETTING STARTED · <b>2/4</b>', 'शुरुआत · <b>2/4</b>'),
    shots: [
      // A2 turntable: the left side (USB-C) for step 1, the right side (power) for step 2 (the old studio side photo showed the old device)
      {t: 0, type: 'turntable', h: 900, y: 330, chipY: 1250,
       views: [[0, 'left'], [L(1) - .1, 'right']],   // the captions say the step
       callouts: [[.4, 'USB-C', tx('any USB-C charger', 'कोई भी USB-C चार्जर'), .40, .325, 40, 1080, L(1) - .1],
                  [L(1) + .4, tx('Power', 'पावर'), tx('press to switch on', 'दबाकर ऑन करो'), .62, .434, 620, 980]]},
      {t: L(1) + 2.2, type: 'device', tr: 'lens', bg: 'var(--ink)', rays: false, w: W, x: X, y: Y, screens: [[L(1) + 2.2, 'setup_1_boot']]},
      {t: L(2) - .1, type: 'device', tr: 'whip', bg: 'var(--sun)', w: W, x: X, y: Y, chipY: Y + H + 25,
       press: [L(5) + .35, L(6) + .25, L(6) + .55],
       screens: [[L(2) - .1, '16_onboarding_1_intro'], [L(4) - .05, '16_onboarding_2_turn'], [L(5) - .05, '16_onboarding_3_press'], [L(6) - .05, '16_onboarding_4_back'],
                 [L(7) - .05, '16_onboarding_5_tap'], [L(8) - .05, '16_onboarding_6_swipe']],
       chips: [[L(4), tx('Turn 🔄', 'घुमाओ 🔄')], [L(5), tx('Press 👆', 'दबाओ 👆')], [L(6), tx('Press twice ↩️', 'दो बार दबाओ ↩️')], [L(7), tx('Tap 👆', 'टैप 👆')],
               [L(8), tx('Swipe up ☝️', 'ऊपर स्वाइप ☝️')]]},
      // "Put a card on me": the card slides into the pocket on the back (A2 back view), then Cheeko turns round
      {t: L(9) - .1, type: 'turntable', tr: 'lens', h: 880, y: 330, chipY: 1200, card: {src: 'cards-shipping/03-play-and-sing-along.jpg', t: L(10) + .6},
       views: [[L(9) - .1, 'backcard'], [L(10) + 1.3, 'front', tx('Story or rhyme card 📖🎵', 'कहानी या राइम कार्ड 📖🎵')]],
       screens: [[L(9) - .1, '16_onboarding_7_card']],
       callouts: [[L(9) + .3, tx('Card pocket', 'कार्ड पॉकेट'), tx('on the back', 'पीछे की तरफ़'), .5, .62, 40, 1080, L(10) + 1.3]]},
      {t: L(11) - .1, type: 'device', tr: 'circle', bg: 'var(--sun)', w: W, x: X, y: Y, chipY: Y + H + 25, card: {src: 'cards-shipping/03-play-and-sing-along.jpg', t: L(11) - .6},
       screens: [[L(11) - .1, '16_onboarding_8_card_ok'], [L(12) - .05, '16_onboarding_9_done']], chips: [[L(12), tx('Ready! 🎉', 'तैयार! 🎉')]], confetti: L(11) + .1},
      {t: L(13) - .1, type: 'title', tr: 'shape', bg: 'var(--brand)', y: 520, size: 140, caps: false,
       html: tx('Turn. Press.<br>Tap. Swipe.<br><span class="hl">Cards.</span> <span class="e">🎴</span>', 'घुमाओ। दबाओ।<br>टैप। स्वाइप।<br><span class="hl">कार्ड।</span> <span class="e">🎴</span>')},
      {t: L(14) - .1, type: 'title', tr: 'whip', bg: 'var(--purple)', y: 600, size: 140, caps: false, slate: true,
       html: tx('Next:<br><span class="hl">Connect it</span> <span class="e">👉</span><br><span style="font-size:60px">Part 3 of 4</span>', 'अगला:<br><span class="hl">कनेक्ट करो</span> <span class="e">👉</span><br><span style="font-size:60px">भाग 3 / 4</span>')},
    ],
    stickers: [{t: L(4) + .2, until: E(4) + .2, emoji: '🔄', x: SX + 150, y: Y + H*.5, size: 140},
               {t: L(7) + .2, until: E(7) + .2, emoji: '👆', x: SX - 40, y: SY - 10, size: 150},
               {t: L(8) + .2, until: E(8) + .2, emoji: '☝️', x: SX - 40, y: SY - 40, size: 150}],
  };
};
