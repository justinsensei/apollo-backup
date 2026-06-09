---
name: obsidian
description: Core settings, paths, frontmatter schemas, baseline conventions, and note triage/sorting mapping rules for Justin's Obsidian vault.
version: 1.4.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [obsidian, core, conventions, paths, frontmatter, triage, sorting]
    related_skills: [obsidian-contacts, obsidian-notes, obsidian-logs, obsidian-utilities]
---

# Obsidian: Core Vault Conventions & Triage Routing

## Overview
This is the foundational skill for interacting with Justin's Obsidian vault. It defines paths, general note-creation rules, frontmatter fields, standard formatting conventions, and global note-triage routing rules.

---

## Vault Path
- Vault root directory: `/home/justin.guest/vault`
- Environmental variable: `OBSIDIAN_VAULT_PATH` set in `~/.hermes/.env` (resolves to `/home/justin.guest/vault` inside VM).

---

## Baseline Conventions

### Frontmatter Schema
Every manual note must have a YAML frontmatter block containing at least these fields:
```yaml
---
id: 'YYYYMMDDHHmmss'                 # Numerical string based on creation time
daily_note: "[[Daily Notes/YYYY-MM-DD-weekday|YYYY-MM-DD Weekday]]" # Link to creation day
category: "[[CategoryName]]"         # Single category link (quoted wikilink)
---
```
- Use single quotes `'` or double quotes `"` around IDs and wikilinks to ensure YAML parsing is safe.
- **`aliases`** (optional): YAML list of alternative names for easy lookup.
- **`project`** (optional): Quoted wikilink pointing to a parent project (placed last in frontmatter).

### Formatting Rules
- **Horizontal Rules:** Always use exactly three hyphens `---` on a line by itself to represent a horizontal divider. Never use two hyphens or other symbols.
- **Filename Case:** All regular notes (except Daily Notes and Meetings which use date prefixes) must be capitalized normal-spaced names, e.g. `Jamie's room.md`, `Aly Lalji.md`. Do not use kebab-case or lowercase hyphenated filenames.

### Git & Synchronization
- Do NOT run `git` commands (add, commit, push) inside the vault. The background watcher `bes-vault-sync` handles commit and synchronization to GitHub automatically within seconds of filesystem writes.

---

## Global Note-Triage Routing Table

Notes are categorized with a single `category` YAML property containing a quoted wikilink to its category note. Based on this category, they must be sorted into the corresponding folder (matching the `Type:` folder mapping in the category's definition file):

| Target Folder | Target Category Link | Description / Type | Sub-skill Guidance |
|---|---|---|---|
| `Contacts/` | `category: "[[People]]"` | Individual contacts, friends, family, collaborators | `obsidian-people` |
| `Contacts/` | `category: "[[Organizations]]"` | Companies, schools, institutions, legal entities | `obsidian-organizations` |
| `Notes/` | `category: "[[Notes]]"` | Default category for conceptual, structured, or raw notes | `obsidian-notes` |
| `Notes/` | `category: "[[References]]"` | Useful facts, cheat sheets, guidelines, checklists | `obsidian-references-sources` |
| `Notes/` | `category: "[[Sources]]"` | Summaries, book reviews, articles, web clips | `obsidian-references-sources` |
| `Notes/` | `category: "[[Thoughts]]"` | Personal/ideas, current opinions, research questions | `obsidian-thoughts-beliefs` |
| `Notes/` | `category: "[[Beliefs]]"` | Trusted models, core guiding principles | `obsidian-thoughts-beliefs` |
| `Notes/` | `category: "[[Decisions]]"` | Team or individual decisions and reasoning logs | `obsidian-decisions` |
| `Notes/` | `category: "[[Projects]]"` | Hubs for notes about ongoing work, milestones, travel | `obsidian-projects` |
| `Daily Notes/` | `category: "[[Daily Notes]]"` | Daily notes containing schedules and work logs | `obsidian-daily-notes` |
| `Logs/` | `category: "[[Meetings]]"` | Chronological meeting agendas, summaries, outcomes | `obsidian-meetings` |
| `Logs/` | `category: "[[Readwise]]"` | Raw logs of what I've been reading (plus highlights) | |
| `Utilities/` | `category: "[[Categories]]"` | Category representation notes themselves (in `Utilities/Categories/`) | `obsidian-utilities` |

---

## Action Steps for Triage
1. **Determine Category:** Read note content and title. Map it to exactly one category above. Convert legacy inline tags (e.g. `#meeting`) to the property and remove from body.
2. **Update YAML:** Set `category: "[[<CategoryName>]]"` using targeted `patch`.
3. **Move File:** Relocate the file from `inbox/` to its corresponding target folder. Create folders with `mkdir -p` if missing.
