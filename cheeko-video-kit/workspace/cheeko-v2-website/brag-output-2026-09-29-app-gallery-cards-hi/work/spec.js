// V25.4 App Guide: Gallery and custom cards (part 4 of 5). Real app screens (Flutter widgets, iOS) on an iPhone; Cheeko's screens from firmware 2.4.311.
window.SPEC = ({L, E, T}) => {
  const HI = (T.vid || '').endsWith('-HI'), tx = (en, hi) => HI ? hi : en, A = 'app-shots-ios/';
  const PH = {type: 'phone', bg: 'var(--tint)', w: 540, x: 470, y: 250, ry0: -7, ry1: -3, rx0: 3, rx1: 1, tapColor: 'var(--brand)', focusAt: [640, 700]};
  return {
    mood: 'calm', capsY: 1440, capMax: 6, capSize: 80, badge: tx('APP GUIDE · <b>4/5 GALLERY &amp; CARDS</b>', 'ऐप गाइड · <b>4/5 गैलरी और कार्ड</b>'),
    shots: [
      {...PH, t: 0,
       screens: [[0, A + '07_gallery.png'], [L(1) + .6, A + '07_gallery_viewer.png', null, null, 'light'], [L(2) + .55, A + '07_gallery_select.png'],
                 [L(3) - .1, A + '10_profile.png'], [L(3) + 1.0, A + '08_custom_card_list.png'], [L(4) + .6, A + '08_custom_card_recording.png'],
                 [L(4) + 3.2, A + '08_custom_card_list.png'], [L(5) - .1, A + '08_image_editor_top.png'], [L(5) + 1.3, A + '08_image_editor.png']],
       taps: [[L(1) + .2, .17, .22], [L(2) + .1, .5, .22], [L(3) + .6, .47, .69], [L(4) + .2, .57, .874], [L(5) + 1.0, .86, .79]],
       focus: [[L(1) + .7, .35, .9, 1.35], [L(2) + .6, .6, .2, 1.4], [L(3) - .1, .5, .69, 1.4], [L(3) + 1.1, .5, .45, 1.2],
               [L(4) + .6, .5, .62, 1.3], [L(4) + 3.2, .5, .77, 1.35], [L(5) - .1, .5, .5, 1.1], [L(5) + 1.3, .55, .79, 1.45], [E(5) + .2, .5, .5, 1]],
       callouts: [
         [L(0) + .6, tx('Everything they imagined', 'हर कल्पना'), '', .5, .3, 40, 1080, E(0) + .2],
         [L(1) + 1.1, tx('Save', 'सेव'), tx('to your phone', 'फ़ोन में'), .2, .9, 40, 470, L(1) + 2.1],
         [L(1) + 2.1, tx('Share', 'शेयर'), tx('with family', 'परिवार के साथ'), .47, .9, 40, 470, E(1) + .25],
         [L(2) + 1.0, tx('Save or share', 'सेव या शेयर'), tx('a few at once', 'एक साथ कई'), .88, .1, 40, 1080, E(2) + .25],
         [L(3) + .2, tx('Custom cards', 'कस्टम कार्ड'), '', .47, .69, 40, 1080, L(3) + 1.0],
         [L(3) + 1.3, tx('Your recordings', 'आपकी रिकॉर्डिंग'), tx('3 of 10', '10 में से 3'), .88, .3, 40, 430, E(3) + .25],
         [L(4) + 1.0, tx('Record', 'रिकॉर्ड'), tx('up to 10 min each', 'हर एक 10 मिनट तक'), .5, .6, 40, 1080, L(4) + 3.2],
         [L(4) + 3.3, tx('Upload audio', 'ऑडियो अपलोड'), 'MP3, WAV', .45, .77, 40, 430, E(4) + .25],
         [L(5) + .2, tx('Crop', 'क्रॉप'), '', .49, .54, 40, 1080, L(5) + 1.3],
         [L(5) + 1.4, tx('Filters', 'फ़िल्टर'), '', .6, .79, 40, 430, E(5) + .25]]},
      {t: L(6) - .1, type: 'device', bg: 'var(--green)', w: 520, x: 280, y: 330, card: {src: 'cards-shipping/06-make-your-own.jpg', t: L(6) + 1.6}, chipY: 1215,
       screens: [[L(6) - .1, '00_home_clock'], [L(6) + 1.6, 'content_play_1_reveal'], [L(6) + 2.4, 'content_play_3_item1']],
       chips: [[L(6) + 2.5, tx('Your voice plays ❤️', 'आपकी आवाज़ ❤️')]]},
      {t: L(7) - .1, type: 'title', bg: 'var(--purple)', y: 600, size: 130, caps: false, slate: true,
       html: tx('Next:<br><span class="hl">Profile</span> <span class="e">👉</span><br><span style="font-size:60px">Part 5 of 5</span>',
                'अगला:<br><span class="hl">प्रोफ़ाइल</span> <span class="e">👉</span><br><span style="font-size:60px">भाग 5 / 5</span>')},
    ],
  };
};
