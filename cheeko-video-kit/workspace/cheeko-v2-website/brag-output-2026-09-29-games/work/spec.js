// V14 Eight offline games. Lines: feature_lines.json V14.
window.SPEC = ({L, E}) => ({
  shots: [
    {t: 0, type: 'device', bg: 'var(--purple)', w: 500, y: 430, screens: [[0, '04_games_menu_1_animal']], chips: [[.3, '8 games 🎮']]},
    {t: L(1) - .1, type: 'device', bg: 'var(--sun)', w: 500, y: 430, screens: [[L(1) - .1, '05_game_1_animal'], [L(1) + 1.0, '05_game_animal_correct']], chips: [[L(1), 'Animal sounds 🐮']]},
    {t: L(2) - .1, type: 'device', bg: 'var(--green)', w: 500, y: 430, screens: [[L(2) - .1, '05_game_2_numbers'], [L(2) + .9, '05_game_numbers_correct']], chips: [[L(2), 'Numbers 🔢']]},
    {t: L(3) - .1, type: 'device', bg: 'var(--ink)', w: 500, y: 430, screens: [[L(3) - .1, '05_game_3_space']], chips: [[L(3), 'Space 🚀']]},
    {t: L(4) - .1, type: 'photo', src: 'live/kid-dance.jpg', pos: '50% 30%'},
    {t: L(4) + 1.8, type: 'device', bg: 'var(--brand)', w: 500, y: 430, screens: [[L(4) + 1.8, '05_game_4_jump']], chips: [[L(4) + 1.8, 'Jump 🦘']]},
    {t: L(5) - .1, type: 'device', bg: 'var(--purple)', w: 500, y: 430,
     screens: [[L(5) - .1, '05_game_paint_stroke'], [L(5) + .75, '05_game_trace_stroke'], [L(5) + 1.5, '05_game_memory_two_flipped'], [L(5) + 2.3, '05_game_piano_key_pressed']],
     chips: [[L(5) - .1, 'Paint 🎨'], [L(5) + .75, 'Trace ✏️'], [L(5) + 1.5, 'Memory 🧠'], [L(5) + 2.3, 'Piano 🎹']]},
    {t: L(6) - .1, type: 'device', bg: 'var(--sun)', w: 500, y: 430, press: [L(6) + .45, L(6) + 1.3],
     screens: [[L(6) - .1, '04_games_menu_7_memory'], [L(6) + .45, '04_games_menu_8_piano'], [L(6) + 1.3, '04_games_menu_5_paint']]},
    {t: L(7) - .1, type: 'stamps', caps: false, items: [[L(7) - .1, 'No<br>ads.', '#F0521D'], [L(8) - .05, 'No in-app<br>purchases.', '#6C3DFF'], [L(9) - .05, 'Just<br>play! 🎉', '#2F6B4F']]},
    {t: L(10) - .15, type: 'outro', caps: false},
  ],
  outro: {cards: ['cards-shipping/02-floor-is-lava.jpg', 'cards-shipping/09-sounds-around-me.jpg', 'cards-shipping/03-play-and-sing-along.jpg']},
});
