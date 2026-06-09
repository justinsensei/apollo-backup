---
name: obsidian-categorize-and-sort
description: Use when triaging, organizing, or sorting a new or incoming note (e.g. in inbox/) by determining its category, formatting its template via sub-skills, and moving it to its correct directory.
version: 1.3.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [obsidian, operations, triage, sorting, taxonomy]
    related_skills: [obsidian, obsidian-people, obsidian-organizations, obsidian-daily-notes, obsidian-meetings, obsidian-decisions, obsidian-thoughts-beliefs, obsidian-projects, obsidian-references-sources]
---

# Obsidian Operation: Categorize and Sort Notes

## Overview
This operational skill handles the workflow of triaging new, raw, or incoming notes. It guides determining the category, formatting the note structure using category-specific sub-skills, and moving the file to its designated physical folder.

---

## The Triage Process

### Step 1 — Determine the Category
Read the note content and title. Map the note to **exactly one** category from the table below. Convert legacy inline tags (e.g. `#people`) to formal category properties.

| Category Link | Destination Folder | Category-Level Formatting Sub-skill |
|---|---|---|
| `category: "[[People]]"` | `Contacts/` | **`obsidian-people`** |
| `category: "[[Organizations]]"` | `Contacts/` | **`obsidian-organizations`** |
| `category: "[[Notes]]"` | `Notes/` | **`obsidian-notes`** |
| `category: "[[References]]"` | `Notes/` | **`obsidian-references-sources`** |
| `category: "[[Sources]]"` | `Notes/` | **`obsidian-references-sources`** |
| `category: "[[Thoughts]]"` | `Notes/` | **`obsidian-thoughts-beliefs`** |
| `category: "[[Beliefs]]"` | `Notes/` | **`obsidian-thoughts-beliefs`** |
| `category: "[[Decisions]]"` | `Notes/` | **`obsidian-decisions`** |
| `category: "[[Projects]]"` | `Notes/` | **`obsidian-projects`** |
| `category: "[[Daily Notes]]"` | `Daily Notes/` | **`obsidian-daily-notes`** |
| `category: "[[Meetings]]"` | `Logs/Meetings/` | **`obsidian-meetings`** |
| `category: "[[Categories]]"` | `Utilities/Categories/` | **`obsidian-utilities`** |

---

### Step 2 — Format the Content (Sub-Skill Handoff)
Once the category is identified:
1. Ensure the note has standard frontmatter (`id`, `daily_note`, `category`).
2. Load the corresponding category-specific sub-skill (e.g. `obsidian-people` for a biography note, or `obsidian-decisions` for a choice log).
3. Format or scaffold the note body according to that category's standard template.

---

### Step 3 — Move the File to its Target Folder
Identify the target folder from the table above. Move the file from its source folder (such as `inbox/`) to the target destination folder.
```bash
mv "/home/justin.guest/vault/inbox/Some Note.md" "/home/justin.guest/vault/Notes/Some Note.md"
```
*Note: Always verify or create the target directory using `mkdir -p` before moving.*

---

## Common Pitfalls
- **Multiple Categories:** Never assign multiple categories to a single note. Every note gets **exactly one** category.
- **Leaking Inbox:** Do not leave notes in `inbox/` once categorized. All processed notes must reside in their taxonomy folders.
- **Links Verification:** moves are generally safe since Obsidian auto-resolves links by note name regardless of folder structure.
