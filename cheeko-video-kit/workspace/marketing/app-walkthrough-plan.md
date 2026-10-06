# V25 Cheeko App Walkthrough: plan and script (draft for Ravi, 2026-09-29)

## The idea

A detailed tour of the parent app, tab by tab, for new parents. Five short parts (about 35 to 45 s each) that each work alone as a Reel, stitched into one film of about 3.5 minutes for YouTube, the website and WhatsApp. Same method as the onboarding series: build the parts one by one, then re-render them together with one music theme.

| Part | Title | What it covers | Length |
|---|---|---|---|
| 1 | Home: their day at a glance | Tabs, Today with Aarav, today's chats, quiz, streak, moments, gallery, recent cards | ~45 s |
| 2 | Device: Cheeko's remote control | Battery and status, volume, brightness, theme, sounds, vibration, sleep, Save, two Cheekos, remove | ~45 s |
| 3 | Analytics: how they're growing | Day and Week, the four stats, details, quiz answers, weekly chart and breakdown, past weeks | ~35 s |
| 4 | Gallery and custom cards | Save and share drawings, record your own voice on a card with a picture | ~40 s |
| 5 | Profile: your child, your rules | Child details, house rules, big days, notifications and recaps, Wi-Fi, another Cheeko, help | ~45 s |
| All | Cheeko App Walkthrough (full film) | All five with chapter cards | ~3.5 min, vertical and 16:9 |

## Look

- Every phone is an iPhone (titanium body, Dynamic Island, iOS status bar and home bar) with the app rendered as iOS, per Ravi.
- Calm and clear: a big iPhone in the centre, warm cream background, one thing at a time. Taps show as ripples; each setting gets the new curved arrow with a label. Chapter cards in Cheeko orange ("App guide · Part 2 of 5").
- Every screen is the real app (branch feat/daily-streak, commit d49af42) rendered from its widgets with sample data: parent Priya, child Aarav (6), 48 min today, 5 talks, 4 cards, 3 games, quiz 7/10, 5-day streak.
- Where the setting reaches the toy, a small Cheeko sits beside the phone and its real firmware screen changes (volume, brightness, theme, sleep).
- Narrator English_Upbeat_Woman, calm, 1.05x. Hindi version after the English one is approved.

## Script

### Part 1: Home, their day at a glance

| # | Voice | Line | On screen |
|---|---|---|---|
| 1 | N (happy) | Here's everything the Cheeko app can do! | iPhone flies in on Home |
| 2 | N (calm) | Four tabs. Home, Device, Analytics and Profile. | Arrows on the four tabs, one by one |
| 3 | N (happy) | Home shows your child's day. How long they played, and how many talks, cards and games. | Today with Aarav: arrows on 48m, Talks, Cards, Games |
| 4 | N (surprised) | Tap Review to read today's chats. Their questions, and Cheeko's answers, word for word. | Tap Review, Today's chats, slow scroll |
| 5 | N (calm) | Tap a character to see just their chats. | Tap Nani in the character strip |
| 6 | N (happy) | Daily Quiz shows how Quizzy's questions went. | Quiz card, arrow on 7/10 |
| 7 | N (happy) | And the streak counts the days in a row they've kept it up. | Streak card, then the Streak screen |
| 8 | N (happy) | Scroll down for the moment of the day, everything they imagined, and the cards they played. | Home scrolls: Explored today, Gallery, Recent activity |

### Part 2: Device, Cheeko's remote control

