// V15 Make Your Own card: "Grandma's voice, on demand". Lines: feature_lines.json V15.
window.SPEC_EN = ({L, E}) => ({
  bubbleY: 1300,
  shots: [
    {t: 0, type: 'photo', src: 'live/girl-holding.jpg', pos: '50% 30%'},
    {t: L(1) - .1, type: 'grid', bg: 'var(--pink)', items: [[L(1), 'cards-shipping/06-make-your-own.jpg', 290, 230, 500, 787, -4]]},
    {t: L(2) - .1, type: 'app', src: 'app/custom-card.jpg', bg: 'var(--brand)', capsY: 1600},
    {t: L(3) - .1, type: 'device', bg: 'var(--sun)', w: 500, y: 430, card: {src: 'cards-shipping/06-make-your-own.jpg', t: L(3) + .9},
     screens: [[0, '01_menu_1_talk'], [L(3) + .95, 'content_play_1_reveal'], [L(3) + 1.6, 'content_play_2b_downloading'], [L(4) - .1, 'content_play_3_item1']]},
    {t: L(5) - .1, type: 'photo', src: 'live/kid-hug.jpg', pos: '45% 40%'},
    {t: L(6) - .1, type: 'photo', src: 'bedtime_world.jpg', pos: '50% 40%'},
    {t: L(7) - .1, type: 'title', bg: 'var(--brand)', y: 560, size: 140, html: '10 क्लिप रिकॉर्ड करो।<br><span class="hl">हमेशा</span> सुनो <span class="e">❤️</span>', caps: false},
    {t: L(8) - .15, type: 'outro', caps: false},
  ],
  bubbles: {5: {y: 1180}},
  outro: {cards: ['cards-shipping/06-make-your-own.jpg', 'cards-shipping/10-nani.jpg', 'cards-shipping/04-dreamy-melodies.jpg']},
});

// Hindi overrides (make_hindi_feature.py)
window.SPEC = h => { const s = window.SPEC_EN(h); s.outro = Object.assign({}, s.outro || {}, {"l1": "कम स्क्रीन।", "l2": "ज़्यादा <span class=\"hlb\">बचपन।<b></b></span> 🧡", "price": "₹5,999 · डिवाइस + 10 कार्ड", "pill": "लिंक बायो में 👆", "send": "ये उस पेरेंट को भेजो जिसे इसकी ज़रूरत है 👀"}); s.who = {kid: ['🧒 बच्चा', '#FFFFFF', '#6C3DFF'], cheeko: ['🦊 Cheeko', '#FFE3B8', '#F0521D'], nani: ['👵 नानी', '#EBDDFF', '#6C3DFF'], mitthu: ['🦜 मिट्ठू', '#D8F5D0', '#2F6B4F'], quizzy: ['🐝 क्विज़ी', '#FFF1B0', '#231A10'], grandma: ['👵 दादी', '#FFE0EC', '#C2185B']}; return s; };
