# New Cheeko design in every video: plan (for Ravi, 2026-09-29)

Status: approved in principle; Ravi gives the go-ahead after 2026-09-30 evening. Photoshoot link to follow (future videos, not needed here).

Ravi's answers (2026-09-29): all three colours are on sale and yellow is the hero; pink and white can be used where they suit. Photos of people stay as they are. The card slides into a pocket on the back, between the body and the Cheeko logo panel, not into the top. It only goes in part of the way: from the front, the top third of the card, with its title, stays visible above Cheeko's head (Ravi's photos: the card is centred, about 73% of the device's width, and about a third of its height shows above the head). Nothing else changed apart from the speaker grill and the colour.

New renders: `~/Downloads/Cheeko New_Renders/` - Yellow, Pink, White, each as front, right side (volume +, volume -, power), left side (USB-C, headphone jack) and back (card pocket with the Cheeko logo). 3840 x 3840, transparent.

## Phase 1: new device images
- From each colour: front (the baked-in screen cleared), right side, left side, back; cropped and saved at video and thumbnail sizes.
- Measure the new screen outline and make a new screen mask, so the real firmware screens sit exactly inside (no corners poking out). Measure the knob, speaker, USB-C, headphone jack and card pocket for arrows and the knob-press ripple.
- Split the back render into two layers (body behind, logo pocket panel in front), so a card can slide into the pocket and disappear behind the panel.

## Phase 2: template changes
- Device image and proportions come from the new render; a colour option per shot (yellow by default).
- Card animation: the card slides down behind Cheeko into the back pocket and stops with its top third (the title) showing above Cheeko's head, centred, at about 73% of the device's width, exactly as in Ravi's photos (measured again from the new render before building).
- New back-view shot: the card slides down the back; its lower part tucks into the pocket behind the Cheeko logo panel while the top still sticks out above the head, with a "Card pocket" arrow.
- Side close-ups use the new side renders. The one product-only photo (the studio photo of the side, V20 and V21) is replaced by the render; every photo of people stays exactly as it is.
- One test page with every device shot type (front, card into the pocket, back view, knob press, phone and Cheeko side by side, end card, side close-ups) for Ravi to check before anything is re-rendered.

## Phase 3: script changes
- V20 Meet Cheeko:
  - "Pop a card into the card slot, and it comes alive." becomes "Slide a card into the pocket on the back, and it comes alive." The shot changes to the back view with the card going in and a "Card pocket" arrow (the old arrow pointed at the top).
  - New line: "Cheeko comes in yellow, pink and white." with the three colours side by side, after "In the box". The end card shows all three.
  - Both lines recorded with the same narrator voice and checked with speech-to-text; V20 gets about 3 s longer.
- V21 (tutorial, "Put a card on me") and V23 (first card): the card goes into the back pocket, back view.
- The onboarding plan and the production rules: the card goes into the pocket on the back.

## Colour use (yellow is the hero)
- Yellow: every main device shot, end card and thumbnail by default.
- All three colours: V20 (the new line and its end card) and the V23 and V25 end cards.
- Pink: V13 Funny Voice (its photo already shows a pink Cheeko).
- White: V15 Grandma's Voice.
- Easy to change per video if Ravi wants more or less.

## Phase 4: re-render (about 3 to 4 hours in the background)
- 32 template videos (V11-V25, English and Hindi), then re-stitch the V25 and V25-HI full films.
- 8 older videos (V01-V05, V03-HI-V05-HI) and the 4 ads (V06-V09): new device image only; their photos stay.
- Stills of every device shot checked before each render; thumbnails re-made from the new renders.
- Archive X01 stays as it is. The Bachpan film picks up the new image when it is next rendered.

## Phase 5: publish
- The current finals are kept in "older versions (old design)" first.
- Publish: the Public videos copies are replaced in place, so the website links keep working; the master sheet and the website update.
- The skill, production rules and Drive shared assets: the new renders are the only current device; the old device image is retired; the card goes into the back pocket.

