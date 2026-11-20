// V29 Quiet Back Seat (2026-10-02). Ravi's own car trip: his son plays with a white Cheeko on headphones in the back seat.
// Photos: assets/img/car-trip/ (Ravi's, git-ignored; cropped to the boy, the car brand on the headrests blurred out).
// The headphone jack is on Cheeko's left side (turntable 'left', measured spot .415/.51). Lines: feature_lines.json V29.
window.SPEC = ({L, E}) => {
  const C = 'car-trip/', D = 540 - 500 * .47;
  const playlist = `<div style="width:620px;background:#14141a;border-radius:44px;padding:40px 40px 30px;box-shadow:0 30px 60px rgba(0,0,0,.45);font-family:var(--body);color:#fff">
    <div style="font:800 30px/1 var(--body);opacity:.6;letter-spacing:.08em">PLAYLIST</div>
    <div style="font:900 58px/1.1 var(--disp);margin:14px 0 26px">Papa's Old Songs 🎶</div>
    ${['Long Drive Classics', 'Highway Melodies', 'Sunday Morning Hits', 'Golden Oldies, Vol. 2'].map((t, i) =>
      `<div style="display:flex;align-items:center;gap:22px;padding:16px 0;border-top:1px solid rgba(255,255,255,.12);font:700 36px/1.2 var(--body)">
        <span style="width:70px;height:70px;border-radius:14px;background:hsl(${30 + i * 70} 70% 55%);display:flex;align-items:center;justify-content:center;font-size:34px">🎵</span>${t}</div>`).join('')}
  </div>`;
  return {
    mood: 'bright', capsY: 1500, deviceColor: 'white',
    shots: [
      // Long drive. Two minutes in, the back seat wants the phone. (car-nohp.jpg: Ravi's photo before the headphones, sparkle mark cropped off)
      {t: 0, type: 'scene', bgImg: C + 'car-nohp.jpg', bgPos: '60% 40%', bgFilter: 'blur(9px) brightness(.72)', items: [
        {kind: 'label', html: '🚗 Km 2 of 300', x: 90, y: 300, r: -4, t: .25, bg: 'var(--sun)', size: 64},
        {kind: 'label', html: '"Papa, phone do na!" 📱', x: 120, y: 640, r: 3, t: 1.5, bg: '#fff', size: 70}]},
      // No phone. You hand him Cheeko. / Stories, rhymes, games.
      {t: L(1) - .1, type: 'device', tr: 'lens', bg: 'var(--sun)', w: 500, x: D, y: 380, confetti: L(1) + .3, chipY: 1240,
       screens: [[L(1) - .1, '00_home_clock'], [L(1) + .5, '03_talk_1_cheeko_6_talking'], [L(2) - .05, '03_talk_4_nani_6_talking'],
                 [L(2) + .55, 'cards-shipping/large/03-play-and-sing-along.jpg'], [L(2) + 1.05, '04_games_menu_1_animal']],
       chips: [[L(2), 'Stories 📖'], [L(2) + .55, 'Rhymes 🎵'], [L(2) + 1.05, 'Games 🎮']]},
      // He's thrilled.
      {t: L(2) + 1.7, type: 'scene', tr: 'circle', bgImg: C + 'car-nohp.jpg', bgPos: '60% 35%', items: [
        {kind: 'label', html: '🎮 8 offline games<br>Highway approved ✅', x: 90, y: 280, r: -4, t: L(2) + 1.9, bg: '#fff', size: 54}]},
      // Same rhyme. Same car. 47th time. (No real song titles: we don't hold the rights. Parents sticker: Ravi's own, made in ChatGPT from his photos.)
      {t: L(3) - .1, type: 'scene', tr: 'whip', bg: '#FFD6C2', rays: true, items: [
        {src: C + 'parents-car.png', kind: 'sticker', x: 50, y: 440, w: 980, in: 'pop', wob: 1.2},
        {kind: 'label', html: '🎵 La la la, la la loo!', x: 90, y: 300, r: -4, t: L(3) + .15, bg: '#fff', size: 56},
        {kind: 'stamp', html: '×47', x: 690, y: 1180, r: 9, t: L(4) - .95, size: 130}]},
      // Papa's old songs playlist? Cancelled.
      {t: L(4) - .1, type: 'scene', tr: 'whip', bg: '#1E2A44', items: [
        {html: playlist, x: 230, y: 330, r: -3, in: 'pop'},
        {kind: 'stamp', html: 'CANCELLED', x: 200, y: 640, r: -12, t: L(5) - .9, size: 120}]},
      // Then Papa remembers. Cheeko has a headphone jack!
      {t: L(5) - .1, type: 'turntable', tr: 'whip', h: 880, y: 330, views: [[L(5) - .1, 'left']],
       callouts: [[L(6) - 1.3, 'Headphone jack 🎧', 'any wired headphones', .415, .51, 40, 1100]]},
      // Headphones on. Rhymes in. Peace out.
      {t: L(6) - .1, type: 'scene', tr: 'lens', bgImg: C + 'car-headphones.jpg', bgPos: '50% 30%', items: [
        {kind: 'label', html: '😎 Do not disturb', x: 380, y: 300, r: 4, t: L(6) + 1.8, bg: 'var(--sun)', size: 60}]},
      // He gets every story. You get your drive back.
      {t: L(7) - .1, type: 'scene', tr: 'circle', bgImg: C + 'car-smile.jpg', bgPos: '50% 25%', items: [
        {kind: 'label', html: '🎧 His stories', x: 90, y: 1180, r: -4, t: L(7) + .3, bg: '#fff', size: 58},
        {kind: 'label', html: '🚗 Our drive', x: 600, y: 1300, r: 4, t: L(7) + 1.7, bg: 'var(--sun)', size: 58}]},
      // Well, almost. The only noise left in the car? Papa's singing. / Honestly? I want headphones too!
      // (Ravi's second sticker, parents-singing.png, replaced his selfie on 2026-10-02.)
      {t: L(8) - .1, type: 'scene', tr: 'whip', bg: 'var(--sun)', rays: true, items: [
        {src: C + 'parents-singing.png', kind: 'sticker', x: 50, y: 440, w: 980, in: 'pop', wob: 1.2},
        {kind: 'label', html: '🎤 Papa, live!', x: 90, y: 300, r: -5, t: L(9) - 1.1, bg: 'var(--ink)', color: '#fff', size: 62},
        {kind: 'label', html: '🙉 "Headphones, please!"', x: 280, y: 1250, r: 3, t: L(9) + .2, bg: '#fff', size: 52}]},
      {t: L(10) - .15, type: 'outro', tr: 'shape', caps: false},
    ],
    outro: {color: 'white'},
  };
};
