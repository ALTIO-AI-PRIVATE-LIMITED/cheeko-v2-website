# Cheeko video production rules

## How a video is made (one folder per video in this Drive)
1. **Script**, the script and shot list (every voiceover line with its shot), plus the Instagram caption.
2. **Voice**, the raw voice takes, the final tightened voiceover, and a music-only track (for posting with trending audio).
3. **Test**, a contact sheet of frames every 1.5s. Every scene and transition is checked here before the final render.
4. **Final**, the video, poster and caption with the standard name `Cheeko_<ID>_<Name>_<Reel|Film>_9x16_<seconds>s.mp4`.
5. **Source**, the composition (`compose.html`) and the music script (`synth.py`), enough to re-render.

IDs run V01, V02... in the order videos are made. Rejected videos move to `X Archive`.

## Style (from Ravi's feedback, 2026-09-28)
- Written for Instagram Reels: hook in the first second, a new shot every 1-2 seconds, word-synced captions, a fun and energetic voice, ~20-30s.
- End on "Link in bio 👆" and "Send this to a parent who needs it 👀".
- Voice: MiniMax speech-2.8-hd, voice **English_Upbeat_Woman**, recorded one line at a time with its own emotion (surprised, happy, calm, fluent...), Ravi picked it 2026-09-28 because a single-emotion take sounded flat. Lines live in `marketing/tools/vo_lines.json`; `build_vo.py` assembles them and re-times the video.
- Never the same child twice in one video. Never a blank or black device screen. Screen content is clipped to the real screen shape (device screen mask).

- **Writing (Ravi, 2026-09-28):** never use em dashes, the ellipsis character or curly quotes in anything people read or hear (voice text, captions, on-screen text, Instagram captions, docs). They read as AI-written. Use commas and full stops, and write like a person texting a friend.
- **Emojis:** use them in on-screen captions, Instagram captions and thumbnails to make them fun (e.g. 😳 🦊 💥 🐯🚲 😴 🔔 👵). Never put emojis in the voice text.

## Facts to use
- ₹5,999 for the device + 10 cards. Free delivery across India. **12-month warranty** and **6-hour battery** (confirmed by Ravi; the website is out of date).
- English + 10 Indian languages. 8 built-in offline games. Talk and Imagine free for 3 months, then an optional plan.
- The 10 shipping cards: Tales of Kindness, Floor is Lava!, Play & Sing Along, Dreamy Melodies, Mitthu the Parrot, Make Your Own, Clever Little Tales, The Adventures of Ravi & Nila, Sounds Around Me (includes pressure cooker and doorbell), Nani.
- New cards: **5 cards for ₹499** (Ravi, 2026-09-29; the website still says 15 cards at ₹199 to ₹299, stale).
- Mitthu the Parrot is an **English learning teacher** (words, meanings, spelling, speaking), not only spelling. Nani is the storyteller, including bedtime stories.
- Made in India by Altio AI. Backed by Anvesana, Swissnex India, Sarvam AI.

## Never
- Say "once" or "one-time" about the price, or give a ship date that has passed.
- Show "Hey Cheeko" voice wake-up, LEDs, Talk/Imagine/Radio working offline, or games that are switched off (Shapes, Math, Race, Tetris...).
- Show old website cards (Storytime Adventures, Ravi's Wild Journey, Around the House).
- Claim certifications (BIS, WPC, EMC are in progress).
- Use the Indian flag, other brands' logos or characters (e.g. the Spider-Man Imagine demo), or invented testimonials and numbers.
