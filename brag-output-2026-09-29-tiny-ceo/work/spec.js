// V08 Tiny CEO (remade 2026-09-30; the first version by Codex was replaced at Ravi's request).
// Deadpan first half: a five-year-old picks up the grown-up internet from your phone. Warm second half: Cheeko.
// Stickers: assets/img/tinyceo/ (cut from the Tiny CEO sprite sheet). The feed on the phone is made up (tinyceo/feed.html), no real brands.
// Lines: feature_lines.json V08.
window.SPEC = ({L, E}) => {
  const T = 'tinyceo/', D = 540 - 500 * .47, FEED = T + 'feed.png';
  return {
    mood: 'bright', capsY: 1500, deviceColor: 'yellow',
    shots: [
      // Meet Aarav. Age five. Wants passive income.
      {t: 0, type: 'scene', bg: '#1E2A44', rays: true, items: [
        {src: T + 'beanbag-ceo.png', kind: 'sticker', x: 170, y: 420, w: 740, in: 'pop', t: .05, float: 6},
        {kind: 'label', html: 'Aarav · age 5', x: 90, y: 290, r: -4, t: .85, bg: '#fff'},
        {kind: 'stamp', html: 'Passive income', x: 120, y: 1150, r: -7, t: 2.1, size: 88}]},
      // His portfolio? Three crayons.
      {t: L(1) - .1, type: 'scene', tr: 'whip', bg: 'var(--sun)', rays: true, items: [
        {src: T + 'crayon-portfolio.png', kind: 'sticker', x: 190, y: 420, w: 720, in: 'pop'},
        {kind: 'label', html: 'Portfolio: 3 crayons 🖍️', x: 110, y: 1190, r: -3, t: L(1) + 1.2, bg: 'var(--ink)', color: '#fff'}]},
      // One of them he found under the sofa. (close-up on the crayon cup)
      {t: L(2) - .1, type: 'scene', tr: 'lens', bg: '#FFE7A8', items: [
        {src: T + 'crayon-portfolio.png', kind: 'sticker', x: 293, y: -40, w: 1124, in: 'pop', zoom: 1.04},
        {kind: 'label', html: '🛋️ Found under the sofa', x: 90, y: 1190, r: 3, t: L(2) + .8, bg: '#fff'},
        {kind: 'stamp', html: 'Rare asset', x: 560, y: 930, r: 8, t: L(2) + 1.35, size: 78}]},
      // How did we get here?
      {t: L(3) - .1, type: 'scene', tr: 'whip', bg: '#FFD6C2', rays: true, items: [
        {src: T + 'parents.png', kind: 'sticker', x: 210, y: 400, w: 700, in: 'pop', wob: 2},
        {kind: 'label', html: 'Parents: confused', x: 120, y: 1190, r: -4, t: L(3) + .35, bg: 'var(--ink)', color: '#fff'}]},
      // You gave him your phone. For five minutes. And your feed came with it. Home loans. Anti-ageing cream. The 4 AM club.
      {t: L(4) - .1, type: 'phone', tr: 'whip', w: 520, x: 280, y: 220, ry0: -12, ry1: -5, rx0: 4, rx1: 2,
       screens: [[L(4) - .1, FEED, [0, 0, 0, 0], null, 'light'],
                 [L(6) - .12, FEED, [L(6) - .12, L(6) + .2, 0, 25], null, 'light'],
                 [L(7) - .1, FEED, [L(7) - .1, L(7) + .2, 25, 50], null, 'light'],
                 [L(8) - .1, FEED, [L(8) - .1, L(8) + .2, 50, 75], null, 'light']],
       tags: [[L(4) + .35, 'Your phone', 50, 300, 'var(--sun)', 'var(--ink)', -5], [L(4) + 1.4, '⏱ 5 min', 740, 260, '#fff', 'var(--ink)', 6],
              [L(5) + .1, 'Your feed', 640, 1180, 'var(--brand)', '#fff', 4]]},
      // Nursery by day. Midlife crisis by night.
      {t: L(9) - .1, type: 'scene', tr: 'whip', bg: '#BFE6FF', rays: true, items: [
        {src: T + 'crayon-portfolio.png', kind: 'sticker', x: 190, y: 430, w: 700, in: 'pop'},
        {kind: 'label', html: '☀️ 9 AM · Nursery', x: 100, y: 290, r: -4, t: L(9) + .1, bg: '#fff'}]},
      {t: L(10) - .1, type: 'scene', tr: 'whip', bg: '#10162E', items: [
        {src: T + 'beanbag-ceo.png', kind: 'sticker', x: 170, y: 430, w: 740, in: 'pop', float: 4},
        {kind: 'label', html: '🌙 11 PM', x: 100, y: 290, r: 4, t: L(10) + .1, bg: '#fff'},
        {kind: 'stamp', html: 'Midlife crisis', x: 150, y: 1160, r: -6, t: L(10) + .45, size: 88}]},
      // Let's give him his childhood back.
      {t: L(11) - .1, type: 'scene', tr: 'shape', bg: 'var(--sun)', rays: true, items: [
        {src: T + 'moon-kid.png', kind: 'sticker', x: 230, y: 520, w: 640, in: 'pop', float: 8},
        {kind: 'label', html: '💛 Back to being five', x: 130, y: 1190, r: -3, t: L(11) + .8, bg: 'var(--ink)', color: '#fff'}]},
      // Meet Cheeko. Stories. Questions. Play.
      {t: L(12) - .1, type: 'device', tr: 'lens', bg: 'var(--brand)', w: 500, x: D, y: 400, confetti: L(12) + .2,
       card: {src: 'cards-shipping/01-tales-of-kindness.jpg', t: L(12) + .75},
       screens: [[L(12) - .1, '03_talk_1_cheeko_6_talking'], [L(12) + .8, 'cards-shipping/large/01-tales-of-kindness.jpg']]},
      {t: L(13) - .1, type: 'cardwheel', tr: 'card', device: '03_talk_1_cheeko_6_talking', cy: 820},
      // No videos. No feed. No ads.
      {t: L(14) - .1, type: 'stamps', tr: 'whip', caps: false, items: [[L(14) - .1, 'No<br>videos.', '#F0521D'], [L(14) + .9, 'No<br>feed.', '#6C3DFF'], [L(14) + 1.85, 'No<br>ads.', '#2F6B4F']]},
      // Let him ask why the moon follows him,
      {t: L(15) - .1, type: 'scene', tr: 'shape', bg: '#1F2A5A', items: [
        {src: T + 'moon-kid.png', kind: 'sticker', x: 80, y: 700, w: 640, in: 'pop'},
        {src: 'device-v2/screens/talk.png', kind: 'sticker', x: 700, y: 820, w: 300, r: 6, t: L(15) + .3, float: 8},
        {src: T + 'moon-bubble.png', kind: 'sticker', x: 500, y: 300, w: 400, t: L(15) + .9, float: 10}]},
      // not why his portfolio is down.
      {t: L(16) - .1, type: 'scene', tr: 'whip', bg: 'var(--tint)', items: [
        {src: T + 'crayon-portfolio.png', kind: 'sticker', x: 60, y: 560, w: 620, r: -3, in: 'pop'},
        {kind: 'stamp', html: '▼ 33%', x: 620, y: 420, r: 7, t: L(16) + .55, size: 96},
        {kind: 'label', html: 'Crayons: 3 → 2', x: 580, y: 650, r: -3, t: L(16) + .95, bg: 'var(--ink)', color: '#fff'}]},
      {t: L(17) - .15, type: 'outro', tr: 'shape', caps: false},
    ],
  };
};
