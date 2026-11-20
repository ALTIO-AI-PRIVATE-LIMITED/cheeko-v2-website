// V28 Everything Swipes (2026-10-01). Real: about 1 in 3 children starting school try to swipe or tap paper books (UK teachers), and the
// classic clip of a baby pinching a magazine (marketing/v08-research-kids-and-phones.md). Stickers: assets/img/ravi-stories/ (sheet C,
// plus A2 for the storybook). Feed: ravi-stories/feed.png (made up, no brands). Lines: feature_lines.json V28. Cheeko's screen: Night.
window.SPEC = ({L, E}) => {
  const R = 'ravi-stories/', D = 540 - 500 * .47, FEED = R + 'feed.png';
  const swipe = (t, img, bg, w, x, y, label, r) => ({t, type: 'scene', tr: 'whip', bg, rays: true, items: [
    {src: R + img, kind: 'sticker', x, y, w, in: 'pop'},
    {kind: 'label', html: label, x: r > 0 && label.length < 12 ? 620 : 110, y: 330, r, t: t + .35, bg: '#fff', size: 58}]});
  return {
    mood: 'bright', capsY: 1500, deviceColor: 'yellow',
    shots: [
      // Ravi, age four, has a theory.
      {t: 0, type: 'scene', bg: '#FFE7A8', rays: true, items: [
        {src: R + 'c5-theory.png', kind: 'sticker', x: 250, y: 470, w: 580, in: 'pop', t: .05, float: 5},
        {kind: 'label', html: 'Ravi · age 4 👦', x: 110, y: 330, r: -4, t: .6, bg: '#fff'}]},
      // Everything swipes.
      {t: L(1) - .1, type: 'stamps', tr: 'whip', caps: false, items: [[L(1) - .05, 'Everything<br>swipes 👆', '#6C3DFF']]},
      // His storybook. The TV. The window. Even Dadi Maa's photo album. Nanaji's newspaper.
      swipe(L(2) - .1, 'a2-book-swipe.png', '#BFE6FF', 740, 170, 520, '👆 Book', -4),
      swipe(L(3) - .1, 'c1-tv-swipe.png', '#D8F5D0', 800, 140, 500, '👆 TV', 4),
      swipe(L(4) - .1, 'c2-window-swipe.png', '#FFE0EC', 720, 180, 480, '👆 Window', -4),
      swipe(L(5) - .1, 'c3-dadi-album.png', '#FFD6C2', 900, 90, 500, "👆 Dadi Maa's album", 4),
      swipe(L(6) - .1, 'c4-nanaji-paper.png', '#E8E0FF', 900, 90, 470, "👆 Nanaji's paper", -4),
      // On a phone, there's always one more. So he thinks nothing ever ends.
      {t: L(7) - .1, type: 'phone', tr: 'lens', w: 520, x: 280, y: 220, ry0: -12, ry1: -5, rx0: 4, rx1: 2,
       screens: [[L(7) - .1, FEED, [L(7) - .1, L(7) + .3, 20, 20], null, 'light'],
                 [L(7) + .6, FEED, [L(7) + .6, L(7) + .95, 20, 40], null, 'light'],
                 [L(7) + 1.5, FEED, [L(7) + 1.5, L(7) + 1.85, 40, 60], null, 'light'],
                 [L(7) + 2.4, FEED, [L(7) + 2.4, L(7) + 2.75, 60, 80], null, 'light'],
                 [L(7) + 3.3, FEED, [L(7) + 3.3, L(7) + 3.7, 80, 40], null, 'light']],
       tags: [[L(7) + .7, 'One more 👆', 70, 300, '#fff', 'var(--ink)', -5], [L(7) + 1.6, 'One more 👆', 600, 420, 'var(--sun)', 'var(--ink)', 5],
              [L(7) + 2.5, 'One more 👆', 60, 600, '#fff', 'var(--ink)', -3], [L(7) + 3.2, 'The end? Never ♾️', 560, 1180, 'var(--red)', '#fff', 4]]},
      // Cheeko is different. Stories that end.
      {t: L(8) - .1, type: 'device', tr: 'lens', bg: 'var(--sun)', w: 500, x: D, y: 380, confetti: L(8) + .2, chipY: 1240,
       card: {src: 'cards-shipping/10-nani.jpg', t: L(8) + .95},
       screens: [[L(8) - .1, '01_menu_1_talk'], [L(8) + 1.0, '03_talk_4_nani_6_talking']],
       chips: [[L(9) + .05, 'Stories that end 📖']]},
      // Questions that get answered.
      {t: L(9) + 1.35, type: 'scene', tr: 'circle', bg: '#BFE6FF', rays: true, items: [
        {src: R + 'c7-amazed.png', kind: 'sticker', x: 30, y: 640, w: 680, in: 'pop'},
        {src: 'device-v2/screens/talk.png', kind: 'sticker', x: 700, y: 580, w: 310, r: 5, t: L(9) + 1.5, float: 6},
        {kind: 'label', html: 'Why is the sky blue? 🤔', x: 90, y: 440, r: -3, t: L(9) + 1.55, bg: '#fff'}]},
      // And then, bedtime.
      {t: L(10) - .1, type: 'scene', tr: 'shape', bg: '#1F2A5A', items: [
        {src: R + 'c6-pyjamas-yawn.png', kind: 'sticker', x: 190, y: 560, w: 700, in: 'pop', float: 4},
        {kind: 'label', html: '🌙 The end. Good night!', x: 250, y: 400, r: -3, t: L(10) + .5, bg: 'var(--sun)'}]},
      {t: L(11) - .15, type: 'outro', tr: 'shape', caps: false},
    ],
  };
};
