# Cheeko parent app: real-widget screenshots (iPhone)

## iOS (2026-09-29)
Every screen is now rendered as iPhone: `debugDefaultTargetPlatformOverride = TargetPlatform.iOS` in `preparePhone` (reset in `finish`), so switches, `SwitchListTile.adaptive`, back chevrons and page transitions are the iOS ones, and the Mac's SF font (`SFNS.ttf`) stands in as the system fallback. The whole set, old and new, is in **`cheeko-v2-website/assets/img/app-shots-ios/`** (onboarding in its `setup/` subfolder). `assets/img/app-shots/` still holds the older Android-look set that earlier videos use; it is not touched. `zsh tests/run.sh` now writes to `app-shots-ios` by default (set `OUT=` to change it). Same method as before: real widgets from commit d49af42, fake services and an in-process fake network, 1179 x 2556 per phone screen (393 x 852 pt at 3x), status-bar area left blank (59 pt) for the video's own iOS status bar. Files ending in `_full` are tall captures of the whole scroll.

Sample data changes in this round: Aarav's gender is stored as `Male` (the app's own spelling; the profile screen reads anything else as Female), his interests are the onboarding picks (Animals, Dinosaurs, Science), and he has a photo (`media/kid-aarav.jpg`, from the website's `live/kid-beanbag.jpg`). Two em dashes in our own sample text were replaced ("very, very big, like an elephant", "Jump, freeze and giggle: a movement game"). All numbers are unchanged.

### Walkthrough additions

New tests are in `tests/profile_shots_test.dart` (10–13) and at the end of `tabs_shots_test.dart` (03, 04, 06), `flows_shots_test.dart` (02, 07) and `setup_shots_test.dart` (08). The existing shots are re-rendered with the same content, apart from the iOS look and the sample-data notes above.

| File | How it was reached | Notes |
|---|---|---|
| 02_today_chats_nani | Home → Review → the Nani tile in the character strip | Two exchanges at 3:30 PM (clever crow story), served by the per-character endpoint. They are not in the "everyone" thread, so the 5-talks count stays. Opens scrolled to the newest, as the app does; the "Today · 3:30 PM" marker is just above the top. |
| 03_device_theme_picker | Device tab → Theme row | The app's "Select theme" dialog, Sunny ticked. |
| 03_device_two_toys (+ `_closed`) | Device tab with a second toy ("Cheeko 2", Anaya, 4) → the name button at top right | Only this test turns on the second toy (`sampleTwoToys`). With two children the app also shows its "Who's using it now?" row (Aarav / Anaya). The menu lists toy names only. |
| 03_device_two_toys_1kid (+ `_closed`) | Same, but the account has one child (Aarav) and the second toy has no child yet (`sampleSecondKid = false`) | Use these: the "Who's using it now?" quick switch is not shipping (one child per Cheeko), and with one child the app does not render it. The menu lists Cheeko and Cheeko 2. |
| 03_device_full, 03_device_actions | Device tab, tall capture; then scrolled to the bottom | "Device actions / Remove Device" above the nav capsule. |
| 03_device_controls_changed (+ `_switches`, `_full`) | Device tab: volume 35, brightness 50 through the sliders' handlers, Sleep mode switch tapped | The header's Save only lights up with unsaved changes, and it scrolls with the page, so no one phone screen shows Save and Sleep mode together: `03_device_controls_changed` is the top (Save lit, 35% / 50%), `_switches` is the Controls card (Sleep mode on), `_full` is both. The older `03_device_controls_adjusted` (volume 30, sleep on) has no Save in view. |
| 03_ctl_1_vol35 … 03_ctl_7_saved | Device tab, scrolled exactly as 03_device_controls (offset 446 pt, identical in ctl_1–ctl_5); then, cumulatively: volume 35, brightness 50, Theme row → "Select theme" (ctl_3), Night tapped (ctl_4), Sleep mode switch (ctl_5); top of the tab with Save lit (ctl_6); Save tapped (ctl_7_saving, ctl_7_saved) | The fake settings endpoint accepts the PATCH as the server does (merged settings, next version, `synced`). The app shows no snackbar on a successful save: the pill spins (`_saving`, controls greyed while in flight), then Save goes back to its faded idle look with the new values kept (`_saved`). |
| 06_analytics_activity_detail (+ `_interactions`) | Analytics, Day → "Games" tile under Today's activity (then "Interactions") | The app's bottom sheet: Floor is Lava!, Sounds Around Me, Word Ladder with score and level. |
| 06_analytics_week_picker | Analytics → Week → back two weeks → the week title | "Choose a week" sheet, "2 weeks ago" ticked. |
| 07_gallery_viewer | Home → Gallery "See all" → first picture | Save / Share / Details at the bottom. |
| 07_gallery_select | Gallery: long-press one picture, tap two more | "3 selected", Select all / Save / Share. |
| 08_image_editor (+ `_top`, `_full`) | `showToyImageEditor` on `media/im-10.jpg` (what the Gallery tile calls once the photo picker returns), then the Sepia tile tapped | The photo picker itself can't run in a test. At 393 x 852 the crop frame and the filter strip don't fit on one screen: `08_image_editor` is scrolled so the strip is fully visible (top of the frame cut), `_top` shows the whole frame in sepia, `_full` has everything including the Sepia amount slider. |
| 08_custom_card_list | `CreateCustomCardView` (as 08_custom_card) with three recordings, each with a picture | Grandma’s lullaby, Good morning song, Story: the thirsty crow. The crow picture is a crop of the Clever Little Tales card art (`media/cc-crow.jpg`). |
| 10_profile, 10_profile_full | App opens on Home, then the Profile tab | Version reads 3.8.36 (140), the pubspec at d49af42 (package info is mocked). |
| 11_kid_profile, 11_kid_profile_full | Profile → Kid Profile | Photo, name, birthday Apr 2, 2020, Male, Animals / Dinosaurs / Science. **`_full` stops partway down the Rules card**: the "House rules & upcoming" row below it is 130 px wider than the phone (app bug, see below), and in a test Flutter paints a striped marker and a tall red label over it. Notes, its suggestion chips and Save Changes could not be captured clean. |
| 12_notifications | Profile → Notifications | iOS switch on. Firebase Messaging can't run in a test, so the controller's public `permissionGranted` / `registered` fields are set, which gives the "ready on this phone" line. |
| 13_add_device_who | Profile → Add Device | "Who is this Cheeko for?" |
| 13_wifi_setup | Profile → Wifi Setup, with Bluetooth reported on | The app skips its checklist and opens the Bluetooth scan ("Select Cheeko", scanning). The Bluetooth plugin is stubbed to stay silent. |
| 04_house_rules_bedtime8 | House rules with 8:00 PM, No scary stories on, English + Hindi, topics "ghosts, horror" | Topics are passed in as the saved rules (typed lower-case). The older 04_house_rules keeps "Ghosts, Monsters". |
| 04_house_rules_upcoming | Same screen, scrolled to the bottom | Science exam, 14 Oct (Parent) and Birthday party at Riya’s, 24 Oct (Told to Cheeko). Fixed dates: after 24 Oct 2026 the app will dim them as past. |

### App issues seen in these screens (for the app team)
- Kid Profile: "House rules & upcoming" row overflows by 130 px at 393 pt (no `Expanded` around the label/value), so on a phone the value is clipped to "Bedtime, languag…" and the chevron is cut off.
- Gallery viewer: the "1 / 8" title and back chevron are theme black on the black viewer (the theme's AppBar `iconTheme` / `titleTextStyle` override the viewer's white `foregroundColor`), so they are barely visible.
- Em dashes: "Birthdays, trips, exams — Cheeko brings them up" (House rules, Upcoming); `Using "Cheeko" — would be moved` (Who is this Cheeko for?); the streak card and streak screen legend ("Rest day — free, the run carries on", "Quiet day — nothing recorded", "Today — still open").
- Profile: the "Device" section subtitle repeats the page's "Manage your account and settings". Spelling varies between "Wifi Setup", "Wi-Fi network" and "WiFi".
- Notifications screen uses stock Material styling (plain AppBar, purple button), unlike the rest of the app, and says "CheekoAI".
- Today's chats "everyone" thread labels every character's reply "Cheeko" (Home maps all non-child lines to "Cheeko"), so Nani's lines would read as Cheeko there.

---

# Onboarding (setup/)

These use the same method as above: real widgets from commit d49af42, the app theme and fonts, fake services and a fake in-process network. Each PNG is 1179 x 2556 (393 x 852 pt at 3x). The sample family is Priya Sharma, Aarav (born 2 Apr 2020, so 6) and a Cheeko toy.

The tests are `tests/onboarding_shots_test.dart` (s04–s10) and `tests/onboarding_account_shots_test.dart` (s01–s03). To re-run everything, use `zsh tests/run.sh`.

| File | Widget / how it was reached | Notes |
|---|---|---|
| s01_walkthrough_signin | `WalkthroughScreen` | Rendered as on iPhone (`debugDefaultTargetPlatformOverride = iOS`), because "Continue with Apple" only exists on iOS. Android shows only the Google button. |
| s02a_parent_profile, s02_parent_consent | `ParentProfileSetupScreen` with name Priya Sharma, email priya@example.com, +91 9876543210, English | The three required boxes were ticked through the app's own "I have read and accept" dialogs. The marketing opt-in is left unticked. |
| s03a_intro … s03g_all_set | `InteractiveKidsOnboardingScreen`: intro, name "Aarav", birthday April 2 2020, the app's "Perfect! Aarav is 6 years old!" popup, Male, interests Animals + Dinosaurs + Science, English | Language is a single choice in the app, so there is no Hindi. The birthday was handed to the app's own date picker in code, so its calendar grid is not shown. **s03g "All set!"** was reached by jumping the page view past the "Complete Setup!" save, which would otherwise create a child on the server. |
| s04_setup_checklist_empty, s04_setup_checklist | `ToyActivationScreen(initialStep: 0)` → `WelcomeStepWidget`, both items tapped, scrolled to show Continue enabled | **"Location Services Enabled" is missing**: the app shows it only on Android (`dart:io Platform.isAndroid`), which a test on a Mac can't fake. This is exactly the iPhone checklist. |
| s05_setup_method | `ProvisioningMethodStepWidget`, Bluetooth selected | **Not reachable in the current app**: nothing in `lib/` uses this widget, and setup always goes to Bluetooth. |
| s06_scanning, s06b_found | `BleProvisioningStepWidget` with a fake Bluetooth service. "Found" shows Cheeko-7F3A and Cheeko-21C9; the app auto-connects to the first, so it shows a spinner. | The screen can't be handed a fake Bluetooth service, so the step is wrapped in a copy of `ToyActivationScreen`'s page frame (gradient, dots, page view). The same applies to s05, s07, s07b and s08. |
| s07_wifi_list, s07b_wifi_password, s08_sending_bluetooth | the Bluetooth path: "WiFi Setup", 5 networks as reported by Cheeko (Sharma Home WiFi strongest), the password dialog (masked), then sending with a spinner on the chosen network | **The Bluetooth path has no "Success! Rebooting" screen**: on success it goes straight to the code step. |
| s07_wifi_list_hotspot_method, s07b_wifi_password_hotspot_method, s08_sending, s08b_success | the older Wi-Fi hotspot path: `WifiConfigurationStepWidget` talking to a fake Cheeko hotspot (192.168.4.1) | This path is where the quoted strings live: "Select your home WiFi network", "Sending WiFi credentials to Cheeko...", and the success card with the 3-second countdown. The status line reads "Success! Rebooting Cheeko..." in code; the card says "WiFi Configuration Successful!". |
| s09_code_empty, s09_code_entered | copies of `../09_pairing_code*.png` (`ActivationCodeStepWidget`, code 482915) | — |
| s10_setup_complete | Home with the app's own "Cheeko setup complete." snackbar | **There is no dedicated completion screen.** After activation the app goes straight to Home. The snackbar is what the app shows after a Wi-Fi re-setup. |
| s11_home_after_setup | copy of `../01_home.png` | — |

## Differences from the phone
- **Status bar:** as in the first batch, the insets are laid out but the status bar area is blank.
- **Emoji and arrows:** the app relies on the phone's system fonts for these. The test engine has none, so the Mac's Apple Color Emoji and Arial Unicode stand in. Emoji therefore look like iPhone emoji; Android phones show Google's emoji instead.
- **Flutter version:** rendered on Flutter 3.32.8 with the same compatibility shims as before (`tests/flutter-3.32-compat.patch`).
