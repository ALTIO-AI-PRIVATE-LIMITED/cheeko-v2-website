# Cheeko device screens (firmware render)

{{COUNT}} screens rendered from **cheeko-os-v2 @ {{COMMIT}}** (firmware {{VER}}) by compiling the firmware's own LVGL UI code on macOS and drawing into a 296x240 RGB565 framebuffer. Nothing was redrawn by hand.

Re-run for another commit: `fwsim/render.sh <commit>`. The repo is only read with `git archive`; its working tree and branches are never touched.

## How it works

- **Real code, compiled for the host:** everything in `main/cheeko_os/`, `main/display/` (lcd_display, cheeko_face, cheeko_character_art, lvgl_display, fonts, images), `cheeko_companion`, `cheeko_sd_image_loader`, `settings.cc`, `content_crypto.cc`, and LVGL 9.4 from `managed_components`. The board's `CustomLcdDisplay` class (card reveal/feedback, download overlay, Imagine hooks, the CheekoOs owner), the Funny Voice name table and the haptics names are copied **verbatim** out of `cheeko_v2_board.cc`, `cheeko_voice_changer.cc` and `cheeko_haptics.cc` by `tools/extract.py`.
- **Driven the same way the device drives it:** CheekoOs `Show/Rotate/Select/Back/VoiceHold*/DrawTouchPoint`, and the same `SetStatus/SetEmotion/SetChatMessage/SetImagineStage` calls (with the same strings) that `application.cc` makes for each device state. Games are played by rotating to an option and pressing.
- **Stubbed (no effect on pixels):** FreeRTOS (single thread, tasks never run), NVS (RAM), audio, network, OTA, analytics and telemetry. Time runs on a simulated clock; LVGL timers and animations advance in 5 ms steps.
- **Config:** a real cheeko-v2 build's `sdkconfig.h` (consumer flavour, developer features compiled in), with the commit's `sdkconfig.defaults` overrides applied. Games shown are the 8 enabled ones: Animal, Numbers, Space, Jump, Paint, Trace, Memory, Piano.
- **Fonts:** the embedded PuHuiTi/Switzer/FontAwesome fonts, plus `font_puhui_basic_20_4` as the theme text font, which is what the assets partition supplies on the device.
- **SD card:** `CHEEKO_SD_CARD_COPY/cheeko` merged with `sd_card_assets/cheeko`, read through the firmware's own loader. `"/sdcard"` paths are rewritten to `"./sdcard"` in the scratch copy only.

## Where the renders can differ from the device

- **Simulated status data:** the clock reads 10:30 AM on 28 Sep 2026 and advances as the run goes on. Battery is 80% and discharging, except on the `15_*` screens. Wi-Fi is connected to "HomeWiFi" at -52 dBm with 2 saved networks. The star counter in the Games header adds up the stars earned earlier in the same run.
- **Sample content:** the Talk reply ("The sky looks blue…") and the Imagine prompt ("a dinosaur flying a kite") are sample text. On the device both come from the server.
- **Imagine result (`09_imagine_5_result`):** the picture is the home wallpaper standing in for the AI-generated image. The frame and caption layout are real.
- **Animation timing:** screens with animations (loading spinner, card reveal, pulsing dots, mouth) are caught at a fixed point in the animation.
- **Not rendered:** the board's power-on splash before LVGL starts (only LcdDisplay's boot page is shown, as `00_boot`), OTA screens, the developer/diagnostics screens, and the BLE Wi-Fi pairing flow beyond its first "Getting ready" card. Pairing restarts the device, so it cannot be driven here.
- **Colours:** RGB565 is expanded to RGB888 exactly. The real panel's gamma, brightness and the physical rounded bezel are not modelled.

## Firmware behaviour visible in these renders (not render bugs)

- **Talk picker:** it lists only Cheeko and Quizzy (`kListedCharacterCount = 2`). The other five characters are reached through RFID "Hello" cards, so their session screens were produced with `SelectCharacterById()`.
- **Game result:** no star icons are drawn. `DrawGameResult` uses the Stickers game icon as the star image, and `CONFIG_CHEEKO_GAME_STAMP=n` compiles that icon out, so only the headline and text show.
- **NUMBERS game:** when the target is 8 or 9 the answer tiles collide, for example 9 / 9 / 9, because `cheeko_game_renderer.cc` `DrawNumber` clamps values above 9 to 9. The harness avoids photographing those questions.
- **Low battery:** the "Please charge me!" text (puhui_32) wraps onto two lines and overlaps the "5% battery left" line.
- **Headers:** long screen titles ("Settings", "More settings", "Themes") run into the time pill.
- **Imagine thinking screen:** the "Painting your idea..." headline is clipped to "Painting / our idea." by its label box.
- **Card-talk knob prompt (`14_card_talk_knob_prompt`):** the hint is a scrolling ticker, so it was caught mid-scroll.
- **Themed runs (`dinku_*`, `robu_*`):** these were rendered with NVS `cheeko/mascot` set to that mascot. The file names keep Cheeko's slot names (for example `talk_picker_1_cheeko`), but the screen shows the mascot. The boot page keeps the fox logo because it is a compiled-in image.
