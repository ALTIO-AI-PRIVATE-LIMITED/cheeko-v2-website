// V25.3 App Guide: Analytics (part 3 of 5). Real app screens (Flutter widgets, iOS) on an iPhone.
window.SPEC = ({L, E, T}) => {
  const HI = (T.vid || '').endsWith('-HI'), tx = (en, hi) => HI ? hi : en, A = 'app-shots-ios/';
  const PH = {type: 'phone', bg: 'var(--tint)', w: 540, x: 470, y: 250, ry0: -7, ry1: -3, rx0: 3, rx1: 1, tapColor: 'var(--brand)', focusAt: [640, 700]};
  return {
    mood: 'calm', capsY: 1440, capMax: 6, capSize: 80, badge: tx('APP GUIDE · <b>3/5 ANALYTICS</b>', 'ऐप गाइड · <b>3/5 एनालिटिक्स</b>'),
    shots: [
      {...PH, t: 0,
       screens: [[0, A + '01_home.png'], [.9, A + '06_analytics_day.png'], [L(2) + .7, A + '06_analytics_activity_detail.png'],
                 [L(3) - .1, A + '06_analytics_day_quiz.png'], [L(4) + .6, A + '06_analytics_week_breakdown.png'], [L(5) - .1, A + '06_analytics_week_picker.png']],
       taps: [[.5, .608, .915], [L(2) + .3, .35, .585], [L(4) + .2, .72, .22]],
       focus: [[L(1) - .1, .42, .34, 1.7], [L(2) + .1, .45, .58, 1.4], [L(2) + .8, .5, .72, 1.3], [L(3) - .1, .42, .5, 1.45],
               [L(4) - .05, .6, .25, 1.3], [L(4) + .7, .45, .35, 1.35], [L(5) - .1, .45, .55, 1.3], [E(5) + .2, .5, .5, 1]],
       callouts: [
         [L(1) + .2, tx('Play time', 'खेलने का समय'), '48 min', .2, .3, 40, 430, L(1) + 1.3],
         [L(1) + 1.3, tx('Success rate', 'सफलता'), '86%', .62, .3, 40, 430, L(1) + 2.4],
         [L(1) + 2.4, tx('Streak', 'स्ट्रीक'), tx('5 days', '5 दिन'), .2, .385, 40, 1040, L(1) + 3.5],
         [L(1) + 3.5, tx('Questions', 'सवाल'), tx('asked today', 'आज पूछे'), .62, .385, 40, 1040, E(1) + .25],
         [L(3) + .4, tx('Every answer', 'हर जवाब'), '', .07, .62, 40, 1100, L(3) + 2.3],
         [L(3) + 2.3, tx('7 right · 1 revealed', '7 सही · 1 बताया'), '', .42, .39, 40, 420, E(3) + .25],
         [L(4) + .9, tx('Each day', 'हर दिन'), '', .6, .17, 40, 420, L(4) + 2.2],
         [L(4) + 2.2, tx('Where time went', 'समय कहाँ गया'), '', .2, .53, 40, 1100, E(4) + .25],
         [L(5) + .2, tx('12 weeks back', '12 हफ़्ते पीछे'), '', .3, .7, 40, 1080, E(5) + .25]]},
      {t: L(6) - .1, type: 'title', bg: 'var(--green)', y: 600, size: 120, caps: false, slate: true,
       html: tx('Next:<br><span class="hl">Gallery &amp; cards</span> <span class="e">👉</span><br><span style="font-size:60px">Part 4 of 5</span>',
                'अगला:<br><span class="hl">गैलरी और कार्ड</span> <span class="e">👉</span><br><span style="font-size:60px">भाग 4 / 5</span>')},
    ],
  };
};
