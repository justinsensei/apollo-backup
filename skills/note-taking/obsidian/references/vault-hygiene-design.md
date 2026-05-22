# Vault Hygiene Script — Design Notes

Scripts: `~/.hermes/scripts/vault_hygiene.py` (main), `~/.hermes/scripts/vault_hygiene_cron.py` (cron wrapper).

Cron job id: `0b12d967fdf6`, schedule: daily 8am, deliver: telegram (red issues only).

## Architecture

Two-tier design:
- **Auto-fix tier**: runs silently, applies safe structural corrections
- **Report tier**: emits findings to stdout; cron wrapper filters to 🔴 sections before Telegram delivery

The cron wrapper (`vault_hygiene_cron.py`) imports stdout from the main script and only passes through lines under `## 🔴` or `## ⚠️  Move conflicts` headers. Clean runs and auto-fix-only runs produce no output → no Telegram message (watchdog pattern).

## Auto-fix decisions

### Misplaced daily notes
**Detection:** filename matches `YYYY-MM-DD (Weekday).md` exactly — no extra words after the weekday name.
**Rationale:** meeting notes also have date prefixes but always have a topic word after the date. Pure `YYYY-MM-DD Weekday.md` = daily note that landed in the wrong folder.
**Action:** move to `Daily Notes/`.

### Tag-to-category conversion
**Always convert:** `#people`, `#person`, `#organizations`, `#organization` — these are unambiguous object-note indicators.
**Date-prefix only:** `#meetings`/`#meeting`, `#projects`/`#project` — these tags are used loosely on non-object notes (e.g. workshop attendee notes get `#project`). Only convert if the filename starts `YYYY-MM-DD`, which signals it was created as an intentional object note.
**Action:** write `category: "[[Wikilink]]"` to frontmatter, remove tag from body.

**Pitfall discovered:** `Dianne AI Workshop 20260420141613.md` had `#project` but was workshop pre-work, not a project object note. No date prefix → correctly skipped.

## Report-only decisions

### Wrong folder
Any note with a `category:` wikilink outside `Notebook/` or vault root. Root is allowed because project notes intentionally live there (manage-projects convention). `Categories/` is excluded — those notes legitimately live there.

### ID conflicts / Missing ID / Missing daily_note
Report but never auto-fix — these require human judgment about which value is canonical or what the creation date actually was.

### What's intentionally skipped

| Folder | Reason |
|--------|--------|
| `Granola/` | Third-party schema (granola_id, attendees, etc.) |
| `Readwise/` | Plugin-managed, gets overwritten on sync |
| `Daily Notes/` | Backfilling daily_note is low-value; daily notes don't self-reference that way |
| `Templates/` | Contains live Templater syntax — never auto-edit |
| `Categories/` | Notes legitimately live in their own folder |
| Root daily notes | `YYYY-MM-DD Weekday.md` in root = today's current note, not a misplacement |

## Known persistent issues (as of 2026-05-22)

- `References/2026-06 Sienna PA Registration.md` — no frontmatter, just a PDF embed. Will keep alerting until manually fixed.
- Today's daily note `2026-05-21 Thursday.md` had stale `id: "20260127154919"` (hardcoded in template). Check `Templates/Daily Note.md` to ensure Templater expression generates fresh timestamps.