Not ours to change: the parent app's home screen art still shows the old device (app team), and the website's device images (web team).

Photoshoot photos: welcome for future videos (more variety, and it helps the never-the-same-child-twice rule); not needed for this update.

## Voice (checked 2026-09-29)
- Reused everywhere. The refresh only changes pictures, so every existing voice track, caption and timing stays exactly as it is (all English and Hindi videos).
- Only V20 Meet Cheeko gets two new clips, from the same narrator (English_Upbeat_Woman, 1.05x) and checked with speech-to-text: "Slide a card into the pocket on the back, and it comes alive." (replaces "Pop a card into the card slot, and it comes alive.") and the new "Cheeko comes in yellow, pink and white." The other V20 clips are reused; the voice track is rebuilt from the clips, about 3 s longer.
- Every script was checked for colour, grill and card-position words: nothing else needs changing ("Put a card on me", "Pop in a card", "A big speaker" stay true; V17's "colour" is the chameleon question, V25.2's is the screen theme).
- Music is re-made on each render as before (same tune); V20's follows its new length.

## Approved setup (V20 pilot signed off by Ravi, 2026-09-29)

Everything below lives in the shared template (`marketing/tools/feature/feature.html`), so every video picks it up when re-rendered.

- **Device:** the new renders (`assets/img/device-v2/`), yellow by default (`deviceColor` per video, `color` per shot). Proportions 3619/2162.
- **Screen fit:** mask measured from the render's black glass (`device_v2_mask.py`), saved as RGBA because CSS masks use the alpha channel (a grey PNG clipped nothing and left black corners). Firmware screens fill the glass; card art (any picture that is not a firmware screen) is cropped, never stretched, showing the top with the title.
- **Card:** 68% of the front's width (74% of the back view), centred on the body (47%; the side buttons stick out on the right), top third above the head. It glides down behind Cheeko into the back pocket, no drop or bounce. From the back it is cut along the measured, slightly slanted pocket edge.
- **Motion picks:** T1 circle wipe (default), T2 lens iris, T3 card swipe, T4 screen portal, T5 whip pan, T6 Cheeko-shape wipe; A2 turntable, A4 card wheel, A5 card deck, A6 screen pop-out, A7 dice-roll title, A8 Imagine vortex. Not used: T7 tile flip, A1 three-colour flip, A3 two-view card sketch.
- **Thumbnails:** device images rebuilt from the new render (`thumbs-work/make_dev_v2.py`, yellow, pink, white).
- **V20:** two new voice lines (back pocket, three colours), turntable tour, trio, card wheel round Cheeko, tiger pop-out, portal, whip and shape transitions; 55.3 s.

## Rollout order (from 2026-09-29)

Videos in list order, starting with V01; each one is checked on stills, rendered and sent before the next. Photos of people stay as they are.

## Progress
- 2026-09-29 V01 Everything Cheeko Does: re-rendered on the new design (hook and end card; card into the back pocket, art cropped on the screen; thumbnail rebuilt). Test copy in Drive `3 Test`; the old final is kept in `4 Final/older versions (old design)`. Not published yet (public copies are replaced in one go in Phase 5, together with the approved V20).

## Photos showing the old grill (Ravi, 2026-09-30)
- Don't pick a photo where the old device's speaker grill is clearly visible (the grill is the one visible change). Fine: no device, back or side, grill hidden by hands, and a really good photo where the device is small in the frame or held so the grill doesn't really show (Ravi, same day). Photos stay unedited.
- This narrows "photos stay as they are": during the refresh, each video's photos are checked, and any that show the old grill are replaced from the photoshoot library (`marketing/photoshoot/small-2400/`, template path `shoot/`), keeping "never the same child twice".
- Already known: V01's parent app photo (`live/s2-manage-content.jpg`) shows the old device on the sofa, so V01 gets a new photo there. V26's three photos were checked and pass.
