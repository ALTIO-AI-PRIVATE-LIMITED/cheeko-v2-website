# /brag plan: Cheeko (v2, fast and fun)

**Format:** vertical 1080×1920, 30fps · **Tone:** playful and punchy (bright colour-block scenes, bouncy pops, hard slide cuts) · **Length:** 22s at 120 BPM (1 beat = 0.5s)

## Angle

Show everything Cheeko does, fast. Each feature gets one bright scene lasting three beats. Every scene slides in from a new direction, and a pop that climbs the scale plays on each cut.

## Storyboard

| Time | Scene | On screen |
|---|---|---|
| 0.0-2.5 | **Hook**, cream | The Tales of Kindness card slams into the device on beat 1 and confetti bursts. **"Insert a card." / "Stories play!"** |
| 2.5-4.0 | **Cards**, orange | "In the box". **10 story cards** fan out (Lava, Play & Sing, Ravi, Clever, Storytime). |
| 4.0-5.5 | **Talk**, sun | **Ask anything.** Cheeko the fox and Quizzy Bee bounce in with "?" and "!" bubbles. |
| 5.5-7.0 | **Imagine**, ink | **Say it. See it.** Three Cheeko drawings drop in on the beat (tiger on a bicycle, auto rickshaw to the moon, robot cooking dosa). |
| 7.0-8.5 | **Games**, purple | **8 games, all offline.** Fox with a controller, plus chips for Animal Sounds, Numbers, Space, Jump and Trace. |
| 8.5-10.0 | **Languages**, green | **English + 10 Indian.** Tiles pop in: अ ಅ அ అ অ A. |
| 10.0-11.5 | **Radio**, cream | **Kid-safe channels.** Fox in headphones, bouncing equaliser, ON AIR. |
| 11.5-13.0 | **Funny Voice**, pink | **Instant giggles.** Fox with a megaphone and a wobbling "hellooo!". |
| 13.0-14.5 | **Parent app**, white | **You see everything.** The real parent app photo. |
| 14.5-17.0 | **Manifesto**, orange | "No video. No feed. No ads." over a drum breakdown, then **"All play."** lands with the drop. |
| 17.0-22.0 | **Outro**, cream | Logo, device with cards fanned out and confetti. **Less screen, more childhood.** "₹5,999 · Device + 10 cards · Free delivery across India", then **cheekoai.in**. |

## Sound

The soundtrack is original and synthesised for this video: D major at 120 BPM, with the progression D-A-Bm-G. It has a bouncy octave bass, a marimba off-beat skank, a glockenspiel hook, and four-on-the-floor kick with claps and hats. The sound effects are tuned to the key: a whoosh on every slide, a pop that climbs the scale per feature, boings for the Talk bubbles and Funny Voice, a radio crackle, and confetti sparkles. The track resolves on D at 20s.

## Honesty check

- All copy is from `index.html`.
- "Once" has been removed from the price, because Talk and Imagine become an optional plan after 3 months.
- The site's ship date is left out because it has already passed.


**Updated 2026-09-28:** every card is now the real shipping card from `assets/img/cards-shipping/` (Ravi's Drive folder); story worlds use the card's own art, blurred.

**Updated 2026-09-28 (current firmware UI):** the device now shows the real current screens rendered from firmware b05c95d (FW 2.4.311, `assets/img/device_current.png` and `assets/img/fw-screens/`) instead of the old dark Talk screen.

**Updated 2026-09-29 (new device design):** the hook and end card use the new yellow render (`assets/img/device-v2/yellow_front.png`) with the measured screen mask inlined in `compose.html`. The card glides down behind Cheeko into the back pocket (68% of the body's width, centred at 47%, top third with the title above the head), no drop or bounce, and its art then fills the screen, cropped. In the end card the centre card sits in the pocket and the other two fan out behind. The thumbnail uses `thumbs-work/dev2/menu.png`. The parent app photo is a photo of people, so it stays as it is. Old design final kept in Drive `4 Final/older versions (old design)`.
