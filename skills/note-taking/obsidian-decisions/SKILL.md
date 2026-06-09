---
name: obsidian-decisions
description: Use when creating or recording team or individual decisions, trade-offs, and reasoning logs under Notes/ with category "[[Decisions]]".
version: 1.0.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [obsidian, notes, decisions, architecture, product]
    related_skills: [obsidian, obsidian-notes]
---

# Obsidian: Decisions Log Management

## Overview
This skill governs the capture and structured recording of individual or team decisions. These files act as historical records of tradeoffs, constraints, and reasoning.

---

## Folder & Category
- **Directory:** `/home/justin.guest/vault/Notes/`
- **Category link:** `category: "[[Decisions]]"`

---

## Note Layout & Structure
A Decision Note is formatted to clearly outline the problem context, proposed options, and the reasoning for the final choice.

```markdown
---
id: 'YYYYMMDDHHmmss'
daily_note: "[[Daily Notes/YYYY-MM-DD Weekday|YYYY-MM-DD Weekday]]"
category: "[[Decisions]]"
---

# Decision: Spaced Capitalized Topic Name

- **Date:** YYYY-MM-DD
- **Decision Maker:** [[Person Who Made Call]] (e.g. [[Justin Goff]], or a colleague)
- **Status:** Proposed/Approved/Superceded

---

## Context & Problem
What is the problem being addressed? Why is it a problem now?

## Options Considered
Detailed overview of options.

### Option 1: Description
- **Pros:** 
- **Cons:** 

### Option 2: Description
- **Pros:** 
- **Cons:** 

---

## Decision & Reasoning
Which option was chosen and why? 

> Highlight any trade-offs accepted or constraints discovered.
```

---

## Core Rules
- **Accurate Attribution:** Always attribute the decision to the actual decision-maker. Do not assume or state Justin made a decision unless he explicitly did.
- **Capitalized spaced names:** Use `ID Title.md` format for the filename (where ID is the creation timestamp, e.g. `20260609120000 Decision to shift to free to play.md`).
- **No Pipe Tables:** Avoid using markdown pipe tables; represent trade-offs using clean bulleted list structures.
