// New design + motion picks + photo swaps, 2026-09-30 (group 3 of the refresh).
// V13 Funny Voice. Playback lines 3-7 are the kid's line through our versions of the five effects. Lines: feature_lines.json V13.
window.SPEC = ({L, E}) => ({
  bubbleY: 1300, deviceColor: 'pink',   // the pink Cheeko (plan: V13 in pink)
  shots: [
    {t: 0, type: 'dicetitle', bg: 'var(--red)', words: ['WARNING', 'GIGGLES'], roll: [E(0) - .75], size: 170, cwf: .74, y: 560, sub: '⚠️ 😂', caps: true},
    {t: L(1) - .1, type: 'device', tr: 'lens', bg: 'var(--purple)', w: 500, y: 430, press: [L(2) - .25],
     screens: [[L(1) - .1, '01_menu_4_funny_voice'], [L(1) + 1.0, '07_funny_voice_1_chipmunk'], [L(2) - .2, '07_funny_voice_1_chipmunk']]},
    {t: L(3) - .35, type: 'device', tr: 'whip', bg: 'var(--sun)', w: 500, y: 430,
     screens: [[L(3) - .35, '07_funny_voice_1_chipmunk'], [L(4) - .3, '07_funny_voice_2_monster'], [L(5) - .3, '07_funny_voice_3_robot'], [L(6) - .3, '07_funny_voice_4_echo'], [L(7) - .3, '07_funny_voice_5_speedy']],
     chips: [[L(3) - .35, 'Chipmunk 🐿️'], [L(4) - .3, 'Monster 👹'], [L(5) - .3, 'Robot 🤖'], [L(6) - .3, 'Echo 🔊'], [L(7) - .3, 'Speedy ⚡']]},
    {t: L(8) - .1, type: 'photo', tr: 'whip', src: 'shoot/DSC02536.jpg', pos: '45% 40%'},
    {t: L(9) - .15, type: 'outro', tr: 'shape', caps: false},
  ],
  stickers: [{t: L(8) + .4, until: E(8) + .3, emoji: '😂', x: 760, y: 280, size: 180}],
  outro: {cards: ['cards-shipping/02-floor-is-lava.jpg', 'cards-shipping/03-play-and-sing-along.jpg', 'cards-shipping/09-sounds-around-me.jpg']},
});
