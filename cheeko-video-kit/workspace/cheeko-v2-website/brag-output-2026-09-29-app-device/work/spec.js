// V25.2 App Guide: Device (part 2 of 5). Real app screens (Flutter widgets, iOS) on an iPhone; Cheeko's screens from firmware 2.4.311
// (theme renders: fwsim --theme). Settings reach Cheeko only after Save (PATCH -> server -> MQTT settings_update), so Cheeko changes on the Save tap.
window.SPEC = ({L, E, T}) => {
  const HI = (T.vid || '').endsWith('-HI'), tx = (en, hi) => HI ? hi : en, A = 'app-shots-ios/';
  const PH = {type: 'phone', bg: 'var(--tint)', w: 540, x: 470, y: 250, ry0: -7, ry1: -3, rx0: 3, rx1: 1, tapColor: 'var(--brand)', focusAt: [640, 700]};
  return {
    mood: 'calm', capsY: 1440, capMax: 6, capSize: 80, badge: tx('APP GUIDE · <b>2/5 DEVICE</b>', 'ऐप गाइड · <b>2/5 डिवाइस</b>'),
    shots: [
      {...PH, t: 0,
       screens: [[0, A + '01_home.png'], [.9, A + '03_device.png'], [L(2) - .1, A + '03_device_controls.png'], [L(2) + 1.0, A + '03_ctl_1_vol35.png'],
                 [L(3) + .8, A + '03_ctl_2_bri50.png'], [L(3) + 1.9, A + '03_ctl_3_picker.png'], [L(3) + 2.6, A + '03_ctl_4_night.png'], [L(5) + .9, A + '03_ctl_5_sleep.png']],
       taps: [[.5, .391, .915], [L(2) + .6, .385, .21], [L(3) + .4, .5, .29], [L(3) + 1.5, .8, .38], [L(3) + 2.25, .19, .45], [L(5) + .5, .82, .78]],
       focus: [[L(1) - .1, .5, .35, 1.5], [L(2) - .1, .45, .25, 1.55], [L(3) + 1.4, .5, .4, 1.3], [L(4) - .1, .6, .62, 1.45], [L(5) - .1, .6, .75, 1.5]],
       callouts: [
         [L(1) + .2, tx('Battery', 'बैटरी'), '80%', .8, .28, 40, 430, L(1) + 1.5],
         [L(1) + 1.5, 'Wi-Fi', tx('network', 'नेटवर्क'), .2, .43, 40, 1080, L(1) + 2.7],
         [L(1) + 2.7, tx('Last seen', 'आख़िरी बार'), tx('online', 'ऑनलाइन'), .72, .55, 40, 1080, E(1) + .25],
         [L(2) + .4, tx('Volume', 'आवाज़'), tx('turn it down', 'कम करो'), .385, .21, 40, 1080, E(2) + .25],
         [L(3) + .2, tx('Brightness', 'ब्राइटनेस'), '', .45, .29, 40, 1080, L(3) + 1.4],
         [L(3) + 2.8, tx('Theme', 'थीम'), tx('Night', 'नाइट'), .8, .38, 40, 1080, E(3) + .25],
         [L(4) + .2, tx('System sound', 'सिस्टम साउंड'), '', .82, .54, 40, 430, L(4) + 1.5],
         [L(4) + 1.5, tx('Vibration', 'वाइब्रेशन'), '', .82, .70, 40, 430, E(4) + .25],
         [L(5) + .8, tx('Sleep mode', 'स्लीप मोड'), tx('naps when idle 😴', 'खाली हो तो झपकी 😴'), .82, .78, 40, 430, E(5) + .25]]},
      {t: L(6) - .1, type: 'duo', bg: 'var(--tint)', rays: false, sb: 'dark', pw: 480, px: 40, py: 380, dw: 380, dx: 640, dy: 600, ry0: 10, ry1: 5,
       app: [[L(6) - .1, A + '03_ctl_6_save.png'], [L(6) + .75, A + '03_ctl_7_saving.png'], [L(6) + 1.5, A + '03_ctl_7_saved.png']],
       dev: [[L(6) - .1, '01_menu_1_talk'], [L(6) + 1.5, 'theme1_01_menu_1_talk']],
       taps: [[L(6) + .5, .84, .113]],
       callouts: [[L(6) + .1, tx('Save', 'सेव'), '', .84, .113, 560, 300, L(6) + 1.5],
                  [L(6) + 1.7, tx('Cheeko updates', 'Cheeko बदल गया'), tx('Night theme ✅', 'नाइट थीम ✅'), 830, 800, 560, 300, E(6) + .3]]},
      {...PH, t: L(7) - .1,
       screens: [[L(7) - .1, A + '03_device_two_toys_1kid_closed.png'], [L(7) + .9, A + '03_device_two_toys_1kid.png'], [L(8) - .1, A + '03_device_actions.png']],
       taps: [[L(7) + .5, .82, .14], [L(8) + .9, .37, .77]],
       focus: [[L(7) + .2, .7, .2, 1.6], [L(8) - .1, .45, .72, 1.4]],
       callouts: [[L(7) + 1.1, tx('Switch Cheeko', 'Cheeko बदलो'), '', .75, .185, 40, 1080, E(7) + .25],
                  [L(8) + .3, tx('Remove Device', 'डिवाइस हटाओ'), tx('progress stays', 'प्रगति बनी रहती है'), .37, .77, 40, 430, E(8) + .3]]},
      {t: L(9) - .1, type: 'title', bg: 'var(--purple)', y: 600, size: 130, caps: false, slate: true,
       html: tx('Next:<br><span class="hl">Analytics</span> <span class="e">👉</span><br><span style="font-size:60px">Part 3 of 5</span>',
                'अगला:<br><span class="hl">एनालिटिक्स</span> <span class="e">👉</span><br><span style="font-size:60px">भाग 3 / 5</span>')},
    ],
  };
};
