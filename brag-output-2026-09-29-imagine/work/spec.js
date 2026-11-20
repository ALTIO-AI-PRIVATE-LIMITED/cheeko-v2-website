// New design + motion picks + photo swaps, 2026-09-30 (group 3 of the refresh).
// V12 Imagine: "Say it. See it." Shots are tied to voice lines (L(i) = start of line i, E(i) = end). Lines: feature_lines.json V12.
window.SPEC = ({L, E}) => ({
  shots: [
    {t: 0, type: 'device', bg: 'var(--purple)', w: 560, y: 290, press: [L(1) - .45],
     screens: [[0, '01_menu_2_imagine'], [L(1) - .4, 'imagine_dosa_1_listening'], [L(1) + .5, 'imagine_dosa_2_listening_transcript'],
               [E(1) + .12, 'imagine_dosa_3_painting'], [L(2) - .05, 'imagine_dosa_5_result']],
     popout: {t: L(2) + .35, src: 'imagine/im-17.jpg', to: [240, 120, 600]}},
    {t: L(3) - .12, type: 'device', tr: 'whip', bg: 'var(--green)', w: 560, y: 290,
     screens: [[L(3) - .12, 'imagine_peacock_2_listening_transcript'], [E(3) + .12, 'imagine_peacock_5_result']]},
    {t: L(4) - .12, type: 'device', tr: 'whip', bg: 'var(--brand)', w: 560, y: 290,
     screens: [[L(4) - .12, 'imagine_mango_2_listening_transcript'], [E(4) + .12, 'imagine_mango_5_result']]},
    {t: L(5) - .08, type: 'vortex', tr: 'portal', screen: 'imagine_mango_5_result', items: ['imagine/im-17.jpg', 'imagine/im-16.jpg', 'imagine/im-10.jpg', 'imagine/im-05.jpg', 'imagine/im-07.jpg', 'imagine/im-13.jpg']},
    {t: L(6) - .08, type: 'phone', tr: 'shape', bg: 'var(--purple)', w: 540, x: 270, y: 200, ry0: -10, ry1: -4, screens: [[L(6) - .08, 'app-shots-ios/07_gallery.png']], capsY: 1520},
    {t: L(7) - .15, type: 'outro', tr: 'shape', caps: false},
  ],
  flashes: [L(2) - .05, E(3) + .12, E(4) + .12],
  bubbles: {1: {y: 1285}, 3: {y: 1285}, 4: {y: 1285}},
  outro: {cards: ['cards-shipping/07-clever-little-tales.jpg', 'cards-shipping/08-ravi-and-nila.jpg', 'cards-shipping/01-tales-of-kindness.jpg']},
});
