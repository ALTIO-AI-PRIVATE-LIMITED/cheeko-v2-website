// V17 Quizzy. Real question from the quiz bank (quiz_question id 1292, accepted answers include "girgit"). Lines: feature_lines.json V17.
window.SPEC = ({L, E}) => ({
  bubbleY: 1300,
  shots: [
    {t: 0, type: 'device', bg: 'var(--sun)', w: 500, y: 430, press: [L(0) + 1.1], confetti: L(3) + .6,
     screens: [[0, '02_talk_picker_2_quizzy'], [L(1) - .1, '03_talk_2_quizzy_6_talking'], [L(2) - .05, '03_talk_2_quizzy_4_listening'],
               [E(2) + .05, '03_talk_2_quizzy_5_thinking'], [L(3) - .05, '03_talk_2_quizzy_6_talking']]},
    {t: L(4) - .1, type: 'title', bg: 'var(--green)', y: 420, size: 130, html: '"Girgit" <span class="e">🦎</span><br>= <span class="hl">chameleon</span> <span class="e">✅</span>'},
    {t: L(5) - .1, type: 'photo', src: 'live/quizzy-girl.jpg', pos: '50% 40%'},
    {t: L(6) - .1, type: 'app', src: 'app/home-quiz.jpg', bg: 'var(--purple)', capsY: 1600},
    {t: L(7) - .15, type: 'outro', caps: false},
  ],
  outro: {cards: ['cards-shipping/07-clever-little-tales.jpg', 'cards-shipping/08-ravi-and-nila.jpg', 'cards-shipping/05-mitthu-the-parrot.jpg']},
});
