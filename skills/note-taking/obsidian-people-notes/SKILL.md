---
name: obsidian-people-notes
description: Create and update typed notes (People, Organizations) in Justin's Obsidian vault. Load this skill whenever Justin explicitly asks to create a note for a person, group of people, or organization.
platforms: [linux]
---

# Obsidian Typed Notes (People & Organizations)

Use this skill **only when Justin explicitly asks** to create a note for a person, group of people, or organization. Do not create these notes proactively.

This skill extends the base `obsidian` skill — load that one too for vault path resolution, file tool conventions, and wikilink rules.

See `references/note-examples.md` for real vault examples of each note type.

## Vault path

`/home/justin.guest/vault` (see `obsidian` skill for resolution rules).

## Destination folder

All typed notes (People and Organizations) go in **`<vault>/Notebook/`**, not the vault root.

## Before creating: check for an existing note

Always search first:
1. Search `<vault>/Notebook/` by filename (person's name or org name).
2. Search contents for `category: "[[People]]"` or `category: "[[Organizations]]"` + the name.

If a note exists, update it rather than creating a duplicate.

## Filename

Use the **person's full name** or **organization's full name** as the filename:

```
Karen Gaul.md
Winchester-Thurston School.md
```

The `id` frontmatter field holds the timestamp — the filename is the name, not the timestamp. This matches every existing typed note in the vault.

Use the **current wall-clock time** for `id` and `daily_note`. When creating multiple notes in one run, increment timestamp by one second per note to avoid collisions.

## Frontmatter — People

```yaml
---
id: 'YYYYMMDDHHmmss'
daily_note: '[[YYYY-MM-DD dddd]]'
category: "[[People]]"
---
```

## Frontmatter — Organizations

```yaml
---
id: 'YYYYMMDDHHmmss'
daily_note: '[[YYYY-MM-DD dddd]]'
category: "[[Organizations]]"
---
```

### Optional frontmatter fields

- **`aliases`** — list of alternate names. Use when Justin provides them, or when an org has common abbreviations. YAML list format:
  ```yaml
  aliases:
    - Winchester-Thurston
    - Winchester
    - WT
  ```
  Place `aliases` after the required three fields.

- **`project`** — quoted wikilink, placed last. Only use if Justin specifies.

### Quoting conventions (match existing notes exactly)

- `id` — single-quoted string: `'20260520144511'`
- `daily_note` — single-quoted wikilink: `'[[2026-05-20 Wednesday]]'`
- `category` — double-quoted wikilink: `"[[People]]"` or `"[[Organizations]]"`

## Body — People

Add context Justin provided (role, employer, relationships, tags). If none given, leave body empty.

Typical shape:
```
Grade 5 teacher at [[Winchester-Thurston School]].

- [[Jamie]]'s Grade 5 teacher
- [[Sam]]'s former teacher
```

**Family wikilinks:** When a relationship involves Justin's family, always use wikilinks:
- `[[Jamie]]` — child, they/them
- `[[Sam]]` — son (oldest)
- `[[Rosie]]` — daughter (youngest)

If Justin says "Sam" without context, it means `[[Sam]]` (his son). Same rule applies to all family members.

**Organization links:** When a person's employer or school is a known org in the vault, wikilink it: `[[Winchester-Thurston School]]`.

## Body — Organizations

Organizations are often "empty" notes (just frontmatter + blank body) that exist as link targets. That's fine — create them as stubs if Justin doesn't provide body content.

## Creating multiple notes

Create each as a separate file. Stagger timestamps by one second each.

## Updating existing notes

Use `patch` for targeted edits. Use `write_file` only if rewriting the whole note is cleaner.

## Pitfalls

- **Do NOT use Templater syntax** (`<% ... %>`) — Templater only runs inside Obsidian. Resolve timestamps yourself and write literal values.
- **Do NOT put typed notes in the vault root.** They belong in `Notebook/`.
- **Filename ≠ timestamp.** The filename is the person's or org's name. The timestamp lives only in the `id` field.
- **The `id` field comment "matching the filename" is wrong** — id matches the creation timestamp, filename matches the name.
- Do not run git commands on the vault; `bes-vault-sync` auto-commits.
