# V19 Parent App: "You hold the keys" (plan and script, draft for Ravi, 2026-09-29)

**Goal:** trust. Parents see that they control the toy from their phone and can see how their child is doing, and that Cheeko is safe by design.
**Format:** Reel, vertical, about 32 s, English + Hindi, thumbnail. Hindi narrator `hindi_male_1_v2` (Trustworthy Advisor) fits this one especially well.
**Style (from Ravi's references: motionin.design, landdding, savee):** more premium than the playful Reels. Dark warm background, one saturated accent (Cheeko orange), big clean type, the real app screens on a phone that moves in 3D (cover-flow of screens, like Motion's "Frieze"), an iris wipe between scenes, and short sticker labels ("VOLUME", "SLEEP", "EVERY WORD") dropped onto the screens like Motion's "Cutout". Calm music with a steady pulse, not the bouncy groove.

Every claim below was checked end to end in the code (app -> server -> device or AI) on 2026-09-29.

## Script (core version, everything here works today)

| # | Voice (emotion) | Line | On screen |
|---|---|---|---|
| 1 | N (calm) | Your kid talks to Cheeko every day. | Dark screen, a kid holding Cheeko, soft light |
| 2 | N (surprised) | So you get to see every word. | Phone flies in: Today's chats, the child's question and Cheeko's answer. Sticker: EVERY WORD 👀 |
| 3 | N (calm) | It only listens while the button is pressed. | Close-up of the knob, press ripple 🔘 |
| 4 | N (calm) | No camera. No wake word. | Two stamps: NO CAMERA 🚫📷, NO "HEY CHEEKO" |
| 5 | N (happy) | Too loud? Turn it down from your phone. | Device controls screen, volume slider moves, stickers VOLUME 🔉 |
| 6 | N (happy) | Dim the screen. Or put it to sleep. | Brightness and sleep switches flip; the real device screen dims to dark 🌙 |
| 7 | N (happy) | See what they played today. | Today with Cheeko: talks, cards, games |
| 8 | N (happy) | How the quiz went. The moment they got curious. | Daily quiz progress, Moment of the day ✨ |
| 9 | N (happy) | Every picture they imagined, saved for you. | Imagine gallery wall flows past (cover-flow) 🎨 |
| 10 | N (happy) | And a little recap every night. | Phone notification: "Today's Cheeko recap 📊 Cheeko played for 45 minutes across 3 sessions today." |
| 11 | N (happy) | You can even record your voice on their cards. | Custom card screen, record button 🎙️ |
| 12 | N (happy) | Their playtime. You hold the keys. | Phone + device side by side, keys icon 🔑 |
| 13 | N (happy) | Cheeko. Less screen, more childhood! | Outro, "Parent app for iPhone and Android" |

About 32 s. The "45 minutes, 3 sessions" in line 10 is sample data shown in the real notification format.

## Optional scenes (only if these are live when the video is posted)

These work in code but are not on the live app or server yet (app branch `feat/daily-streak` is local and unpushed; backend `deploy/persona-simplification`; voice agent `deploy/persona-on-jev`):

| Voice | Line | On screen |
|---|---|---|
| N (happy) | Set house rules. No scary stories. Bedtime at 8. | House rules screen, topics to avoid |
| N (surprised) | Add their exam, and Cheeko wishes them luck the day before. | Upcoming events, then Cheeko talking screen "All the best for your exam tomorrow!" |
| N (happy) | Keep their daily streak going. | Streak calendar 🔥 |
| N (calm) | Every answer passes child-safety filters. | Shield icon |

If they ship, lines 11 and 12 become: "Set house rules. Add their big days." / "Their playtime. Your rules."

## Not claimed (checked, not true today)

Screen-time limits, quiet hours, bedtime lock (bedtime is only a hint to the AI), battery alerts on the phone, updating the toy from the phone, reading chats from earlier days, deleting data from the app, controlling auto-listen or autoplay, data stored in India, content-filter settings.

## Visuals I need or will make

- App screens: I'll use the real app screens cut out of the Play Store images (home, today's chats, device settings, analytics, gallery, custom card). Sharper option: Ravi records the real app on a phone (Today's chats, Device controls, Home, Gallery) for 10 seconds each.
- Device: real firmware screens (fw-screens), including the brightness setting and the screen dimming.
