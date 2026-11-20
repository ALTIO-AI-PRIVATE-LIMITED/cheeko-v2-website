// V16 Nani, the storyteller. Lines: feature_lines.json V16.
window.SPEC_EN = ({L, E}) => ({
  bubbleY: 1300,
  shots: [
    {t: 0, type: 'device', bg: '#3B1F4F', w: 500, y: 430, card: {src: 'cards-shipping/10-nani.jpg', t: L(0) + 1.3},
     screens: [[0, '01_menu_1_talk'], [L(0) + 1.35, '14_card_reveal_hello_nani'], [L(1) - .1, '03_talk_4_nani_6_talking'],
               [L(2) - .05, '03_talk_4_nani_4_listening'], [E(2) + .05, '03_talk_4_nani_5_thinking'], [L(3) - .05, '03_talk_4_nani_6_talking']]},
    {t: L(4) - .1, type: 'photo', src: 'live/mom-daughter.jpg', pos: '42% 50%'},
    {t: L(5) - .1, type: 'device', bg: '#6B2F4F', w: 500, y: 430, card: {src: 'cards-shipping/10-nani.jpg', t: L(5) - .6}, screens: [[L(5) - .1, '03_talk_4_nani_6_talking']]},
    {t: L(6) - .1, type: 'photo', src: 'bedtime_world.jpg', pos: '50% 40%'},
    {t: L(7) - .15, type: 'outro', caps: false},
  ],
  stickers: [{t: L(5) + 1.2, until: E(5) + .3, emoji: '🔖', x: 790, y: 1020, size: 170}],
  outro: {cards: ['cards-shipping/10-nani.jpg', 'cards-shipping/07-clever-little-tales.jpg', 'cards-shipping/01-tales-of-kindness.jpg']},
});

// Hindi overrides (make_hindi_feature.py)
window.SPEC = h => { const s = window.SPEC_EN(h); s.outro = Object.assign({}, s.outro || {}, {"l1": "कम स्क्रीन।", "l2": "ज़्यादा <span class=\"hlb\">बचपन।<b></b></span> 🧡", "price": "₹5,999 · डिवाइस + 10 कार्ड", "pill": "लिंक बायो में 👆", "send": "ये उस पेरेंट को भेजो जिसे इसकी ज़रूरत है 👀"}); s.who = {kid: ['🧒 बच्चा', '#FFFFFF', '#6C3DFF'], cheeko: ['🦊 Cheeko', '#FFE3B8', '#F0521D'], nani: ['👵 नानी', '#EBDDFF', '#6C3DFF'], mitthu: ['🦜 मिट्ठू', '#D8F5D0', '#2F6B4F'], quizzy: ['🐝 क्विज़ी', '#FFF1B0', '#231A10'], grandma: ['👵 दादी', '#FFE0EC', '#C2185B']}; return s; };
