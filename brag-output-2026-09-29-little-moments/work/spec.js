// V07 Little Moments, More Connection (remade 2026-09-30; the first version by Codex was replaced at Ravi's request).
// Four everyday struggles as the family drawings (assets/img/moments/, cut from Ravi's family sheet with the new Cheeko painted in),
// then Cheeko answers each one with real families from the August shoot (assets/img/shoot/). Lines: feature_lines.json V07.
// Children: T1+T2 (03042), G1+B2 (02553), G4 (03203), G3 (02912), T4 (03290): never the same child twice.
window.SPEC = ({L, E}) => {
  const M = 'moments/', D = 540 - 500 * .47;
  const struggle = (t, img, bg, label, r) => ({t, type: 'scene', tr: 'whip', bg, rays: true, items: [
    {src: M + img, kind: 'card', x: 120, y: 300, w: 840, h: 810, r, in: 'pop', zoom: 1.06},
    {kind: 'label', html: label, x: 520, y: 1120, r: -r * 1.5, t: t + .3, size: 54}]});
  return {
    mood: 'bright', capsY: 1450, deviceColor: 'yellow',
    shots: [
      // hook: the four struggles drop in as a pile of cards
      {t: 0, type: 'scene', bg: 'var(--sun)', rays: true, items: [
        {src: M + '03-waiting.jpg', kind: 'card', x: 50, y: 250, w: 480, h: 462, r: -8, in: 'drop', t: .12},
        {src: M + '05-rainy-day.jpg', kind: 'card', x: 550, y: 300, w: 480, h: 470, r: 6, in: 'drop', t: .32, from: [300, -1100]},
        {src: M + '07-whys.jpg', kind: 'card', x: 70, y: 770, w: 480, h: 470, r: 5, in: 'drop', t: .52, from: [-300, -1100]},
        {src: M + '09-not-sleepy.jpg', kind: 'card', x: 540, y: 810, w: 480, h: 462, r: -5, in: 'drop', t: .72}]},
      struggle(L(1) - .1, '03-waiting.jpg', '#7FA8FF', '⏳ Minute 47', -3),
      struggle(L(2) - .1, '05-rainy-day.jpg', '#5E7E9E', '🌧️ Day 3 indoors', 3),
      struggle(L(3) - .1, '07-whys.jpg', 'var(--purple)', '❓ Why #100', -2),
      struggle(L(4) - .1, '09-not-sleepy.jpg', '#1F2A5A', '🕘 9:45 PM', 3),
      // the turn: the new Cheeko, a story card glides into the back pocket
      {t: L(5) - .1, type: 'device', tr: 'lens', bg: 'var(--sun)', w: 500, x: D, y: 380, confetti: L(5) + .25,
       card: {src: 'cards-shipping/01-tales-of-kindness.jpg', t: L(6) - .15},
       screens: [[L(5) - .1, '03_talk_1_cheeko_6_talking'], [L(6) - .1, 'cards-shipping/large/01-tales-of-kindness.jpg']]},
      // waiting -> story time: two toddlers, each with a Cheeko (the screen opens into the photo)
      {t: L(6) + .3, type: 'scene', tr: 'portal', bg: '#FFE7A8', items: [
        {src: 'shoot/DSC03042.jpg', kind: 'card', x: 45, y: 420, w: 990, h: 660, r: -3, in: 'pop', zoom: 1.05, pos: '45% 55%'},
        {kind: 'label', html: '📖 Story time', x: 110, y: 1140, r: -4, t: L(6) + .7, bg: 'var(--brand)', color: '#fff'}]},
      // rainy day -> eight games on Cheeko, then the family on the floor
      {t: L(7) - .1, type: 'device', tr: 'whip', bg: 'var(--purple)', w: 500, x: D, y: 360, chipY: 1240,
       screens: [[L(7) - .1, '04_games_menu_1_animal'], [L(7) + .3, '04_games_menu_2_numbers'], [L(7) + .6, '04_games_menu_3_space'], [L(7) + .9, '04_games_menu_5_paint'], [L(7) + 1.2, '05_game_4_jump']],
       chips: [[L(7) + .35, '8 games 🎮']]},
      {t: L(7) + 1.8, type: 'scene', tr: 'circle', bg: 'var(--green)', items: [
        {src: 'shoot/DSC02553.jpg', kind: 'card', x: 45, y: 420, w: 990, h: 660, r: 3, in: 'pop', zoom: 1.05},
        {kind: 'label', html: '📶 No Wi-Fi needed', x: 470, y: 1140, r: 4, t: L(7) + 2.2}]},
      // a hundred whys -> the curious girl, her questions pop around her, Cheeko loves them
      {t: L(8) - .1, type: 'scene', tr: 'shape', bgImg: 'shoot/DSC03203.jpg', bgPos: '50% 30%', items: [
        {kind: 'label', html: 'Why is the sky blue?', x: 60, y: 230, r: -4, t: L(8) + .3, bg: '#fff', size: 46},
        {kind: 'label', html: 'Why do cats purr?', x: 420, y: 390, r: 3, t: L(8) + .8, bg: '#fff', size: 46},
        {kind: 'label', html: 'Why does the moon follow us?', x: 70, y: 550, r: -2, t: L(8) + 1.3, bg: '#fff', size: 46},
        {src: 'device-v2/screens/talk.png', kind: 'sticker', x: 700, y: 900, w: 300, r: 6, t: L(8) + 1.6, float: 8}]},
      // bedtime -> the Nani card goes in, then the lamp-lit bedtime photo
      {t: L(9) - .1, type: 'device', tr: 'lens', bg: '#2A1F4F', rays: false, w: 500, x: D, y: 380,
       card: {src: 'cards-shipping/10-nani.jpg', t: L(9) + .85},
       screens: [[L(9) - .1, '00_home_clock'], [L(9) + .9, '14_card_reveal_hello_nani'], [L(9) + 1.3, '03_talk_4_nani_6_talking']]},
      {t: L(9) + 1.55, type: 'photo', tr: 'circle', src: 'shoot/DSC02912.jpg', pos: '50% 55%'},
      // the best part: parents dancing with their baby
      {t: L(10) - .1, type: 'photo', tr: 'card', src: 'shoot/DSC03290.jpg', pos: '50% 40%'},
      // LITTLE MOMENTS rolls into MORE CONNECTION
      {t: L(11) - .1, type: 'dicetitle', tr: 'shape', bg: 'var(--brand)', words: ['LITTLE|MOMENTS', 'MORE|CONNECTION'], roll: [L(11) + 1.05], size: 132, cwf: .72, y: 760, caps: false},
      {t: L(12) - .15, type: 'outro', tr: 'shape', caps: false},
    ],
  };
};
