# Cheeko — Website (v2)

Marketing site for **Cheeko**, the screen-free, voice-first AI learning toy for Indian children (ages 2–8) by **Altio AI Pvt. Ltd.**

**Live:** https://cheeko-site.netlify.app

---

## 1. Creative brief

**Product.** Cheeko is a handheld, screen-free toy: a child taps/places a physical RFID card and Cheeko tells a story, plays a rhyme, runs a game, or answers a question out loud. A parent app keeps grown-ups in control. Hero colourway: sunshine yellow (also white + pink). Mascot: an orange, green-eyed fox.

**Audience.** The buyer is the **parent** (25–40, urban/semi-urban India, screen-anxious); the user is the **child** (2–8). The parent makes the purchase decision; the child creates the demand.

**Objective.** Make parents feel Cheeko is a *trustworthy, guilt-free alternative to handing over a phone* — and make the magic obvious in seconds.

**Insight.**
> Parents don't actually fear screens — they fear *passive* attention. They want their child *lost in imagination*, but the one thing that reliably captures the child is a glowing rectangle that **consumes** attention instead of **expanding** it.

**Big idea — "Imagination, out loud."**
Tap a card and a whole world appears — in the child's ears and imagination, never on a screen. The site proves this by *doing* it: as you scroll, you "operate" the product and watch worlds bloom out of the device.

**Tagline.**
- Master (headline): **"Less screen, more childhood."**
- Secondary (product line): *"Imagination, out loud."*

**Art direction — a deliberate dual-register system:**
- **Register A — the real world:** warm, 3D-claymorphic / Pixar-style (child, fox, home, the yellow device).
- **Register B — the imagination:** painterly, cinematic story-worlds (Ghibli/Disney-leaning) for what Cheeko plays — jungle, starry night, curiosity, play.
- **Palette:** orange `#F36E24`, golden `#FFCE00`, fox-rust `#E0823A`, cream `#FFF5E8`, ink `#1B1B1B`. **Type:** Switzer. Warm, rounded, generous whitespace; the one dark moment is "The problem."

---

## 2. What's been built

A single-page scrolling experience. Top → bottom:

1. **Hero** — "Less screen, more childhood." Headline reveals word-by-word; floating "Story playing / Screen-free" chips; drifting particles; magnetic buttons; 3D-tilt hero image; scroll-progress bar; custom cursor.
2. **Hero → Problem dark takeover** — the hero **pins in place** and a dark circle **grows from the centre over the hero**, revealing **"The problem"** (big image, one line) in place. Then normal scroll resumes. (Scroll-scrubbed, native.)
3. **How it works — the centrepiece (4 cards + features):** one pinned device; each scroll **places a card from a different direction**, the **device screen reveals that world from the centre outward**, and the **whole section background becomes that world**:
   - Stories · Rhymes · Ask Cheeko (safe AI) · Games
   - then a **5th "Made for little hands" beat**: the device zooms in and **hand-drawn orange dotted-arrow labels** point to its parts (fox screen, top card slot, rotary dial, speaker). Mobile shows the labels as a grid.
4. **Proof strip + stats** — scrolling marquee of content types; animated counters (10+ languages, 100+ cards, 0 ads, ages 3–12).
5. **Story gallery** — horizontal-scroll of vertical story-cards (Jungle, Mythology, Bedtime, Rhymes, Languages) + a "+100 more → Get Cheeko" closing card.
6. **Languages** — the regional-language moat (tappable chips).
7. **Safe AI ("Ask Cheeko")** — tutor-not-friend, mic transparency.
8. **For parents + bedtime** — control + the grandmother bedtime moment.
9. **Choose your Cheeko** — colourway switcher (yellow / white / pink), consistent product shots.
10. **CTA** — ₹5,999, confetti on "Get Cheeko." **Footer.**
- Site-wide: **chapter dots** (right rail), background-wash morph, soft warm theming.

**Known TODOs / parked:**
- Exact pixel-match of the world art to the device screen in "How it works" (registration is close; a cleaner masking approach is planned).
- Mobile QA polish pass.
- Final marketing copy + real social proof (ratings/press).
- Custom domain (cheekoai.in) + favicon / OG share image.
- Hero video is a low-res motion test; a premium version is pending.

