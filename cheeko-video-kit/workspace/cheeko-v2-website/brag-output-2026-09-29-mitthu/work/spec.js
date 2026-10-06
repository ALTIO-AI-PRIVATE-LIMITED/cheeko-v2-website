// V18 Mitthu, your English teacher. Lines: feature_lines.json V18.
window.SPEC = ({L, E}) => ({
  bubbleY: 1300,
  shots: [
    {t: 0, type: 'device', bg: 'var(--green)', w: 500, y: 430, card: {src: 'cards-shipping/05-mitthu-the-parrot.jpg', t: L(0) + 1.4},
     screens: [[0, '01_menu_1_talk'], [L(0) + 1.45, 'card_mitthu_1_reveal'], [L(1) - .15, 'card_mitthu_6_talking']]},
    {t: L(4) - .1, type: 'letters', word: 'ENORMOUS', from: L(4) + .05, to: E(4) - .35, bg: 'var(--sun)', img: 'live/char-mitthu.png', y: 760, caps: false},
    {t: L(5) - .1, type: 'device', bg: 'var(--green)', w: 500, y: 430, card: {src: 'cards-shipping/05-mitthu-the-parrot.jpg', t: L(5) - .6},
     screens: [[L(5) - .1, 'card_mitthu_6_talking'], [L(6) - .1, 'card_mitthu_4_listening'], [E(6) + .05, 'card_mitthu_6_talking']]},
    {t: L(7) - .1, type: 'photo', src: 'live/use-2.jpg', pos: '50% 30%'},
    {t: L(9) - .15, type: 'outro', caps: false},
  ],
  stickers: [{t: L(2) + 1.6, until: E(2) + .3, emoji: '🐘', x: 760, y: 900, size: 190}, {t: L(5) + .3, until: E(5) + .2, emoji: '⭐', x: 800, y: 330, size: 150}],
  outro: {cards: ['cards-shipping/05-mitthu-the-parrot.jpg', 'cards-shipping/10-nani.jpg', 'cards-shipping/07-clever-little-tales.jpg']},
});
