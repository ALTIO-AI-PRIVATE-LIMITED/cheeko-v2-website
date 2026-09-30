Cheeko "Meet the device" animation
===================================

The dial on the device turns one notch every 1.9 seconds and the screen steps
through the real Cheeko main menu: TALK, IMAGINE, GAMES, FUNNY VOICE, RADIO,
SETTINGS. Visitors can also click or tap the dial to turn it themselves.

Open index.html to see it (double-click works, no server needed).

Files
  index.html        demo page
  snippet.html      the three pieces to paste into your own page
  device-anim.css   styles (the screen mask is built in)
  device-anim.js    the animation, no libraries
  img/              device, dial and the six menu screens (WebP)

To add it to a page
  1. Copy device-anim.css, device-anim.js and the img folder next to your page.
  2. Paste the three parts of snippet.html into your page.
  3. If img/ lives somewhere else, change the img/ paths in the section.

Good to know
  - Width: the section fills its parent, up to 1120 px. Below 640 px wide the
    labels become a two-column list under the device.
  - It only animates while the device is on screen and the tab is visible.
  - People who turn on "reduce motion" see it standing still on TALK.
  - The labels and arrows are real text, so edit the words in the section.
    Each label's data-fx / data-fy is where its arrow points on the device
    (0 to 1 across and down the device picture).
