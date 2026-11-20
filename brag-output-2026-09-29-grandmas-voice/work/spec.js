// New design + motion picks + photo swaps, 2026-09-30 (group 3 of the refresh).
// V15 Make Your Own card: "Grandma's voice, on demand". Lines: feature_lines.json V15.
window.SPEC = ({L, E}) => ({
  bubbleY: 1300, deviceColor: 'white',   // the white Cheeko (plan: V15 in white)
  shots: [
    {t: 0, type: 'photo', src: 'shoot/DSC03202.jpg', pos: '50% 40%'},
    {t: L(1) - .1, type: 'grid', tr: 'card', bg: 'var(--pink)', items: [[L(1), 'cards-shipping/06-make-your-own.jpg', 290, 230, 500, 787, -4]]},
    {t: L(2) - .1, type: 'phone', tr: 'whip', bg: 'var(--brand)', w: 540, x: 270, y: 200, ry0: -10, ry1: -4, capsY: 1520, tapColor: 'var(--sun)',
     screens: [[L(2) - .1, 'app-shots-ios/myo/myo_08_recording.png'], [L(2) + 1.35, 'app-shots-ios/myo/myo_11_editor_filters.png']]},
    // the card slides into the back pocket (turntable back view), then Cheeko turns round and plays Grandma's story
    {t: L(3) - .1, type: 'turntable', tr: 'lens', h: 860, y: 360, card: {src: 'cards-shipping/06-make-your-own.jpg', t: L(3) + .9},
     views: [[L(3) - .1, 'backcard'], [L(3) + 1.5, 'front']],
     screens: [[L(3) + 1.5, 'content_play_2b_downloading'], [L(4) - .1, 'content_play_3_item1']]},
    {t: L(5) - .1, type: 'photo', tr: 'circle', src: 'live/kid-hug.jpg', pos: '45% 40%'},
    {t: L(6) - .1, type: 'photo', src: 'bedtime_world.jpg', pos: '50% 40%'},
    {t: L(7) - .1, type: 'title', tr: 'shape', bg: 'var(--brand)', y: 560, size: 140, html: 'Record 10 clips.<br>Play them <span class="hl">forever</span> <span class="e">❤️</span>', caps: false},
    {t: L(8) - .15, type: 'outro', tr: 'shape', caps: false},
  ],
  bubbles: {5: {y: 1180}},
  outro: {cards: ['cards-shipping/06-make-your-own.jpg', 'cards-shipping/10-nani.jpg', 'cards-shipping/04-dreamy-melodies.jpg']},
});
