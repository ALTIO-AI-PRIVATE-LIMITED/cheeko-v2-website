---
name: cheeko-device-modes
description: What the Cheeko toy can actually do (menu, radio, cards) and what the voice agent cannot trigger
metadata:
  type: project
---

Checked 2026-09-25 against firmware `cheeko-os-v2` and the live dev DB, because
a persona must never offer a capability the toy lacks.

Device main menu (carousel, `CheekoMainMenuId`), as a parent sees it:
**TALK, IMAGINE, GAMES, FUNNY VOICE, RADIO, SETTINGS**.
Rotate moves the carousel, select opens. Inside RADIO the transport row is
prev / play-pause / next: rotate changes station, select toggles play.

**The voice agent CANNOT start radio, rhymes or card content.** There is no
play/radio tool in picoclaw, and no server-to-device command for it — the
firmware's `radio_stream` is a FreeRTOS task name and `screen` is outbound
device info, not an inbound command. So a persona may only GUIDE a parent
through the menu, never promise to do it. Making it actually act would need a
new p2p command + firmware handler + a worker tool.

Real device event vocabulary (`device_analytics_event.event_name`) with dev
volumes: `content_track_start` 1454, `card_session_start` 1248,
`ai_talk_start` 1211, `content_start` 1020, `game_start` 770,
`radio_start` 190. Cards are the dominant interaction, not conversation.

Radio is genuinely used: 162 plays, 17 devices, 20 stations (Dance Party,
Fun Kids Live, Happy Songs, Bedtime Stories, Tiny Tunes, Bollywood Fun).

RFID cards arrive over `devices/p2p/<mac>` as `card_ai` (switch character) or
`card_content` (play a packaged audio skill). `ai_device.mode`
(conversation/music/story) exists and `cycleMode` flips it, but every one of
the 46 dev devices sits on `conversation` — it is not what drives radio.
