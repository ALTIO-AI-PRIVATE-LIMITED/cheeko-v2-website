// V13 Funny Voice. Playback lines 3-7 are the kid's line through our versions of the five effects. Lines: feature_lines.json V13.
window.SPEC_EN = ({L, E}) => ({
  bubbleY: 1300,
  shots: [
    {t: 0, type: 'title', bg: 'var(--red)', y: 520, size: 190, html: 'चेतावनी <span class="e">⚠️</span>'},
    {t: L(1) - .1, type: 'device', bg: 'var(--purple)', w: 500, y: 430, press: [L(2) - .25],
     screens: [[L(1) - .1, '01_menu_4_funny_voice'], [L(1) + 1.0, '07_funny_voice_1_chipmunk'], [L(2) - .2, '07_funny_voice_1_chipmunk']]},
    {t: L(3) - .35, type: 'device', bg: 'var(--sun)', w: 500, y: 430,
     screens: [[L(3) - .35, '07_funny_voice_1_chipmunk'], [L(4) - .3, '07_funny_voice_2_monster'], [L(5) - .3, '07_funny_voice_3_robot'], [L(6) - .3, '07_funny_voice_4_echo'], [L(7) - .3, '07_funny_voice_5_speedy']],
     chips: [[L(3) - .35, 'Chipmunk 🐿️'], [L(4) - .3, 'Monster 👹'], [L(5) - .3, 'Robot 🤖'], [L(6) - .3, 'Echo 🔊'], [L(7) - .3, 'Speedy ⚡']]},
    {t: L(8) - .1, type: 'photo', src: 'live/kid-joy.jpg', pos: '50% 40%'},
    {t: L(9) - .15, type: 'outro', caps: false},
  ],
  stickers: [{t: L(8) + .4, until: E(8) + .3, emoji: '😂', x: 760, y: 280, size: 180}],
  outro: {cards: ['cards-shipping/02-floor-is-lava.jpg', 'cards-shipping/03-play-and-sing-along.jpg', 'cards-shipping/09-sounds-around-me.jpg']},
});

// Hindi overrides (make_hindi_feature.py)
window.SPEC = h => { const s = window.SPEC_EN(h); s.outro = Object.assign({}, s.outro || {}, {"l1": "कम स्क्रीन।", "l2": "ज़्यादा <span class=\"hlb\">बचपन।<b></b></span> 🧡", "price": "₹5,999 · डिवाइस + 10 कार्ड", "pill": "लिंक बायो में 👆", "send": "ये उस पेरेंट को भेजो जिसे इसकी ज़रूरत है 👀"}); s.who = {kid: ['🧒 बच्चा', '#FFFFFF', '#6C3DFF'], cheeko: ['🦊 Cheeko', '#FFE3B8', '#F0521D'], nani: ['👵 नानी', '#EBDDFF', '#6C3DFF'], mitthu: ['🦜 मिट्ठू', '#D8F5D0', '#2F6B4F'], quizzy: ['🐝 क्विज़ी', '#FFF1B0', '#231A10'], grandma: ['👵 दादी', '#FFE0EC', '#C2185B']}; return s; };
