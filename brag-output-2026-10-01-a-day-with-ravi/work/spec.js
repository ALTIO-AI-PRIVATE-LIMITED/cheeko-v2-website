// V08 A Day With Ravi (2026-10-01, replaces Tiny CEO). Every moment is a real, recurring parent story (marketing/v08-research-kids-and-phones.md).
// Stickers: assets/img/ravi-stories/ (Ravi's ChatGPT/Codex sheets, cut with marketing/tools/cut_sheet.py). The feed on the phone is made up
// (ravi-stories/feed.html: traditional rhymes, no real brands). Lines: feature_lines.json V08. Cheeko's screen: Night (template default).
window.SPEC = ({L, E}) => {
  const R = 'ravi-stories/', D = 540 - 500 * .47, FEED = R + 'feed.png';
  return {
    mood: 'bright', capsY: 1500, deviceColor: 'yellow',
    shots: [
      // Meet Ravi. Age four.
      {t: 0, type: 'scene', bg: '#FFE7A8', rays: true, items: [
        {src: R + 'cast-ravi.png', kind: 'sticker', x: 300, y: 380, w: 480, in: 'pop', t: .05, float: 6},
        {kind: 'label', html: 'Ravi · age 4 👦', x: 110, y: 290, r: -4, t: .7, bg: '#fff'}]},
      // Won't eat a bite without rhymes.
      {t: L(1) - .1, type: 'scene', tr: 'whip', bg: '#FFD6C2', rays: true, items: [
        {src: R + 'a1-dinner-phone.png', kind: 'sticker', x: 70, y: 470, w: 940, in: 'pop'},
        {kind: 'label', html: 'Bites eaten: 0 🍛', x: 560, y: 330, r: 4, t: L(1) + .9, bg: 'var(--ink)', color: '#fff'}]},
      // Swipes his storybook. (then taps it harder)
      {t: L(2) - .1, type: 'scene', tr: 'whip', bg: '#BFE6FF', rays: true, items: [
        {src: R + 'a2-book-swipe.png', kind: 'sticker', x: 170, y: 440, w: 740, in: 'pop', out: L(2) + .6},
        {src: R + 'a3-book-tap.png', kind: 'sticker', x: 150, y: 430, w: 780, in: 'pop', t: L(2) + .6, wob: 1.5},
        {kind: 'stamp', html: 'Tap tap TAP', x: 560, y: 330, r: 7, t: L(2) + .75, size: 76}]},
      // Checks Nanaji's pocket before saying hi.
      {t: L(3) - .1, type: 'scene', tr: 'card', bg: '#D8F5D0', rays: true, items: [
        {src: R + 'a4-nanaji-pocket.png', kind: 'sticker', x: 90, y: 400, w: 900, in: 'pop'},
        {kind: 'label', html: 'Nanaji is home! 👴', x: 90, y: 280, r: -4, t: L(3) + .1, bg: '#fff'},
        {kind: 'label', html: 'Phone found 📱', x: 600, y: 1210, r: 4, t: L(3) + 1.5, bg: 'var(--brand)', color: '#fff'}]},
      // Answers Dadi Maa in cartoon English.
      {t: L(4) - .1, type: 'scene', tr: 'whip', bg: '#FFE0EC', rays: true, items: [
        {src: R + 'a5-dadi-english.png', kind: 'sticker', x: 80, y: 480, w: 920, in: 'pop'},
        {kind: 'label', html: 'Beta, khana khaya?', x: 60, y: 300, r: -3, t: L(4) + .15, bg: '#fff'},
        {kind: 'label', html: 'Yes Granny, totally! 😎', x: 420, y: 400, r: 3, t: L(4) + 1.1, bg: 'var(--sun)'}]},
      // Phone goes away? The whole building hears it.
      {t: L(5) - .1, type: 'scene', tr: 'whip', bg: '#FFB8A8', rays: true, items: [
        {src: R + 'a6-meltdown.png', kind: 'sticker', x: 90, y: 470, w: 900, in: 'pop', wob: 2.5},
        {kind: 'stamp', html: 'WAAAAH!', x: 130, y: 330, r: -7, t: L(5) + 1.1, size: 110}]},
      // Five minutes of rhymes. Autoplay did the rest.
      {t: L(6) - .1, type: 'phone', tr: 'lens', w: 520, x: 280, y: 220, ry0: -12, ry1: -5, rx0: 4, rx1: 2,
       screens: [[L(6) - .1, FEED, [0, 0, 0, 0], null, 'light'],
                 [L(7) - .15, FEED, [L(7) - .15, L(7) + .25, 0, 20], null, 'light'],
                 [L(7) + .45, FEED, [L(7) + .45, L(7) + .8, 20, 40], null, 'light'],
                 [L(7) + .95, FEED, [L(7) + .95, L(7) + 1.25, 40, 60], null, 'light'],
                 [L(7) + 1.35, FEED, [L(7) + 1.35, L(7) + 1.6, 60, 80], null, 'light']],
       tags: [[L(6) + .2, '⏱ 5 min', 70, 300, '#fff', 'var(--ink)', -5],
              [L(7) + .5, '⏱ 25 min', 70, 300, '#fff', 'var(--ink)', -5],
              [L(7) + 1.0, '⏱ 50 min', 70, 300, 'var(--sun)', 'var(--ink)', -5],
              [L(7) + 1.4, '⏱ 1 hr 12 min 😳', 70, 300, 'var(--red)', '#fff', -5],
              [L(7) + .1, 'Autoplay 🔁', 640, 1180, 'var(--brand)', '#fff', 4]]},
      // Meet Cheeko. Stories, questions and play.
      {t: L(8) - .1, type: 'device', tr: 'lens', bg: 'var(--sun)', w: 500, x: D, y: 380, confetti: L(8) + .2, chipY: 1240,
       card: {src: 'cards-shipping/01-tales-of-kindness.jpg', t: L(8) + .95},
       screens: [[L(8) - .1, '03_talk_1_cheeko_6_talking'], [L(8) + 1.0, 'cards-shipping/large/01-tales-of-kindness.jpg']],
       chips: [[L(9) + .05, 'Stories 📖'], [L(9) + .75, 'Questions ❓'], [L(9) + 1.5, 'Play 🎲']]},
      // No videos. No feed. No ads.
      {t: L(9) + 2.2, type: 'stamps', tr: 'whip', caps: false, items: [[L(9) + 2.2, 'No<br>videos.', '#F0521D'], [L(9) + 2.95, 'No<br>feed.', '#6C3DFF'], [L(9) + 3.65, 'No<br>ads.', '#2F6B4F']]},
      // Let him ask why the moon follows him. Not for one more video.
      {t: L(10) - .1, type: 'scene', tr: 'shape', bg: '#1F2A5A', items: [
        {src: R + 'a8-laugh-point.png', kind: 'sticker', x: 40, y: 700, w: 640, in: 'pop'},
        {src: 'device-v2/screens/talk.png', kind: 'sticker', x: 690, y: 700, w: 300, r: 6, t: L(10) + .3, float: 8},
        {src: 'tinyceo/moon-bubble.png', kind: 'sticker', x: 470, y: 250, w: 420, t: L(10) + .8, float: 10}]},
      {t: L(11) - .15, type: 'outro', tr: 'shape', caps: false},
    ],
  };
};
