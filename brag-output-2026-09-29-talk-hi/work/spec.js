// V11 Talk: "Ask anything". Lines: feature_lines.json V11.
window.SPEC_EN = ({L, E}) => ({
  bubbleY: 1300,
  shots: [
    {t: 0, type: 'photo', src: 'live/kid-beanbag.jpg', pos: '50% 40%'},
    {t: L(1) - .1, type: 'device', bg: 'var(--sun)', w: 500, y: 430, press: [L(1) + .9, L(2) - .25],
     screens: [[L(1) - .1, '01_menu_1_talk'], [L(1) + .9, '02_talk_picker_1_cheeko'], [L(2) - .2, '03_talk_1_cheeko_4_listening'],
               [E(2) + .05, '03_talk_1_cheeko_5_thinking'], [L(3) - .05, '03_talk_1_cheeko_6_talking']]},
    {t: L(4) - .1, type: 'glyphs'},
    {t: L(5) - .1, type: 'device', bg: 'var(--ink)', w: 500, y: 430, press: [L(5) + .4, L(5) + 1.6], screens: [[L(5) - .1, '03_talk_1_cheeko_4_listening']]},
    {t: L(6) - .15, type: 'outro', caps: false},
  ],
  stickers: [{t: .3, until: 1.4, emoji: '🌤️', x: 720, y: 260, size: 150}, {t: 1.5, until: 2.8, emoji: '🐱', x: 120, y: 420, size: 150}, {t: 2.9, until: E(0), emoji: '❓', x: 740, y: 560, size: 170},
             {t: L(5) + 2.2, until: E(5) + .3, emoji: '🔒', x: 800, y: 330, size: 150}],
  outro: {l1: 'Ask anything.', l2: 'Ask <span class="hlb">Cheeko.<b></b></span> 🦊', cards: ['cards-shipping/07-clever-little-tales.jpg', 'cards-shipping/05-mitthu-the-parrot.jpg', 'cards-shipping/10-nani.jpg']},
});

// Hindi overrides (make_hindi_feature.py)
window.SPEC = h => { const s = window.SPEC_EN(h); s.outro = Object.assign({}, s.outro || {}, {"l1": "कुछ भी पूछो।", "l2": "Cheeko से <span class=\"hlb\">पूछो।<b></b></span> 🦊", "price": "₹5,999 · डिवाइस + 10 कार्ड", "pill": "लिंक बायो में 👆", "send": "ये उस पेरेंट को भेजो जिसे इसकी ज़रूरत है 👀"}); s.who = {kid: ['🧒 बच्चा', '#FFFFFF', '#6C3DFF'], cheeko: ['🦊 Cheeko', '#FFE3B8', '#F0521D'], nani: ['👵 नानी', '#EBDDFF', '#6C3DFF'], mitthu: ['🦜 मिट्ठू', '#D8F5D0', '#2F6B4F'], quizzy: ['🐝 क्विज़ी', '#FFF1B0', '#231A10'], grandma: ['👵 दादी', '#FFE0EC', '#C2185B']}; return s; };
