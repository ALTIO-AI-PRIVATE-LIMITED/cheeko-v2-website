# Cheeko Web Voice Demo Design

> Historical design note: the temporary guest-testing mode below was removed on 2026-10-03. Current Talk live access requires Google sign-in and permits ten lifetime one-minute sessions per verified Google identity. See the website README for current setup.

## Goal

Add a website-only Cheeko voice demo to the v2 marketing site. A visitor clicks **Talk**, confirms their identity with Google, and receives temporary access to a live back-and-forth voice session with the existing Cheeko realtime agent.

## Scope

- One character: Cheeko.
- Google authentication through the existing `cheekoai` Firebase project.
- Website-only lead registration; no normal Cheeko product account, password, device profile, child memory, quiz state, or transcript persistence.
- One isolated LiveKit conversation per authenticated website session.
- Existing Cheeko persona and configured realtime voice provider.

## Temporary testing mode

Google verification is currently hidden so the voice experience can be tested directly. With `WEB_DEMO_GOOGLE_AUTH_REQUIRED=false` (the current default), the website requests a rate-limited anonymous token from `POST /toy/web-demo/auth/guest` and immediately begins the normal microphone and LiveKit flow. Guest access does not create a lead or product account. Setting the flag to `true` disables guest issuance with HTTP 403; the existing website then reveals **Continue with Google** without another frontend deployment.

## User flow

1. The visitor opens Cheeko's character dialog and clicks **Talk**.
2. The dialog offers **Continue with Google**.
3. Firebase completes Google authentication in a popup and returns an ID token to the browser.
4. The browser sends that ID token to the dedicated web-demo endpoint.
5. The backend verifies the token with Firebase Admin, requires the `google.com` provider and a verified email, records the demo lead, and returns a short-lived opaque website token.
6. The browser requests microphone permission and starts an isolated LiveKit room.
7. Cheeko greets the visitor and supports natural turn-taking, interruption, mute, and manual end.
8. The browser and backend close the room at the hard session limit.

## Architecture

The manager API owns Firebase identity verification, website access tokens, rate limits, LiveKit room creation, agent dispatch, and cleanup. It verifies Firebase directly for this endpoint and deliberately does not use the mobile product-account middleware, so it never creates or links a `sys_user`. The browser signs out of the temporary Firebase client session after the exchange and retains only the short-lived demo token.

The static website receives only short-lived LiveKit participant credentials. The existing Python GPT-Live worker recognizes `session_kind=website_demo`, loads Cheeko's persona and realtime provider, and disables device data, tools, transcript logging, summaries, and persistence.

## Backend API

### `POST /toy/web-demo/auth/google`

Requires `Authorization: Bearer <firebase-id-token>`. The backend verifies the token with Firebase Admin and accepts only a Google identity with a verified email. It upserts the isolated website lead and returns `{ token, expiresAt, email }`.

### `POST /toy/web-demo/voice/start`

Requires `Authorization: Bearer <website-token>`. It allows one active room per token, creates a `webdemo_<uuid>` LiveKit room with two participants, dispatches the fixed Cheeko agent with demo metadata, and returns `{ url, token, sessionId, expiresAt }`.

### `DELETE /toy/web-demo/voice/:sessionId`

Requires the same website token. It only deletes a room owned by that token and is idempotent.

## Storage

Dedicated Prisma tables hold Google-verified website leads, website access sessions, and active voice sessions. Access sessions may temporarily have no lead while guest testing is enabled. Access tokens are stored only as SHA-256 hashes. The website lead stores the Firebase UID, normalized verified email, and timestamps. Audio and conversation transcripts are not stored.

## Voice isolation

Website rooms never use a device-shaped room name or MAC address. Demo dispatch metadata contains `session_kind: "website_demo"`, `character: "Cheeko"`, the selected public language, and server-owned realtime settings. In demo mode the worker:

- fetches only Cheeko's character session and active realtime provider;
- omits progress, workspace memory, quiz state, `remember_child_fact`, and web search;
- does not create `SessionRecorder`, summarize, persist, or log utterance text;
- adds a short-demo instruction overlay with concise responses and no requests for personal information;
- closes naturally near the deadline.

## Limits, security, and privacy

- Dedicated Google-exchange and start-session rate limiters.
- One active voice session per website token.
- Fixed Cheeko character, runtime agent, provider, and voice; callers cannot override them.
- Short website and LiveKit token lifetimes.
- Server-side room deletion after the configured demo duration and cleanup of stale `webdemo_` rooms.
- HTTPS/WSS transport; Firebase, LiveKit, and provider secrets stay server-side.
- CORS permits only configured website origins and local development origins.
- No password, email code, child/device memory, or transcript storage.

## Website UI

The existing **Hear me** control remains available. The Cheeko dialog adds a **Talk** control and a Google sign-in stage followed by the conversation stage. The conversation UI contains state, countdown, mute, and end controls. Errors remain inside the dialog. Closing the dialog disconnects and requests backend cleanup.

## Verification

Backend tests cover Firebase identity constraints, rejection of the removed email-code endpoints, token authentication, fixed dispatch configuration, room ownership, cleanup, and rate limiting. Python tests prove website rooms have no device MAC, memory tools, recorder, or manager persistence calls. Frontend checks cover the Google-auth markup/controller, microphone handling, LiveKit lifecycle, timeout, manual end, and modal close.
