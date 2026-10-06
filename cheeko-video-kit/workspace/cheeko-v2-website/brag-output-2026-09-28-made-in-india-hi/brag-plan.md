# /brag plan: Cheeko Reel #4 "Made in India" (marketing/cheeko-video-ideas.md #4)

**Format:** vertical 1080×1920, 30fps, 32.6s · **VO:** MiniMax speech-2.8-hd, English_radiant_girl, happy (same voice as Reels 1b and 3). Take 1 of 2 (take 2 dropped an "and"); checked with Sarvam speech-to-text; pauses tightened 38.2s → 30.1s; "Real humans on WhatsApp." cut for length.

## Script and shots
| Time | VO | On screen |
|---|---|---|
| 0-2.1 | "Guess this sound!" *[synthesised cooker whistle]* | Orange rays, a "?", a cartoon pressure cooker that shakes and steams |
| 2.1-3.5 | "Pressure cooker! (laughs)" | "PRESSURE COOKER!" stamp + confetti as the beat drops |
| 3.5-9.1 | "That's Cheeko's Sounds Around Me card. Cooker whistle... doorbell... *[ding-dong]* name that sound!" | The real shipping Sounds Around Me card drops into Cheeko, cooker and doorbell bubbles; the bell rings on the ding-dong |
| 9.1-12.5 | "Because Cheeko is made in India, for Indian kids." | "MADE IN INDIA · FOR INDIAN KIDS" stamp over the device, then "Backed by Anvesana · Swissnex · Sarvam" (the site's own row) |
| 12.5-17.5 | "Nani tells the stories every family knows... and when you interrupt? She listens!" | Nani and her card, a "• • •" story bubble, a "✋ Wait, why?" interruption, Nani tilts to listen, a heart |
| 17.5-21.45 | "Say, an auto rickshaw flying to the moon... and it's drawn!" | Green; the wish types out, flash, the site's real Imagine drawing (im-07) paints onto the screen |
| 21.45-25.75 | "Hindi, Tamil, Kannada, Bengali... and English too!" | A giant letter for each language |
| 25.75-27.7 | "Built by Indian parents." | Real family photo from the Bengaluru shoot |
| 27.7-32.6 | "Cheeko. Less screen, more childhood!" | Outro with the Clever Little Tales, Mitthu and Nani cards |

## Honesty check
- "Made in India": site footer and tender spec. "Built by Indian parents": site's "We're parents too" + Made in India. Backers: the site's own "Backed by" row, same logo files.
- Sounds Around Me: the shipping sound-game card. Ravi confirmed on 2026-09-28 that it includes the pressure cooker and doorbell sounds (the site still calls it "Around the House"). The card line was re-recorded (same voice, take matched to 1.84s) and spliced in.
- Nani: site copy "Interrupt her mid-story. She listens."; "the tales every family knows" is the Clever Little Tales card copy. The "Wait, why?" bubble is illustrative.
- Imagine drawing is the site's own "an auto rickshaw flying to the moon" (im-07).
- The Indian flag is deliberately not used (Flag Code restricts commercial use).
- Device screen overlays use the measured screen mask; the screen is never blank.

**Updated 2026-09-28 (current firmware UI):** the device now shows the real current screens rendered from firmware b05c95d (FW 2.4.311, `assets/img/device_current.png` and `assets/img/fw-screens/`) instead of the old dark Talk screen.

## Hindi version (2026-09-28)
Same shots and timing as the English Reel, re-voiced in Hindi with MiniMax `hindi_male_1_v2` (Trustworthy Advisor, chosen by Ravi), one clip per line with its own emotion (lines in `marketing/tools/vo_lines_hi.json`). Captions and fixed on-screen text are in Hindi (`marketing/tools/make_hindi.py`); the device screens and the child's Imagine wish stay in English because that is what the device shows. Qwen multilingual was tried first and rejected: it garbled the Hindi (checked with Sarvam hi-IN speech-to-text).

## Imagine wish in Hindi (2026-09-28)
Ravi: the device takes any language, so the child now says the wish in Hindi ("साइकिल चलाता टाइगर" / "चाँद पर उड़ता ऑटो रिक्शा"). The device screens are rendered from firmware b05c95d with that Hindi prompt: the firmware has no Devanagari glyphs in any built-in font, so the transcript shows only quote marks, the prompt line under "Painting our idea." is blank and the picture has no caption. The video shows exactly that (listening, painting, picture) and skips the transcript screen.
