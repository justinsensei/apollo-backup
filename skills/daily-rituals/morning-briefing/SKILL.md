---
name: morning-briefing
description: Use when generating or managing Justin's daily morning briefing report. This is a thin pointer skill that directs Bes to load and apply the canonical morning briefing conventions and formatting rules maintained in the vault.
version: 3.0.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [briefing, morning, report, thin-pointer]
    related_skills: [obsidian, work-log, todoist]
---

# 🌅 Morning Briefing Pointer

## Overview
Bes is a **thin assistant** whose Obsidian-specific conventions are stored and maintained directly inside the Obsidian vault.

The canonical rules, formats, and step-by-step logic for the Morning Briefing are located in:
`/home/justin.guest/Developer/obsidian-vault/.cursor/skills/morning-briefing/SKILL.md`

## When to Use
* **Scheduled Cron Run:** Executed daily at 5:00 AM.
* **Manual Request:** Used when asked for the briefing.

## Instructions
1. **Load Canonical Skill:** Read the live, canonical skill file:
   `/home/justin.guest/Developer/obsidian-vault/.cursor/skills/morning-briefing/SKILL.md`
2. **Execute Workflow:** Follow the exact layout formatting, data collection, and file-writing steps defined in that file.
