# Vault Audit — 2026-05-22

Full structural and frontmatter audit of `/home/justin.guest/vault`.

## Vault size

| Folder | Files |
|--------|-------|
| Notebook/ | 324 |
| Daily Notes/ | 228 (archived) |
| Granola/ | 52 (summaries + transcripts) |
| Readwise/ | 112 |
| References/ | 38 |
| Templates/ | 7 |
| Root | 2 (today's daily note + Bes Setup.md) |
| **Total** | **~796** |

## Notebook breakdown

| Type | Count |
|------|-------|
| category: [[Meetings]] | 148 |
| category: [[People]] | 149 |
| category: [[Organizations]] | 1 |
| No category field | 25 |

- 153 notes are date-prefixed (`YYYY-MM-DD Title`) — these are meeting notes, correctly in Notebook.
- 171 notes have no date prefix — mix of People, Orgs, and uncategorized notes.

## Issues found

### 1. Misplaced daily notes in Notebook/ (5 files)
Files named `YYYY-MM-DD Weekday.md` (no topic after the weekday) accidentally in `Notebook/` instead of `Daily Notes/`:
- `2026-05-20 Wednesday.md`
- `2026-05-19 Tuesday.md`
- `2026-05-18 Monday.md`
- `2026-03-17 Tuesday.md`
- `2025-10-01 Wednesday.md`

Detection: filename `YYYY-MM-DD (Monday|Tuesday|…).md` + `#daily_note` tag OR no meeting content.

### 2. Notebook notes missing category (25 files)

Apparent types based on filename + tags:

| Tag/Pattern | Files | Suggested category |
|-------------|-------|--------------------|
| `#project` | AI Agents 2026 H1.md, Mobile Game Doctors.md | `[[Projects]]` |
| `#reference` | ASL Facts.md, Benchmarks - *.md (3 files) | `[[References]]` (doesn't exist yet) or leave uncategorized |
| `#trip` | Madeira 2026.md, Belize 2026.md | No category yet |
| Essay/journal | Sports fandom sucks, Fighting with Jamie, Brain dump on Bes, etc. | No category yet |
| `category:` field blank | Headaches 20260520142723.md | Needs value |
| Other (workshop notes, external content) | Dianne AI Workshop, Cursor on Agent-Powered Dev, etc. | Ambiguous |

Full list (25):
```
Sports fandom sucks 20260423102157.md
Dianne AI Workshop 20260420141613.md
ASL Facts.md
Tor's thoughts about Artemis-style code bots 20260514080631.md
2026-05-20 Wednesday.md  ← misplaced daily note
Spring Performance 20260501134243.md
2026-03-17 Tuesday.md  ← misplaced daily note
Single-agent for Clio for now 20260519111334.md
Response to Tor's thoughts on Artemis 20260514081149.md
Fighting with Jamie 20260519075445.md
AI Agents 2026 H1.md
2026-05-18 Monday.md  ← misplaced daily note
Mobile Game Doctors.md
Cursor on Agent-Powered Dev 20260513084557.md
The Beginning of Infinity 20260506092057.md
Benchmarks - notification opt-in rate.md
Bot thoughts - Clio vs Artemis 20260513091336.md
PostHog → CustomerIO 20260423101926.md
Benchmarks - Subscription page CTR.md
Madeira 2026.md
Belize 2026.md
2026-05-19 Tuesday.md  ← misplaced daily note
Benchmarks - user retention.md
Brain dump on Bes 20260519162610.md
2025-10-01 Wednesday.md  ← misplaced daily note
```

### 3. Bes Setup.md in vault root (1 file)
Sole project note with `category: "[[Projects]]"`. Lives in vault root by manage-projects convention, not in Notebook. This is INTENTIONAL per the manage-projects skill — project notes go in root.

### 4. Readwise — bulk import bug (112 files)
All 112 Readwise notes have identical malformed frontmatter from a one-time import run:
- `id: "2026052211:53 AM"` (should be `YYYYMMDDHHmmss`)
- `daily_note: "2026-05-22 Friday"` (plain string, should be `[[2026-05-22 Friday]]` wikilink)

These are auto-managed by the Readwise plugin — do NOT patch them manually, they'll be overwritten on next sync. Fix belongs in the Readwise import template/settings.

### 5. Daily Notes missing daily_note field
Many archived daily notes (in `Daily Notes/`) have `id` but no `daily_note` in frontmatter — they predate the `daily_note` convention. Low priority since the filename itself is the date reference.

## What to skip in a hygiene job

- `Granola/` — own schema, third-party managed
- `Readwise/` — own schema, plugin-managed
- `Daily Notes/` — backfilling `daily_note` field is low-value
- `Templates/` — contains Templater syntax, never auto-edit
- `.trash/` — ignore
- `.cursor/`, `.claude/` — IDE metadata, ignore
