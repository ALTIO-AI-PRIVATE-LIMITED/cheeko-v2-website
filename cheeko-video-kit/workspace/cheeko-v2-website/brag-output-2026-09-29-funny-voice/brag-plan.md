# V13 Funny Voice: script and shot list

One feature per video, 2026-09-29. Vertical 1080x1920, 32.38s. Voices: narrator = English_Upbeat_Woman, Cheeko = English_PlayfulGirl, Nani = English_Graceful_Lady, Mitthu = loongnorahu, Quizzy = loongivyhu, kid = English_LovelyGirl, Grandma = English_Wiselady.

| Time | Speaker | Line |
|---|---|---|
| 0.1s | narrator | Warning. This toy causes giggles. |
| 2.8s | narrator | Hold the button and say something silly. |
| 5.2s | kid | Hello! I am a dinosaur! |
| 8.2s | Funny Voice | (the kid's line played back as chipmunk) |
| 10.2s | Funny Voice | (the kid's line played back as monster) |
| 14.3s | Funny Voice | (the kid's line played back as robot) |
| 17.3s | Funny Voice | (the kid's line played back as echo) |
| 21.5s | Funny Voice | (the kid's line played back as speedy) |
| 23.2s | narrator | Five silly voices. No Wi-Fi needed. |
| 26.3s | narrator | Cheeko. Less screen, more childhood! |

Shots: see `work/spec.js` (each shot is tied to a voice line). Device screens are real firmware renders (fw-screens, commit b05c95d). Narrator lines become word captions, character and kid lines become speech bubbles.

The five playback voices are our approximations of the device effects (made with ffmpeg in build_feature.py).
