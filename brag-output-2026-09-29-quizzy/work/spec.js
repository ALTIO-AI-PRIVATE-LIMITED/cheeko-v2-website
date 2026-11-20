// New design + motion picks + photo swaps, 2026-09-30 (group 3 of the refresh).
// V17 Quizzy. Real question from the quiz bank (quiz_question id 1292, accepted answers include "girgit"). Lines: feature_lines.json V17.
window.SPEC = ({L, E}) => ({
  bubbleY: 1300,
  shots: [
    {t: 0, type: 'device', bg: 'var(--sun)', w: 500, y: 430, press: [L(0) + 1.1], confetti: L(3) + .6,
     screens: [[0, '02_talk_picker_2_quizzy'], [L(1) - .1, '03_talk_2_quizzy_6_talking'], [L(2) - .05, '03_talk_2_quizzy_4_listening'],
               [E(2) + .05, '03_talk_2_quizzy_5_thinking'], [L(3) - .05, '03_talk_2_quizzy_6_talking']]},
    {t: L(4) - .1, type: 'dicetitle', tr: 'whip', bg: 'var(--green)', words: ['GIRGIT', 'CHAMELEON'], roll: [L(4) + .9], size: 150, cwf: .74, y: 520, sub: '🦎 = ✅'},
    {t: L(5) - .1, type: 'photo', tr: 'shape', src: 'shoot/DSC03431.jpg', pos: '50% 45%'},
    {t: L(6) - .1, type: 'phone', tr: 'whip', bg: 'var(--purple)', w: 540, x: 270, y: 200, ry0: -10, ry1: -4, capsY: 1520, screens: [[L(6) - .1, 'app-shots-ios/06_analytics_day_quiz.png']]},
    {t: L(7) - .15, type: 'outro', tr: 'shape', caps: false},
  ],
  outro: {cards: ['cards-shipping/07-clever-little-tales.jpg', 'cards-shipping/08-ravi-and-nila.jpg', 'cards-shipping/05-mitthu-the-parrot.jpg']},
});
