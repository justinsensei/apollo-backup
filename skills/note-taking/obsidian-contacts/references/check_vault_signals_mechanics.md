# Background Script Mechanics: check_vault_signals.py

## Overview
The `check_vault_signals.py` script is a background process running in Justin's vault that automatically maintains contact timelines and discovers potential new contact cards (unresolved links). It is a major driver of automation, but poses significant risks of timeline pollution and link-hijacking if contacts or aliases are not structured properly.

---

## How It Works

### 1. File Modification Tracking
The script uses a watermark stored at `~/.hermes/state/vault_signals_watermark.json`. It only scans markdown files modified *after* this timestamp.

### 2. Entity Index Loading
It builds an in-memory index of all existing contact cards by scanning `/vault/Contacts/` and `/vault/inbox/`.
- **Target Filtering**: It looks inside files for `category: "[[People]]"` or `category: "[[Organizations]]"`.
- **Alias Resolution**: It parses the YAML frontmatter `aliases:` list of each card, enabling it to map short names or spelling variations back to full-name files.

### 3. Timeline Enrichment (The Matching Engine)
For every scanned modified file, the script tries to match existing entities in three ways (case-insensitively):
1. **Explicit Wikilink Matching**: e.g., `[[John Wheeler]]` or `[[Contacts/John Wheeler]]`.
2. **Exact Name Match with Word Boundaries**: e.g., `\bjohn wheeler\b`.
3. **Exact Alias Match with Word Boundaries**: e.g., matching any alias listed in frontmatter (like `\bjanny\b`).

If a match is found, the script automatically appends a timeline entry to that contact's markdown file:
`- event_date | Mentioned in [[source_rel_path|source_title]]`

### 4. Unresolved Link Discovery
The script scans modified files for any `[[Target Link]]`.
- It ignores common system terms (such as `meetings`, `references`, `thoughts`), binary/image extensions, and date-formatted links.
- It checks if the link target exists as a filename anywhere in the vault *or* as an alias in any contact card.
- If it is truly unresolved, it gets added to `~/.hermes/morning-briefing/vault_signals_last_run.json` as a candidate for contact creation.

---

## Core Failure Modes & Pitfalls

### Pitfall A: Alias-Driven Link Hijacking (Common Word Collisions)
When a contact has a highly common or generic alias (like `Mac` for `Mac Lawrence`, `Ryan` for `Ryan Jaroncyk`, or `Georgia` for `Georgia Sullivan`), the word-boundary text matching will catch **any plain-text instance** of that word.
- **Example**: Mentions of "macOS", "MacMini", or "Mac Studio" will match `\bmac\b` and write false timeline entries to `Mac Lawrence.md`'s personal card.
- **Example**: Mentions of psychologist "Richard Ryan" in wellness articles will match `\bryan\b` and write false entries to nephew/in-law `Ryan Jaroncyk.md`'s card.
- **Example**: Mentions of "Georgia Tech" or the state "Georgia" will match `\bgeorgia\b` and pollute `Georgia Sullivan.md`.

### Pitfall B: Ghost-Link Multiplication (The "Sam" Problem)
If a generic first name like `Sam` is linked as `[[Sam]]` or `[[Contacts/sam]]`, but no card `Sam.md` exists on disk:
1. The script will flag it as an unresolved candidate.
2. If an agent creates a generic `sam.md` file, the matching engine will map **all** instances of "Sam" (including `Sam Burgess`, `Sam Eustace`, `Sam Liberty`, and his son `Sam Goff`) into that single generic file's timeline. This completely merges unrelated professional and personal histories into a corrupted timeline.

---

## Safety Guidelines for Future Agents

1. **Strict Alias Selection**:
   * NEVER register highly generic, common first names (like `Mac`, `Ryan`, `Georgia`, `Linda`) as standalone aliases if they collide with regional, corporate, technical, or other external terms in the vault.
   * If a first-name alias is absolutely necessary (e.g., for direct family members consistently referenced by first-name only, like `Jonny` or `Jackie` or `Jim`), verify that the name is highly distinct and has zero plain-text technical or business overlaps in the vault's daily or meeting notes.

2. **Full-Name Filename Defaulting**:
   * Always name contact files using full names (e.g., `Sam Goff.md` instead of `sam.md`, `Ruth Guzner.md` instead of `ruth.md`).
   * Never create generic placeholder cards (e.g. `sam.md`, `andy.md`, `ruth.md`).

3. **Link Corrections**:
   * When creating a full-name card for someone previously referred to by a short link (e.g., creating `Sam Goff.md` when old notes contain `[[Sam]]` or `[[Contacts/sam]]`), do a global search and replace to correct the old links to point directly to the full-name card with a clean display pipe (e.g., replace `[[Sam]]` with `[[Sam Goff|Sam]]`).
