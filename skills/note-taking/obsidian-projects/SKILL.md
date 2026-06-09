---
name: obsidian-projects
description: Use when creating or recording active projects, personal or team milestones, trips, or travel plans under Notes/ with category "[[Projects]]".
version: 1.0.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [obsidian, notes, projects, travel, milestones]
    related_skills: [obsidian, obsidian-notes]
---

# Obsidian: Projects & Travel Hubs

## Overview
This skill governs notes that act as central hubs for ongoing work initiatives, travel planning, or personal family milestones.

---

## Folder & Category
- **Directory:** `/home/justin.guest/vault/Notes/`
- **Category link:** `category: "[[Projects]]"`

---

## Note Layout & Structure

A Project or Travel note organizes timelines, tasks, objectives, and related sub-notes:

```markdown
---
id: 'YYYYMMDDHHmmss'
daily_note: "[[Daily Notes/YYYY-MM-DD Weekday|YYYY-MM-DD Weekday]]"
category: "[[Projects]]"
---

# Project Name / Travel Destination

> Executive summary or purpose of the project/trip.

## State
- **Status:** Active/On Hold/Planning/Completed
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
- [[Related Note 2]]
```

---

## Naming Rules
- Filename format: `Title.md` (no timestamp prefix).
- Use CAPITALIZED normal-spaced names for project hubs (e.g. `SignLab Free to Play Shift.md`, `Telluride 2026.md`).
- Never prefix with dates/timestamps.
