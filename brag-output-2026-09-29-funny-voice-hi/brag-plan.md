# V13-HI Funny Voice (Hindi): script and shot list

One feature per video, 2026-09-29. Vertical 1080x1920, 37.99s. Voices: narrator = hindi_male_1_v2, Cheeko = English_PlayfulGirl, Nani = English_Graceful_Lady, Mitthu = English_Upbeat_Woman, Quizzy = hindi_female_1_v2, kid = English_LovelyGirl, Grandma = hindi_female_2_v1.

| Time | Speaker | Line |
|---|---|---|
| 0.1s | narrator | चेतावनी। इस खिलौने से हँसी रुकती नहीं। |
| 3.4s | narrator | बटन दबाओ और कुछ मज़ेदार बोलो। |
| 6.0s | kid | हैलो! मैं एक डायनासोर हूँ! |
| 9.8s | Funny Voice | (the kid's line played back as chipmunk) |
| 12.2s | Funny Voice | (the kid's line played back as monster) |
| 17.3s | Funny Voice | (the kid's line played back as robot) |
| 20.9s | Funny Voice | (the kid's line played back as echo) |
| 25.8s | Funny Voice | (the kid's line played back as speedy) |
| 27.9s | narrator | पाँच मज़ेदार आवाज़ें। वाई फ़ाई की ज़रूरत नहीं। |
| 31.7s | narrator | Cheeko. कम स्क्रीन, ज़्यादा बचपन! |

Shots: see `work/spec.js` (each shot is tied to a voice line). Device screens are real firmware renders (fw-screens, commit b05c95d). Narrator lines become word captions, character and kid lines become speech bubbles.

Hindi notes: the device cannot show Devanagari, so Imagine screens use the *_hi_* renders (blank transcript and caption).

The five playback voices are our approximations of the device effects (made with ffmpeg in build_feature.py).
