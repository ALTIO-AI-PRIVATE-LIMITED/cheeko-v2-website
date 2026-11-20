// V27 One More Bite (2026-10-01). The number one real pattern: no bite without rhymes on the phone (marketing/v08-research-kids-and-phones.md).
// Stickers: assets/img/ravi-stories/ (sheet B, plus A1 for Mumma with the spoon). Feed: ravi-stories/feed.png (made up, no brands).
// Lines: feature_lines.json V27; line 1 is Mumma (speech bubble, Gemini Kore in Hinglish, Ravi's pick). Cheeko's screen: Night (template default).
window.SPEC_EN = ({L, E}) => {
  const R = 'ravi-stories/', D = 540 - 500 * .47, FEED = R + 'feed.png';
  return {
    mood: 'bright', capsY: 1500, deviceColor: 'yellow',
    who: {mumma: ['👩 Mumma', '#FFE0EC', '#F0521D']}, bubbles: {1: {y: 250}},
    shots: [
      // Dinner time at Ravi's house.
      {t: 0, type: 'scene', bg: '#FFE7A8', rays: true, items: [
        {src: R + 'b1-dinner-wide.png', kind: 'sticker', x: 50, y: 560, w: 980, in: 'pop', t: .05},
        {kind: 'label', html: '🕗 8:00 PM', x: 110, y: 380, r: -4, t: .5, bg: '#fff'}]},
      // One more bite, Ravi!  (Mumma)
      {t: L(1) - .1, type: 'scene', tr: 'whip', bg: '#FFD6C2', rays: true, items: [
        {src: R + 'a1-dinner-phone.png', kind: 'sticker', x: 70, y: 560, w: 940, in: 'pop', zoom: 1.04}]},
      // The rhyme ends. The next one starts on its own. And the next. And the next.
      {t: L(2) - .1, type: 'phone', tr: 'lens', w: 520, x: 280, y: 220, ry0: -12, ry1: -5, rx0: 4, rx1: 2,
       screens: [[L(2) - .1, FEED, [0, 0, 0, 0], null, 'light'],
                 [L(2) + 1.35, FEED, [L(2) + 1.35, L(2) + 1.75, 0, 20], null, 'light'],
                 [L(3) - .05, FEED, [L(3) - .05, L(3) + .3, 20, 40], null, 'light'],
                 [L(3) + .7, FEED, [L(3) + .7, L(3) + 1.0, 40, 60], null, 'light']],
       tags: [[L(2) + .4, 'अगला वीडियो 3, 2, 1', 70, 300, '#fff', 'var(--ink)', -5], [L(3) + .1, 'ऑटोप्ले 🔁', 640, 1180, 'var(--brand)', '#fff', 4]]},
      // Five minutes becomes forty.
      {t: L(4) - .1, type: 'scene', tr: 'whip', bg: '#E8E0FF', rays: true, items: [
        {src: R + 'b2-hamster.png', kind: 'sticker', x: 50, y: 560, w: 470, in: 'pop'},
        {src: R + 'b3-mumma-tired.png', kind: 'sticker', x: 470, y: 600, w: 580, in: 'pop', t: L(4) + .2},
        {kind: 'label', html: '⏱ 5 मिनट', x: 110, y: 380, r: -4, t: L(4), out: L(4) + .95, bg: '#fff', size: 64},
        {kind: 'stamp', html: '⏱ 40 मिनट', x: 110, y: 350, r: -6, t: L(4) + .95, size: 96}]},
      // The plate? Still full.
      {t: L(5) - .1, type: 'scene', tr: 'whip', bg: '#CFE3F5', rays: true, items: [
        {src: R + 'b4-cold-thali.png', kind: 'sticker', x: 120, y: 600, w: 840, in: 'pop', wob: 1},
        {kind: 'label', html: 'दाल: ठंडी ❄️', x: 560, y: 420, r: 4, t: L(5) + .9, bg: 'var(--ink)', color: '#fff'}]},
      // Tonight, meet Cheeko. (the Nani card goes into the back pocket, Nani starts talking)
      {t: L(6) - .1, type: 'device', tr: 'lens', bg: '#2A1F4F', rays: false, w: 500, x: D, y: 380, confetti: L(6) + .2,
       card: {src: 'cards-shipping/10-nani.jpg', t: L(6) + 1.3},
       screens: [[L(6) - .1, '00_home_clock'], [L(6) + 1.35, '14_card_reveal_hello_nani'], [L(7) - .1, '03_talk_4_nani_6_talking']]},
      // Nani tells a tale. His eyes on his plate, his ears on the story.
      {t: L(7) + 1.0, type: 'scene', tr: 'circle', bg: '#FFE7A8', rays: true, items: [
        {src: R + 'b5-eating-listening.png', kind: 'sticker', x: 30, y: 620, w: 660, in: 'pop'},
        {src: 'device-v2/screens/nani.png', kind: 'sticker', x: 690, y: 560, w: 320, r: 5, t: L(7) + 1.2, float: 6},
        {kind: 'label', html: '👀 थाली', x: 110, y: 420, r: -4, t: L(7) + 1.9, bg: '#fff'},
        {kind: 'label', html: '👂 कहानी', x: 690, y: 420, r: 4, t: L(7) + 2.7, bg: 'var(--purple)', color: '#fff'}]},
      // Plate? Empty.
      {t: L(8) - .1, type: 'scene', tr: 'whip', bg: 'var(--sun)', rays: true, items: [
        {src: R + 'b6-clean-plate.png', kind: 'sticker', x: 190, y: 520, w: 700, in: 'pop'},
        {kind: 'stamp', html: 'सब ख़त्म!', x: 430, y: 360, r: 7, t: L(8) + .75, size: 96, color: 'var(--green)'}]},
      // Dinner comes with a story now. Not a screen.
      {t: L(9) - .1, type: 'scene', tr: 'shape', bg: '#FFD6C2', rays: true, items: [
        {src: R + 'b7-parents-dinner.png', kind: 'sticker', x: 30, y: 640, w: 1020, in: 'pop'},
        {kind: 'label', html: 'आख़िरकार डिनर 💛', x: 120, y: 460, r: -4, t: L(9) + .6, bg: '#fff'}]},
      {t: L(10) - .15, type: 'outro', tr: 'shape', caps: false},
    ],
  };
};

// Hindi overrides (make_hindi_feature.py)
window.SPEC = h => { const s = window.SPEC_EN(h); s.outro = Object.assign({}, s.outro || {}, {"l1": "कम स्क्रीन।", "l2": "ज़्यादा <span class=\"hlb\">बचपन।<b></b></span> 🧡", "price": "₹5,999 · डिवाइस + 10 कार्ड", "pill": "लिंक बायो में 👆", "send": "ये उस पेरेंट को भेजो जिसे इसकी ज़रूरत है 👀"}); s.who = {kid: ['🧒 बच्चा', '#FFFFFF', '#6C3DFF'], cheeko: ['🦊 Cheeko', '#FFE3B8', '#F0521D'], nani: ['👵 नानी', '#EBDDFF', '#6C3DFF'], mitthu: ['🦜 मिट्ठू', '#D8F5D0', '#2F6B4F'], quizzy: ['🐝 क्विज़ी', '#FFF1B0', '#231A10'], grandma: ['👵 दादी', '#FFE0EC', '#C2185B'], mumma: ['👩 मम्मा', '#FFE0EC', '#F0521D']}; return s; };