---

## 3. Tech & structure

Deliberately **dependency-light** — a single static HTML file, no build step, no framework.

| Layer | Choice |
|---|---|
| Markup/Style | Plain HTML + CSS (one `<style>` block) |
| Interactions | **Vanilla JS** — all scroll effects are hand-written `requestAnimationFrame` + scroll listeners, organised as one IIFE per effect |
| Font | Switzer (self-hosted, `assets/fonts/`) |
| External | `canvas-confetti` via CDN (the only third-party script) |
| Hosting | Netlify (static) |

```
site/
├── index.html        # the whole site (CSS top · HTML middle · JS bottom)
├── netlify.toml       # publish config (publish = ".")
├── server.py          # tiny local preview server
├── README.md
└── assets/
    ├── fonts/switzer-variable.ttf
    └── img/           # device renders, fox, painterly worlds, cards, colourways, logo
```

**Why no GSAP/React/Lenis:** a heavy smooth-scroll library broke native scrolling mid-build, so everything was rebuilt on native scroll — fast, robust, and easy for any developer to edit.

---

## 4. Run locally

```bash
python3 server.py        # serves http://127.0.0.1:8123 and proxies /api/web-demo/*
```

The Cheeko **Talk live** demo also needs the Manager API running on
`http://127.0.0.1:8002` and the Cheeko LiveKit voice worker running. If the
Manager API uses another host, set `CHEEKO_MANAGER_API_URL` to its origin when
starting `server.py`. Restart an older preview server after changing this file.
Plain `python3 -m http.server` only serves files and returns HTTP 501 for the
demo's POST requests. On Netlify, `netlify.toml` handles the API proxy instead.

Talk live is available in four character dialogs (Cheeko, Quizzy Bee,
Nani, and Mitthu). Each dialog starts a separate 60-second
LiveKit session with that character's manager persona. **Talk** opens the mic;
**Done talking** closes that turn; **Listen** plays the character audio and
**Pause listening** pauses it. Closing the dialog ends the room.

Talk live requires Google sign-in through the `cheekoai` Firebase project.
The Manager API verifies the Google Firebase ID token and issues a temporary
website token. Each Google identity can start at most ten one-minute Talk
sessions across all characters, tabs, devices, and sign-ins. Starting a session
uses one allowance even if it ends early. The allowance never resets. At the
limit, the website displays a message and the Manager API refuses another room.
Guest access is disabled, including tokens issued before this change.

The Manager API needs `FIREBASE_PROJECT_ID=cheekoai`, a valid
`FIREBASE_SERVICE_ACCOUNT_PATH` or `FIREBASE_SERVICE_ACCOUNT`, a dedicated
`WEB_DEMO_SECRET` (or existing `SERVICE_SECRET_KEY`), the web-demo database
migration, and its usual LiveKit URL/key/secret. In Firebase Authentication,
enable Google as a sign-in provider and add the deployed website domain to
Authorized domains. The Firebase service account and LiveKit secrets stay on
the server, never in website JavaScript.
The voice worker must be registered under the same name as
`WEB_DEMO_AGENT_NAME` (default `cheeko-agent`). For the local Picoclaw setup,
copy `LIVEKIT_URL`, `LIVEKIT_PUBLIC_URL`, `LIVEKIT_API_KEY`, and
`LIVEKIT_API_SECRET` from `admin-dashboard/.env` into `manager-api-node/.env`,
set `WEB_DEMO_AGENT_NAME=cheeko-web-demo`, restart the Manager API, then run:

```bash
python3 scripts/run-local-web-demo-worker.py
```

The runner uses the existing local Picoclaw config and Manager API service key,
and gives website rooms a separate temporary workspace. Keep it running while
testing. Restart the Manager API and worker after their configuration or code
changes.
Guest access also requires the `20261003000000_web_demo_guest_nullable_lead`
Manager API migration when an existing database has a non-null `lead_id` on
`web_demo_access_session`.

## 5. Deploy

Static deploy to Netlify (project: `cheeko-site`). Any static host works — just publish this folder.

---

*Built as a living prototype. Edit `index.html` directly; the JS effects are clearly commented (hero dark takeover · feed sequence · horizontal gallery · etc.).*
