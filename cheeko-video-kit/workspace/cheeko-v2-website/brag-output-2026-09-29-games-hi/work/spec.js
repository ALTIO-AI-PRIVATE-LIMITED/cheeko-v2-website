// V14 Eight offline games. Lines: feature_lines.json V14.
window.SPEC_EN = ({L, E}) => ({
  shots: [
    {t: 0, type: 'device', bg: 'var(--purple)', w: 500, y: 430, screens: [[0, '04_games_menu_1_animal']], chips: [[.3, '8 गेम्स 🎮']]},
    {t: L(1) - .1, type: 'device', bg: 'var(--sun)', w: 500, y: 430, screens: [[L(1) - .1, '05_game_1_animal'], [L(1) + 1.0, '05_game_animal_correct']], chips: [[L(1), 'जानवर 🐮']]},
    {t: L(2) - .1, type: 'device', bg: 'var(--green)', w: 500, y: 430, screens: [[L(2) - .1, '05_game_2_numbers'], [L(2) + .9, '05_game_numbers_correct']], chips: [[L(2), 'गिनती 🔢']]},
    {t: L(3) - .1, type: 'device', bg: 'var(--ink)', w: 500, y: 430, screens: [[L(3) - .1, '05_game_3_space']], chips: [[L(3), 'स्पेस 🚀']]},
    {t: L(4) - .1, type: 'photo', src: 'live/kid-dance.jpg', pos: '50% 30%'},
    {t: L(4) + 1.8, type: 'device', bg: 'var(--brand)', w: 500, y: 430, screens: [[L(4) + 1.8, '05_game_4_jump']], chips: [[L(4) + 1.8, 'जंप 🦘']]},
    {t: L(5) - .1, type: 'device', bg: 'var(--purple)', w: 500, y: 430,
     screens: [[L(5) - .1, '05_game_paint_stroke'], [L(5) + .75, '05_game_trace_stroke'], [L(5) + 1.5, '05_game_memory_two_flipped'], [L(5) + 2.3, '05_game_piano_key_pressed']],
     chips: [[L(5) - .1, 'पेंट 🎨'], [L(5) + .75, 'ट्रेस ✏️'], [L(5) + 1.5, 'मेमोरी 🧠'], [L(5) + 2.3, 'पियानो 🎹']]},
    {t: L(6) - .1, type: 'device', bg: 'var(--sun)', w: 500, y: 430, press: [L(6) + .45, L(6) + 1.3],
     screens: [[L(6) - .1, '04_games_menu_7_memory'], [L(6) + .45, '04_games_menu_8_piano'], [L(6) + 1.3, '04_games_menu_5_paint']]},
    {t: L(7) - .1, type: 'stamps', caps: false, items: [[L(7) - .1, 'ना<br>ऐड्स।', '#F0521D'], [L(8) - .05, 'ऐप में कोई<br>खरीदारी नहीं।', '#6C3DFF', 130], [L(9) - .05, 'बस<br>खेलो! 🎉', '#2F6B4F']]},
    {t: L(10) - .15, type: 'outro', caps: false},
  ],
  outro: {cards: ['cards-shipping/02-floor-is-lava.jpg', 'cards-shipping/09-sounds-around-me.jpg', 'cards-shipping/03-play-and-sing-along.jpg']},
});

// Hindi overrides (make_hindi_feature.py)
window.SPEC = h => { const s = window.SPEC_EN(h); s.outro = Object.assign({}, s.outro || {}, {"l1": "कम स्क्रीन।", "l2": "ज़्यादा <span class=\"hlb\">बचपन।<b></b></span> 🧡", "price": "₹5,999 · डिवाइस + 10 कार्ड", "pill": "लिंक बायो में 👆", "send": "ये उस पेरेंट को भेजो जिसे इसकी ज़रूरत है 👀"}); s.who = {kid: ['🧒 बच्चा', '#FFFFFF', '#6C3DFF'], cheeko: ['🦊 Cheeko', '#FFE3B8', '#F0521D'], nani: ['👵 नानी', '#EBDDFF', '#6C3DFF'], mitthu: ['🦜 मिट्ठू', '#D8F5D0', '#2F6B4F'], quizzy: ['🐝 क्विज़ी', '#FFF1B0', '#231A10'], grandma: ['👵 दादी', '#FFE0EC', '#C2185B']}; return s; };
