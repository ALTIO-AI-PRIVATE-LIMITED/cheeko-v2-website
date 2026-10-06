# /brag plan: Cheeko Reel #3 "Built to END" (marketing/cheeko-video-ideas.md #3)

**Format:** vertical 1080×1920, 30fps, 29.8s · **Tone:** fast, funny, Reels-native · **VO:** MiniMax speech-2.8-hd, English_radiant_girl, emotion happy (same voice as the "NO tantrum" Reel). Take 1 of 2, long pauses tightened 32.5s → 27.4s; checked word-complete with Sarvam speech-to-text.

## Script and shots
| Time | VO | On screen |
|---|---|---|
| 0.0-4.85 | "Your phone is built to never end. Scroll... scroll... scroll..." | A phone with an endless feed of video tiles over a blurred kid-on-phone photo; each "scroll" flicks it, then it spins out and gets yanked away |
| 4.85-7.3 | "Cheeko? Built to END! (laughs)" | Sun rays, Cheeko pops in with a "?", "Built to END!" with END in red, the device giggles on the laugh |
| 7.3-10.65 | "No feed. No videos. Nothing to scroll." | Feed, video and scroll icons pop in and get struck out |
| 10.65-17.6 | "Here's everything it ever shows: Talk! Games! Imagine! Radio! Funny Voice! ...That's it!" | The device screen flips through the five real menu screens with a 1/5 ... 5/5 counter; "That's it!" + confetti |
| 17.6-21.45 | "And when nobody's playing? It goes to sleep. By itself." | Night sky; the screen dims to dark, z z z float up |
| 21.45-24.4 | "Screens that end... raise kids who know how to stop." | Girl dancing with Cheeko, then a family laughing, zoom punch on "STOP" |
| 24.4-29.8 | "Cheeko. Less screen, more childhood!" | Outro: logo bounce on "Cheeko", device + three new cards, highlight on "childhood.", ₹5,999 · Device + 10 cards, "Link in bio 👆", "Send this to a parent who needs it 👀" |

## Sound
Original: a ticking loop that speeds up under the feed with a whoosh per "scroll", a record-stop as the phone is yanked, near-silence on "Cheeko?", the D-major 120 BPM groove drops on "END!", a drum-less lullaby while it falls asleep, back in for the kids, resolves on D. VO ~7-10 dB over the music.

## Honesty check
- "Everything it ever shows" = the firmware's main menu: Talk, Imagine, Games, Funny Voice, Radio (+ Settings, not a content screen). The five menu images are the site's own device art.
- "It goes to sleep by itself": firmware dims the screen when idle and deep-sleeps after 30 minutes (cheeko_v2_board.cc). The video shows the dimming, not a time.
- "No feed. No videos. Nothing to scroll." is site copy; "Screens that end raise kids who know how to stop." is site copy.
- Feed tiles are abstract gradients, and the video icon is a generic purple play button: no real app, platform or logo is shown.
- No child repeats within the video; none of the kids from the "NO tantrum" Reel appear except the device itself.

**Updated 2026-09-28 (current firmware UI):** the device now shows the real current screens rendered from firmware b05c95d (FW 2.4.311, `assets/img/device_current.png` and `assets/img/fw-screens/`) instead of the old dark Talk screen.

## Hindi version (2026-09-28)
Same shots and timing as the English Reel, re-voiced in Hindi with MiniMax `hindi_male_1_v2` (Trustworthy Advisor, chosen by Ravi), one clip per line with its own emotion (lines in `marketing/tools/vo_lines_hi.json`). Captions and fixed on-screen text are in Hindi (`marketing/tools/make_hindi.py`); the device screens and the child's Imagine wish stay in English because that is what the device shows. Qwen multilingual was tried first and rejected: it garbled the Hindi (checked with Sarvam hi-IN speech-to-text).
