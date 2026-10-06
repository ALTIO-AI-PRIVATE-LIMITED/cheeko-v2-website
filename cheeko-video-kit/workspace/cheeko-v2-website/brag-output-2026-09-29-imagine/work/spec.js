// V12 Imagine: "Say it. See it." Shots are tied to voice lines (L(i) = start of line i, E(i) = end). Lines: feature_lines.json V12.
window.SPEC = ({L, E}) => ({
  shots: [
    {t: 0, type: 'device', bg: 'var(--purple)', w: 560, y: 290, press: [L(1) - .45],
     screens: [[0, '01_menu_2_imagine'], [L(1) - .4, 'imagine_dosa_1_listening'], [L(1) + .5, 'imagine_dosa_2_listening_transcript'],
               [E(1) + .12, 'imagine_dosa_3_painting'], [L(2) - .05, 'imagine_dosa_5_result']]},
    {t: L(3) - .12, type: 'device', bg: 'var(--green)', w: 560, y: 290,
     screens: [[L(3) - .12, 'imagine_peacock_2_listening_transcript'], [E(3) + .12, 'imagine_peacock_5_result']]},
    {t: L(4) - .12, type: 'device', bg: 'var(--brand)', w: 560, y: 290,
     screens: [[L(4) - .12, 'imagine_mango_2_listening_transcript'], [E(4) + .12, 'imagine_mango_5_result']]},
    {t: L(5) - .08, type: 'grid', bg: 'var(--sun)', items: [
      [L(5), 'imagine/im-17.jpg', 90, 300, 460, 345, -6], [L(5) + .25, 'imagine/im-16.jpg', 540, 560, 460, 345, 5], [L(5) + .5, 'imagine/im-10.jpg', 170, 830, 460, 345, -3]]},
    {t: L(6) - .08, type: 'app', src: 'app/gallery.jpg', bg: 'var(--purple)', capsY: 1600},
    {t: L(7) - .15, type: 'outro', caps: false},
  ],
  flashes: [L(2) - .05, E(3) + .12, E(4) + .12],
  bubbles: {1: {y: 1285}, 3: {y: 1285}, 4: {y: 1285}},
  outro: {cards: ['cards-shipping/07-clever-little-tales.jpg', 'cards-shipping/08-ravi-and-nila.jpg', 'cards-shipping/01-tales-of-kindness.jpg']},
});
