---
name: obsidian-notes
description: "Master conventions for the Notes/ directory: governs Thoughts, Beliefs, Decisions, Projects, and general conceptual notes."
version: 1.1.0
author: Bes
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [obsidian, notes, thoughts, beliefs, decisions, projects, folder-conventions]
    related_skills: [obsidian, obsidian-logs, obsidian-contacts, obsidian-vault-jam]
---

# Obsidian Type: Notes Directory Conventions

This master skill governs the physical structure, coordinate mapping, templates, and formatting rules of the `/Notes/` top-level directory in Justin's vault.

---

## 1. Global Folder & Naming Conventions

### Saved Location
All permanent notes (Thoughts, Beliefs, Projects, References) are stored under `/Notes/` or its subdirectories. New drafts of Decisions or Concepts must first be created inside the `/Inbox/` directory for active manual review and triage.

### Filename Suffix ID Rule
- **Categories (Notes, Decisions, Thoughts, Memories, Concepts, Scraps, Beliefs):** Must use spaced, capitalized filenames ending in a unique 14-digit creation ID: `Title ID.md` (e.g., `Spaced Title 20260609120000.md`).
- **References & Projects:** Named `Title.md` without any ID suffix (e.g., `Ascend membership.md`).
- **Rationale:** The 14-digit ID suffix at the end of the filename provides a robust, redundant, and backward-compatible anchor. This allows background scripts to automatically heal and repair links if files are renamed or shifted across categories, preventing ghost links.

---

## 2. Thoughts & Beliefs

Governs unstructured personal reflections (`Thoughts`) and permanent guiding principles (`Beliefs`).

### Thoughts (Emergent Notes)
- **Category:** `category: "[[Thoughts]]"`
- **Layout:**
  ```markdown
  ---
  id: "YYYYMMDDHHmmss"
  daily_note: "[[YYYY-MM-DD Weekday|YYYY-MM-DD Weekday]]"
  category: "[[Thoughts]]"
  ---

  # Thought Title

  What is the core idea or reflection? Keep it atomic and brief.

  ---

  ## Context & Details
  - Emergent observations...
  - Open questions...
  ```

### Beliefs (Evolved Convictions)
- **Category:** `category: "[[Beliefs]]"`
- **Layout Requirements:** Beliefs represent mature mental models and must feature a concise thesis followed by:
  - **Core Tenets:** Exactly 3 numbered, actionable pillars with **bolded names**.
  - **Application Scenarios:** Exactly 2 scenario bullets with **bolded contexts**.
  - **Related & Sources:** Links to supporting material.
  ```markdown
  ---
  id: "YYYYMMDDHHmmss"
  daily_note: "[[YYYY-MM-DD Weekday|YYYY-MM-DD Weekday]]"
  category: "[[Beliefs]]"
  ---

  # Belief Title

  Core thesis or definition paragraph. Concise, high-level statement of what this belief represents.

  ---

  ## Core Tenets
  1. **[Tenet 1 Name]:** Description of the first fundamental pillar.
  2. **[Tenet 2 Name]:** Description of the second pillar.
  3. **[Tenet 3 Name]:** Description of the third pillar.

  ## Application
  - **[Scenario A]:** Specific guideline on how this principle is put into practice.
  - **[Scenario B]:** Practical application scenario or playbook rule.

  ---

  ## Related
  * [[Related Note A]]

  ## Sources
  * [[Source Note or Book Link]]
  ```

### Reversion & Promotion Constraints (June 2026)
- **Default to Notes:** All personal reflections default to `category: "[[Notes]]"`.
- **No Proactive Promotions:** Never automatically or proactively migrate notes to `Thoughts` or `Beliefs` without explicit user request.
- **Naming on Reversion:** If demoted, append the 14-digit creation ID suffix back to the filename on disk.

---

## 3. Decisions Log

Records individual or team decisions, trade-offs, and design architectures.

- **Category:** `category: "[[Decisions]]"`
- **Drafting Location:** Always create brand new decisions in `/Inbox/` for review.
- **No Pipe Tables:** Represent trade-offs or lists using clean bulleted structures instead of markdown pipe tables.
- **Accurate Attribution:** Always attribute the decision clearly to the actual decision-maker. Do not assume Justin made a choice unless he explicitly did.

### Note Layout
```markdown
---
id: "YYYYMMDDHHmmss"
daily_note: "[[YYYY-MM-DD Weekday|YYYY-MM-DD Weekday]]"
category: "[[Decisions]]"
---

## Decision: Spaced Capitalized Topic Name

[Concise narrative of the decision (1-2 short paragraphs) covering:]
- What was the status quo before the decision.
- What changed our minds and why (attributing accurately).
- What might cause us to change our minds later (if applicable).

## Related
- [[Link to relevant note or log]]
```

---

## 4. Projects & Travel Hubs

Coordinates central hubs for work initiatives, family milestones, or travel plans.

- **Category:** `category: "[[Projects]]"`
- **Directory:** `/Notes/Projects/`
- **Filename:** `Title.md` (No ID suffix).
- **Casing & Sync Alignment:** Match project names exactly with external trackers (like Todoist). Capitalize proper nouns and acronyms (e.g., `ADHD Treatment 2026`, `AI Agents 2026 H1`), but keep general words lowercase/sentence-case (e.g., `Ascend membership`, `B2C expansion strategy`).

### Project Note Layout
```markdown
---
id: "YYYYMMDDHHmmss"
daily_note: "[[YYYY-MM-DD Weekday|YYYY-MM-DD Weekday]]"
category: "[[Projects]]"
status: Active
---

# Project Name

> Concise, high-quality 2-3 sentence summary of the project's purpose, scope, or strategic value. Do not prefix with "Executive summary:".

## State
- **Timeline:** Expected Start/End dates
- **People Involved:** [[Person Name]], [[Another Person]]

---

## 🎯 Objectives & Milestones
- List of core goals or trip milestones.

## 🗒 Task List
- [ ] Direct, actionable task
- [ ] Another task

## 🔗 Related Notes & Resources
- [[Related Note 1]]
```
