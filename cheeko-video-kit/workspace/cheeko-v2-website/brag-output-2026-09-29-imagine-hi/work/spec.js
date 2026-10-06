// V12 Imagine: "Say it. See it." Shots are tied to voice lines (L(i) = start of line i, E(i) = end). Lines: feature_lines.json V12.
window.SPEC_EN = ({L, E}) => ({
  shots: [
    {t: 0, type: 'device', bg: 'var(--purple)', w: 560, y: 290, press: [L(1) - .45],
     screens: [[0, '01_menu_2_imagine'], [L(1) - .4, 'imagine_dosa_hi_1_listening'], [L(1) + .5, 'imagine_dosa_hi_1_listening'],
               [E(1) + .12, 'imagine_dosa_hi_3_painting'], [L(2) - .05, 'imagine_dosa_hi_5_result']]},
    {t: L(3) - .12, type: 'device', bg: 'var(--green)', w: 560, y: 290,
     screens: [[L(3) - .12, 'imagine_peacock_hi_1_listening'], [E(3) + .12, 'imagine_peacock_hi_5_result']]},
    {t: L(4) - .12, type: 'device', bg: 'var(--brand)', w: 560, y: 290,
     screens: [[L(4) - .12, 'imagine_mango_hi_1_listening'], [E(4) + .12, 'imagine_mango_hi_5_result']]},
    {t: L(5) - .08, type: 'grid', bg: 'var(--sun)', items: [
      [L(5), 'imagine/im-17.jpg', 90, 300, 460, 345, -6], [L(5) + .25, 'imagine/im-16.jpg', 540, 560, 460, 345, 5], [L(5) + .5, 'imagine/im-10.jpg', 170, 830, 460, 345, -3]]},
    {t: L(6) - .08, type: 'app', src: 'app/gallery.jpg', bg: 'var(--purple)', capsY: 1600},
    {t: L(7) - .15, type: 'outro', caps: false},
  ],
  flashes: [L(2) - .05, E(3) + .12, E(4) + .12],
  bubbles: {1: {y: 1285}, 3: {y: 1285}, 4: {y: 1285}},
  outro: {cards: ['cards-shipping/07-clever-little-tales.jpg', 'cards-shipping/08-ravi-and-nila.jpg', 'cards-shipping/01-tales-of-kindness.jpg']},
});

// Hindi overrides (make_hindi_feature.py)
window.SPEC = h => { const s = window.SPEC_EN(h); s.outro = Object.assign({}, s.outro || {}, {"l1": "कम स्क्रीन।", "l2": "ज़्यादा <span class=\"hlb\">बचपन।<b></b></span> 🧡", "price": "₹5,999 · डिवाइस + 10 कार्ड", "pill": "लिंक बायो में 👆", "send": "ये उस पेरेंट को भेजो जिसे इसकी ज़रूरत है 👀"}); s.who = {kid: ['🧒 बच्चा', '#FFFFFF', '#6C3DFF'], cheeko: ['🦊 Cheeko', '#FFE3B8', '#F0521D'], nani: ['👵 नानी', '#EBDDFF', '#6C3DFF'], mitthu: ['🦜 मिट्ठू', '#D8F5D0', '#2F6B4F'], quizzy: ['🐝 क्विज़ी', '#FFF1B0', '#231A10'], grandma: ['👵 दादी', '#FFE0EC', '#C2185B']}; return s; };
