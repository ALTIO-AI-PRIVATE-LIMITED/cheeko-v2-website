# Meet the device animation integration

Approved by the user on 2026-09-30.

Replace only the static annotated image in the home page's “Meet the device” section with the supplied, self-contained `assets/cheeko-device-animation` widget. Retain the existing section heading and page styling. Load its CSS and JavaScript as local assets, and point all image references at the supplied `img/` directory.

The dial advances through six supplied menu screens on click or tap; while visible, it also advances every 1.9 seconds. Labels and arrows remain legible on desktop, labels become a two-column list on narrow layouts, and reduced-motion preference disables autoplay. If JavaScript is unavailable, the initial Talk screen and labels remain visible. No other page section or backend behavior changes.

Verification: source integration tests cover placement, referenced local assets, script/style loading and responsive/motion behavior; a browser pass checks the dial and layouts when a local preview is available.
