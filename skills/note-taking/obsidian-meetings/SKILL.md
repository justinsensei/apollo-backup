---
name: obsidian-meetings
description: Use when creating or cleaning up chronological meeting notes and managing Granola reconciliation under Logs/Meetings/ with category "[[Meetings]]".
version: 1.0.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [obsidian, logs, meetings, granola, reconciliation]
    related_skills: [obsidian, obsidian-logs]
---

# Obsidian: Meetings & Granola Management

## Overview
This skill governs chronological meeting notes, including formatting templates and the automated cleanup workflow for raw meetings synced from Granola.

---

## Folder & Category
- **Directory:** `/home/justin.guest/vault/Logs/Meetings/`
- **Category link:** `category: "[[Meetings]]"`

---

## Filename Conventions
- Filename format: `YYYY-MM-DD - Spaced Meeting Title.md`.
- Example: `2026-06-09 - SignLab Product Alignment.md`.

---

## Meeting Note Structure
```markdown
---
id: 'YYYYMMDDHHmmss'
daily_note: "[[Daily Notes/YYYY-MM-DD-weekday|YYYY-MM-DD Weekday]]"
category: "[[Meetings]]"
---

# Meeting Title

**Date:** YYYY-MM-DD
**Attendees:** [[Justin Goff]], [[Person Name]]

---

## Agenda
- 

## Notes
- 

## Action Items
- [ ] 
```

---

## Granola Reconciliation Workflow
Machine-generated meeting logs and transcripts from Granola drop directly into `/home/justin.guest/vault/meetings/`. To prevent clutter and ensure clean integration, they must be pre-processed and swept to `/Logs/Meetings/` by our vault hygiene automation:

1. **Scan Source:** Checks for any files inside `/home/justin.guest/vault/meetings/`.
2. **Inject standard frontmatter:** Parses the date from the file metadata or title, then inserts standard numeric `id` and `daily_note` links.
3. **Format cleanup:** Strips double hyphens, double rules, or extraneous sync headers.
4. **Relocation:** Saves the sanitized file to `/home/justin.guest/vault/Logs/Meetings/` and deletes the raw file from `/meetings/`.
