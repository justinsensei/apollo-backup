---
name: daily-rituals
description: "Master daily rituals and routines for Justin: Morning Briefing generation and Daily Wind-Down & Wrap-Up."
version: 1.0.0
author: Apollo
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [daily-rituals, morning-briefing, wind-down, routines, work-log, vault]
    related_skills: [obsidian, apollo-brain-ingest, workspace-integrations]
---

# Daily Rituals & Routines

This umbrella skill governs Justin's recurring daily rituals: the **Morning Briefing** (5:00 AM automated report and live review) and the **Daily Wind-Down & Wrap-Up** (evening interactive session).

---

## Ritual Submodules & Detailed Workflows

- **Morning Briefing:** See `references/morning-briefing.md` for generating the daily morning report, vault signal checks, schedule briefing, and canonical vault skill pointers.
- **Daily Wind-Down & Wrap-Up:** See `references/wind-down.md` for the 4-phase interactive evening session (Input candidates, Discovered contacts, Work log draft/alignment, Tomorrow's calendar preview).

---

## General Principles

1. **Vault as Source of Truth:** Live rules for briefings and wrap-ups are maintained directly in the vault under `.cursor/skills/`.
2. **Interactive Pacing:** Respect phase boundaries during interactive sessions. One phase per message, waiting for explicit confirmation.
3. **No Direct Daily Note Overwrites:** Preserve historical sections (such as `## 🌄 Morning Briefing`) when writing work log updates.
