---
name: obsidian-notes
description: Use when managing the Notes/ directory, conceptual mapping, and coordinating Thoughts, Beliefs, Decisions, Projects, References, and Sources categories.
version: 1.0.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [obsidian, notes, folder-conventions]
    related_skills: [obsidian, obsidian-thoughts-beliefs, obsidian-decisions, obsidian-projects, obsidian-references-sources]
---

# Obsidian Type: Notes Directory Conventions

## Overview
This skill governs the physical structure and coordinate mapping of the `/Notes/` top-level directory in Justin's vault.

---

## Directory & Sub-skills
- **Directory:** `/home/justin.guest/vault/Notes/`
- **Sub-skills (Categories):**
  - **`obsidian-thoughts-beliefs`**: For raw reflections or core principles (`category: "[[Thoughts]]"` or `category: "[[Beliefs]]"`).
  - **`obsidian-decisions`**: For trade-offs, architecture decisions, and reasoning logs (`category: "[[Decisions]]"`).
  - **`Memory`**: For journal-like personal notes, conversations, and good days (`category: "[[Memory]]"`).
  - **`obsidian-projects`**: For ongoing project hubs, travel, or milestones (`category: "[[Projects]]"`).
  - **`obsidian-references-sources`**: For factsheets or Readwise web clips (`category: "[[References]]"` or `category: "[[Sources]]"`).

---

## Folder-Level Rules

### Distinguishing Scratchpads vs. Structured Concepts
- **Scratchpads (note type):** Kept unstructured, focused on thoughts, brainstorms, or transient ideas.
- **Structured Concepts (concept type):** Clearly defined terms, models, or entities. Keep these distinct to avoid conceptual drift.

### Naming Conventions
- All files under `/Notes/` must use Spaced, Capitalized names.
- Do not prefix concept or belief notes with timestamps or IDs in the filename.
- If a note is a historical record, a timestamp can exist at the end of the filename (e.g. `Armor framework for avoiding burnout 20250621083744.md`).

### Aliases
- Ensure complex, conceptual, or heavily-referenced notes define clean `aliases:` lists in their YAML frontmatter. This allows effortless wikilinking without typing the full exact title every time.
