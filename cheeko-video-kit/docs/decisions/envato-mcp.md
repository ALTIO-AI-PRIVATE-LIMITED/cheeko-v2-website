---
name: envato-mcp
description: Envato Elements MCP (https://mcp.envato.com/mcp) needs NO sign-in; search-only (music, SFX, stock video, photos…), returns title/author/link, no downloads or previews
metadata:
  type: reference
---

Envato MCP: `https://mcp.envato.com/mcp`, in Claude Code user config as `envato` (HTTP, shows ✔ Connected), set up 2026-09-28. The claude.ai/desktop custom-connector route FAILED ("Couldn't register with envato's sign-in service", ref ofid_9d1d9877070b3686) because the server has no OAuth at all — no .well-known metadata, and `initialize`/`tools/list`/`tools/call` work unauthenticated. So don't add it as a claude.ai connector; the Claude Code config entry is enough (tools load in NEW sessions).

Tools: search_music, search_sound_effects, search_stock_video, search_photos, search_graphics, search_fonts, search_video_templates, … (args: searchTerms, page, perPage, sortBy, filters). Results = title, author, item_url only — no preview audio, BPM or duration, and no downloads. If the tools aren't loaded in a session, call it directly with curl JSON-RPC (POST, Accept: application/json, text/event-stream).

**How to apply:** for music, shortlist 3–5 tracks with links; Ravi listens, downloads on envato.com, registers the licence to the video name (e.g. "Cheeko V06 Imagine") and drops the file in Drive `cheeko ai videos/01 Shared assets/Music/`. Never log in to Envato or download for him. See [[cheeko-marketing-videos]].

**Built-in browser login (2026-09-28):** Ravi signed in to Envato himself in the desktop app's built-in browser (lands on app.envato.com). The sign-in persists across sessions. Agreed workflow: I shortlist, then ask per item ("Download X and register the licence as 'Cheeko V0n <Name>'?") and only download/register after an explicit yes. Never touch account settings, billing or sign-out.