| # | Voice | Line | On screen |
|---|---|---|---|
| 1 | N (happy) | The Device tab is Cheeko's remote control. | Tap Device |
| 2 | N (calm) | See the battery, the Wi-Fi network, and when Cheeko was last online. | Arrows: battery, Network, Last seen |
| 3 | N (happy) | Too loud? Slide the volume down. | Volume slider moves; Cheeko beside the phone |
| 4 | N (happy) | Set the brightness, and pick a colour theme for Cheeko's screen. | Brightness slider, theme picker (Sunny, Night, Ocean, Candy...); Cheeko's screen changes theme |
| 5 | N (calm) | Turn system sounds and vibration on or off. | Two switches flip |
| 6 | N (calm) | Sleep mode lets Cheeko nap by itself when nobody's playing. | Sleep switch on; Cheeko's screen dims, then naps (firmware: the app's sleep_enabled switches the idle timer that dims at 2 min, screen off at 5, naps at 30) |
| 7 | N (happy) | Then tap Save, and the changes go to Cheeko. | Tap Save |
| 8 | N (calm) | Got two Cheekos? Switch between them at the top. | Device name dropdown |
| 9 | N (calm) | Remove Device unlinks a Cheeko. Your child's progress stays with them. | Scroll to Device actions, arrow on Remove Device |

### Part 3: Analytics, how they're growing

| # | Voice | Line | On screen |
|---|---|---|---|
| 1 | N (happy) | Analytics shows how your child is growing. | Tap Analytics |
| 2 | N (calm) | The Day view shows play time, success rate, their streak, and questions asked. | Arrows on the four stat cards |
| 3 | N (calm) | Tap any section for the details. | Today's activity: Games, Cards, Interactions, Audio |
| 4 | N (surprised) | In the quiz, see every answer. Right, wrong, or revealed. | Quiz answers list |
| 5 | N (happy) | The Week view shows each day's activity, and where their time went. | Week: bar chart, then the breakdown pie |
| 6 | N (calm) | Look back up to twelve weeks. | Week picker, Previous |

### Part 4: Gallery and custom cards

| # | Voice | Line | On screen |
|---|---|---|---|
| 1 | N (happy) | Everything your child imagines is saved in the Gallery. | Home, Gallery, See all, grid |
| 2 | N (happy) | Open a picture to save it or share it with family. | Full screen: Save, Share |
| 3 | N (calm) | Hold to pick a few, and share them together. | Multi-select, Select all |
| 4 | N (surprised) | Custom cards put your own voice on a card. | Profile, Add Custom Cards |
| 5 | N (happy) | Record a story, a song or a message. Or upload an audio file. | Record Voice sheet recording, then Upload Audio |
| 6 | N (happy) | Add a picture, crop it, pick a filter. | Image editor: crop, filters, Use This Picture |
| 7 | N (happy) | Up to ten recordings, and Cheeko plays them when your child taps their custom card. | Card list with items; Cheeko beside it playing the recording with its picture |

### Part 5: Profile, your child, your rules

| # | Voice | Line | On screen |
|---|---|---|---|
| 1 | N (happy) | In Profile, keep your child's details up to date. | Tap Profile, Kid Profile |
| 2 | N (happy) | A photo, their birthday, and what they love. Cheeko uses it in every chat. | Photo, birthday, interests chips |
| 3 | N (calm) | Set house rules. No scary stories, bedtime at eight, which languages, and topics to skip. | House rules screen (see note A) |
| 4 | N (surprised) | Add their big days, like a birthday or an exam, and Cheeko brings them up. | Upcoming: "Science exam, Oct 14" added |
| 5 | N (happy) | Turn on notifications for a recap of their day every night, and their week every Sunday. | Notifications screen, then the recap notification drops in |
| 6 | N (calm) | Add another Cheeko, or change its Wi-Fi, right here. | Device section: Add Device, Wi-Fi Setup |
| 7 | N (calm) | And if you need us, tap Help and Support. | Help & Support row |
| 8 | N (happy) | That's the Cheeko app. Their playtime, your rules! | Outro: Cheeko app for iPhone and Android |

About 420 words, 3.3 to 3.6 minutes with the chapter cards.

## What we will NOT show or say (checked in the code, 2026-09-29)

- Earlier days' chats (the app shows today only), character settings, the music library, chit chat: these screens exist in code but no button opens them.
- Auto listen, System prompt and Autoplay: the switches are on the Device screen, so they are visible, but the narrator does not mention them (note B).
- Time limits, screen-time limits, quiet hours, a bedtime lock, firmware updates from the phone, per-type notification settings, battery alerts, deleting the account or pictures: none of these exist.
- Bedtime and house rules are said as "Cheeko keeps them in mind", never as a lock.
- Developer options (7 taps on the version number).

## Questions for Ravi

- **A. Answered 2026-09-29:** one child per Cheeko for now, so "who's using it now" is out. House rules, big days and the streak ship before we post.
- **B. Auto listen, Autoplay, System prompt.** Ravi (2026-09-29): the app team will fix the Device settings screen. Once the fixed build is in, tell me what each switch does on the toy and I add one line for them in Part 2; until then the narrator skips them.
- **C. Answered 2026-09-29:** its own Drive folder "Cheeko App Guide", same layout as Onboarding Cheeko.

Each part also ends with a short "Next up" line (Parts 1 to 4). Recorded 2026-09-29: parts run 26 to 37 s (about 2.7 min of voice).

## For the app team (seen while mapping the app; fix before we film if possible, since some show on screen)

Ravi, 2026-09-29: the app team will fix the Device settings screen switches (note B) and the streak card's em dash. We render the app screens from the fixed commit once it lands; until then the streak card's last line stays out of frame.

On screen in the video:
- Em dashes in app text: the streak card "One rest day a week is free — the run keeps going." (being fixed) and the Switch Cheeko sheet "Everything — progress, chats and profile — follows...".
- Typos: "Terms of Services" (sign-in), "todays' journey" (Home), "Wifi Setup" / "Wifi updated" next to "Wi-Fi", the Device section in Profile repeats the subtitle "Manage your account and settings".
- The Device card says Live/Idle while the tile below says Online/Offline.

Bugs:
- Choosing Malayalam as Cheeko's language in onboarding saves English (interactive_kids_onboarding_screen.dart:252-265).
- Editing a child's Notes is not saved (child_profile_screen.dart:916-925, kids_service updateKid has no notes).
- Phone numbers must be exactly 10 digits for every country code.
- "Explored today → See all" does nothing; "Moment of the day" summaries come from keyword matching and can be wrong (any question with "star", including "start", says "explored how distance changes what we see").
- The custom card child picker shows the toy's raw MAC address.
- Device Save never tells the parent whether the toy applied the change (the sync status widget exists but is unused).
- Two different "streak" numbers: Analytics "Active streak" and the daily streak card.

Promises the app does not keep:
- Terms of Service say parents can delete their account in the app, customise personas, and monitor all conversations; the app has no delete, no persona screen, and today's chats only.
- The Notifications subtitle promises battery alerts; they only fire while the app is open.
- "Preferred language" in the parent profile is saved but changes nothing.

Security: Developer Options open to anyone with 7 taps on the version number and the PIN 8090 (in the code), and let the app switch to the development server.

### Found while rendering the walkthrough screens (2026-09-29)

- More em dashes in app text: House rules "Birthdays, trips, exams — Cheeko brings them up" (shows in Part 5), the streak screen legend "Rest day — free, the run carries on", "Quiet day — nothing recorded", "Today — still open" (Part 1), and "Using "Cheeko" — would be moved" on Who is this Cheeko for?
- Kid Profile: the "House rules & upcoming" row is 130 px wider than an iPhone screen, so its value is cut ("Bedtime, languag…") and the arrow is hidden. Also the page is titled "Edit Profile", the same as the parent's page.
- The Kid Profile shows any gender other than exactly "Male" as "Female" (the server value "male" in lowercase would show as Female).
- Gallery viewer: the "1 / 8" title and the back arrow are dark on the black viewer, nearly invisible.
- Notifications screen: default styling with a purple button, unlike the rest of the app, and it says "CheekoAI".
- Wi-Fi is spelled three ways: "Wifi Setup", "Wi-Fi network", "WiFi".
- In the "everyone" chat thread every character's reply is labelled "Cheeko", so Nani's lines read as Cheeko there.
- Device Save gives no confirmation: after the spinner the Save pill just fades back.
- The device-name menu (two Cheekos) lists names in small, light text and covers the button.
