# Cheeko Web Voice Demo Implementation Plan

**Goal:** Let a v2 website visitor confirm their identity with Google and start a temporary, isolated live voice conversation with Cheeko.

**Architecture:** Use the existing Firebase project for a Google popup in the static site. Exchange the Firebase ID token through a dedicated manager API route for a short-lived, demo-only token. The route verifies Firebase directly and stays outside normal product-account creation/linking. Use that demo token to create a fixed Cheeko LiveKit room. Mark the room as a website demo so the Python realtime worker uses Cheeko's persona without device data, memory tools, web search, transcript logging, or persistence.

**Tech Stack:** Firebase Authentication, Firebase Admin, Express, Prisma/PostgreSQL, LiveKit server/client SDKs, Python LiveKit Agents, vanilla HTML/CSS/JavaScript, Jest, and Pytest.

## Implementation checklist

- [x] Add `firebase_uid` to the isolated website lead and remove email challenge storage.
- [x] Add `POST /toy/web-demo/auth/google` with Firebase token verification, Google-provider enforcement, verified-email enforcement, rate limiting, and short-lived opaque demo-token issuance.
- [x] Keep the web-demo authentication boundary separate from normal `sys_user` account middleware.
- [x] Remove the email request/verify endpoints, code generator, SMTP sender, challenge model, and related environment configuration.
- [x] Keep the existing token-protected LiveKit start/stop endpoints and fixed Cheeko dispatch.
- [x] Keep the Python agent's website-demo data, tool, transcript, and persistence isolation.
- [x] Replace the website email/code stages with **Continue with Google** using the existing Firebase project.
- [x] Sign the browser out of its temporary Firebase client session after the demo-token exchange.
- [x] Preserve the existing **Hear me** behavior and limit the new **Talk** behavior to Cheeko.
- [x] Add tests for valid Google exchange, non-Google rejection, missing tokens, removed email routes, voice ownership, and room cleanup.
- [x] Add a temporary rate-limited guest-token path that bypasses and hides Google verification while voice testing is active.
- [x] Keep the Google UI and endpoint dormant so `WEB_DEMO_GOOGLE_AUTH_REQUIRED=true` restores verification without a frontend change.
- [x] Verify JavaScript syntax, Prisma schema, focused manager API tests, Python isolation tests, MCP route protections, and diff integrity.

## Deployment configuration

- Firebase Authentication must have Google enabled and the v2 website domains authorized.
- The manager API uses its existing Firebase Admin credentials.
- `WEB_DEMO_SECRET` and existing LiveKit credentials remain required server-side.
- Netlify proxies `/api/web-demo/*` to `/toy/web-demo/*` on the manager API and permits microphone access for the site.
