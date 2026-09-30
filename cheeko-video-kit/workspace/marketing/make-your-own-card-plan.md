# V26 Make Your Own Card: storyboard (draft for Ravi, 2026-09-30)

Ravi's brief: first the complete flow (upload the audio, add the picture, the card goes in), then the emotional side: loved ones, their favourite content, and playing it again and again.

Vertical 1080x1920 Reel, about 50 s. New design (yellow hero, card into the back pocket). Narrator English_Upbeat_Woman 1.05x; Hindi after the English is approved.

## Facts checked in the code (app feat/daily-streak d49af42, firmware cheeko-os-v2)

- Way in: Profile tab, "Add Custom Cards". Screen "Create Custom Card", "3 of 10 recordings", "Add Media".
- Audio: "Upload Audio" (MP3, WAV, max 10 MB) or "Record Voice" (up to 10 minutes; Tap the mic, Recording, Re-record / Use Recording).
- A "Content rights" check (tick, I Agree) comes before the first upload or picture.
- Picture (optional): Gallery or Camera, then "Adjust Image": drag to crop, rotate, zoom, filters (Original, Brightness, Grayscale, Sepia, Saturation, Blur, Invert), "Use This Picture". Shown as "Fitted to 296 x 240".
- Save: "Add to Custom Card", then "Saved. Cheeko picks it up the next time the card is tapped."
- Up to 10 recordings per child. A recording can be opened and its audio or picture replaced. No reorder, no delete in the app (we do not mention either).
- On Cheeko: the card goes into the back pocket; first time "Getting ... ready" with a progress bar, then each recording plays with its picture on the screen.
- Knob: turn for next or previous, press to pause. At the end the card loops back to the first recording (autoplay is on by default).
- Saved on Cheeko's SD card, so it plays without Wi-Fi once it has been fetched. New recordings need Wi-Fi the next time the card goes in.
- The Make Your Own card is one of the 10 cards in the box.
- The app's own sample card already has the three themes: "Grandma's lullaby", "Good morning song", "Story: the thirsty crow".

## Storyboard

| # | Time | Voice | Line | On screen |
|---|---|---|---|---|
| 1 | 0-2.5 | N (excited) | Your voice, on a Cheeko card! | Dice-roll title "Make Your Own"; the card glides into Cheeko's back pocket, a sound wave pulses on the screen |
| **Part 1: how it works** | | | | |
| 2 | 2.5-6 | N (happy) | Open the Cheeko app. Tap Profile, then Add Custom Cards. | iPhone flies in on Profile, tap ripple and curved arrow on "Add Custom Cards", Create Custom Card opens |
| 3 | 6-9 | N (happy) | Upload a song or story, MP3 or WAV. | Tap "Upload Audio"; the rights check flashes (tick, I Agree); "Good morning song" drops into the list |
| 4 | 9-13 | N (calm) | Or record your voice right in the app. | Record Voice sheet: tap the mic, waveform, "Use Recording" |
| 5 | 13-17 | N (happy) | Add a picture. Crop it, pick a filter. | Gallery, Adjust Image: drag to crop, filters flick past, "Use This Picture" |
| 6 | 17-19.5 | N (happy) | Tap Add to Custom Card. Done! | Tap, "Uploading", toast "Saved. Cheeko picks it up..."; "3 of 10 recordings" |
| 7 | 19.5-23 | N (happy) | Now slide the card into Cheeko's back pocket. | Turntable: back view, the card glides into the pocket, Cheeko turns to the front (portal from the phone's screen into Cheeko's) |
| 8 | 23-26 | Mom (happy) | Good morning, sunshine! Time to wake up! | "Getting ready" bar, then the peacock picture fills Cheeko's screen, speaker pulses |
| 9 | 26-29 | N (happy) | Turn the knob for the next one. Up to ten on a card! | Knob ripple, screen changes to the thirsty crow; chip "1 of 10" |
| **Part 2: why it matters** | | | | |
| 10 | 29-31 | N (soft) | Grandma lives far away? | Photo: grandparent with a child |
| 11 | 31-34 | N (warm) | Record her lullaby on your next visit. | Phone recording beside Grandma (photo or app close-up) |
| 12 | 34-37 | Grandma (calm) | Sleep now, my little star. | Night scene: Cheeko by the bed, Grandma's picture on the screen |
| 13 | 37-40 | N (happy) | Their favourite song. The story only you tell. It's all on the card. | Quick cuts: peacock, crow, a parent reading (photo) |
| 14 | 40-41 | Kid (excited) | Again! Again! | Kid photo, bouncy stickers |
| 15 | 41-45 | N (playful) | Again and again? Cheeko never gets tired. It even plays without Wi-Fi. | Loop counter 1x, 2x, 3x ... 27x, Wi-Fi-off icon, Cheeko keeps playing |
| 16 | 45-47.5 | N (happy) | The Make Your Own card comes in the box! | Card wheel: the 10 cards spin round Cheeko, Make Your Own stops in front |
| 17 | 47.5-50 | N (happy) | Cheeko. Less screen, more childhood! | Standard end card, yellow Cheeko with the card in the pocket |

About 130 words spoken. Different lines and scenes from V15 Grandma's Voice (that one is a 20 s emotional Reel; this is the full how-to).

## Motion (approved picks)

A7 dice-roll title (hook), T4 screen portal (phone to Cheeko), A2 turntable (card into the back pocket), A6 screen pop-out (the picture pops out of Cheeko's screen in Part 2), A4 card wheel (end), T1/T5/T6 between scenes.

## What we need

- App screens rendered from the real widgets (the appshots harness): the rights check, the file landing in the list, Uploading and the Saved toast. The Profile, card list, recorder and image editor screens already exist in `app-shots-ios/`.
- Cheeko screens: `content_play_2b_downloading`, then our three pictures on the play screen (296 x 240).
- Photos: a grandparent with a child, a parent recording on a phone, a child in bed with Cheeko. Never the same child twice.
- Voices: narrator, Mom, Grandma, kid (MiniMax, checked with speech-to-text).

## Not said

Deleting or reordering recordings, WhatsApp voice notes or iPhone voice memos (the app takes MP3 and WAV only), anything from YouTube (the rights check says it needs permission).
