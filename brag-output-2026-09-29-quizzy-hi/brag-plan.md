# V17-HI Quizzy (Hindi): script and shot list

One feature per video, 2026-09-29. Vertical 1080x1920, 26.44s. Voices: narrator = hindi_male_1_v2, Cheeko = English_PlayfulGirl, Nani = English_Graceful_Lady, Mitthu = English_Upbeat_Woman, Quizzy = hindi_female_1_v2, kid = English_LovelyGirl, Grandma = hindi_female_2_v1.

| Time | Speaker | Line |
|---|---|---|
| 0.1s | narrator | रोज़ दस छोटे सवाल। |
| 1.9s | Quizzy | कौन सा जानवर छिपने के लिए अपना रंग बदलता है? |
| 5.0s | kid | वो गिरगिट है! |
| 7.1s | Quizzy | हाँ! गिरगिट! बिल्कुल सही! |
| 9.9s | narrator | अपने शब्दों में जवाब दो। हिंदी या इंग्लिश, कोई भी। |
| 14.1s | narrator | ना स्कोर। ना प्रेशर। |
| 16.2s | narrator | और पेरेंट ऐप में देखो, क्विज़ कैसा रहा। |
| 19.5s | narrator | Cheeko. कम स्क्रीन, ज़्यादा बचपन! |

Shots: see `work/spec.js` (each shot is tied to a voice line). Device screens are real firmware renders (fw-screens, commit b05c95d). Narrator lines become word captions, character and kid lines become speech bubbles.

Hindi notes: the device cannot show Devanagari, so Imagine screens use the *_hi_* renders (blank transcript and caption).

Quiz question is real: quiz_question id 1292 (dev DB), accepted answers include girgit.
