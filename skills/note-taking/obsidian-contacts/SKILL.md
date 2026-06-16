---
name: obsidian-contacts
description: "Master conventions for the Contacts/ directory: governs People and Organizations categories, ID generation, and duplicate prevention."
version: 1.5.0
author: Bes
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [obsidian, contacts, people, organizations, folder-conventions]
    related_skills: [obsidian, obsidian-notes, obsidian-logs]
---

# Obsidian Type: Contacts Directory Conventions

This master skill governs the physical structure, coordinates, templates, and formatting rules of the `/Notes/Contacts/` directory in Justin's vault.

---

## 1. Directories & Storage Coordination

- **New Contacts Landing Directory:** `/home/justin.guest/vault/Inbox/`
- **Permanent Contacts Directory:** `/home/justin.guest/vault/Notes/Contacts/`
- **Duplicate Prevention Check:** Before writing any contact file, always search both `/Notes/Contacts/` and `/Inbox/` by name, abbreviation, or known aliases using:
  `search_files(target='files', path='/home/justin.guest/vault/Notes/Contacts', pattern='*')`
- **Relocation Boundary:** Only brand-new contact stubs created by Bes should land in `/Inbox/`. Never move or relocate existing contact files already in `/Notes/Contacts/` to the inbox; always update them in-place.

---

## 2. People Contacts

For individual contacts, family members, friends, or colleagues.

- **Category:** `category: "[[People]]"`
- **Constraint - No Family Deduction:** Do not attempt to automatically deduce or populate family relationships. Justin maintains these manually.
- **Constraint - No Third-Person Phrasing:** Avoid third-person phrasing like "Justin's colleague". Keep descriptions objective, direct, and concise.
- **No Timeline or Open Threads:** Rely entirely on Obsidian's backlinks for chronological navigation. Do NOT add a "Timeline" or "Open Threads" section to individual people profiles.

### People Profile Layout
```markdown
---
id: "YYYYMMDDHHmmss"
category: "[[People]]"
aliases:
  - Firstname
---

Short objective description of who they are and their role.

## State
- **Role:** Developer / Designer / Friend
- **Relationship:** Work colleague / Cousin / etc.
- **Family:** [[Spouse Name]] (spouse), [[Child Name]] (child) # Single-line list if relevant. No bullet list.
```

---

## 3. Organization Contacts

For companies, schools, partner organizations, vendors, or institutions.

- **Category:** `category: "[[Organizations]]"`

### Organization Profile Layout
```markdown
---
id: "YYYYMMDDHHmmss"
category: "[[Organizations]]"
aliases:
  - Acronym (e.g. WSP)
  - Short Name
---

> Executive summary: brief description of who this organization is and our connection. Keep it direct.

## State
- **Type:** School/Partner/Vendor/Employer
- **Key Contacts:** [[Person Name]], [[Another Person]]

## Open Threads
- Any active, open discussion points.

---

## Timeline
- YYYY-MM-DD | Context of creation or updates. Maintain chronological order with newest events at the top.
```

---

## 4. Shared Folder-Level Rules

### Filename Capitalization & Casing
- All contact files must use standard capitalized, spaced filenames (prefer full names over first-name-only filenames, e.g. `Andy Goff.md` instead of `andy.md`).
- Lowercase filenames are strictly forbidden (e.g., do not write `smartpass.md` or `duolingo.md`). Always use standard corporate capitalization (e.g. `SmartPass.md`, `Duolingo.md`).

### Common-Name Alias Safeguards
- Never register overly generic, high-collision first names (like `Mac`, `Georgia`, `Linda`, `Andrew`, `Andy`) as standalone aliases in frontmatter. This prevents automated scripts from matching unrelated system terms or locations.

### Contact ID Generation & Uniqueness
Every contact file must include a double-quoted 14-digit ID in its frontmatter:
- **Format:** `id: "YYYYMMDDHHMMSS"`.
- **Acquiring Timestamp:** Query the file birth/creation timestamp via `stat -c %W <filepath>`. Fall back to modification time (`mtime`) if birth time returns `0`.
- **Enforce Uniqueness:** If the generated ID matches any existing ID in the vault (common in batch operations), increment the last digit or two until the ID is completely unique.

### Pruning Obsolete Contacts
A contact note is considered safe to prune if:
1. It has zero backlinks or mentions across the vault.
2. The body of the note is completely empty (whitespace only) besides frontmatter.
*Always run a dry run and check with the user before performing deletions.*
