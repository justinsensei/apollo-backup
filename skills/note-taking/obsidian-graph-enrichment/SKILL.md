---
name: obsidian-graph-enrichment
description: Principles and link hierarchy conventions for maintaining a clean note graph and tracking chronological thinking evolution in Obsidian.
version: 1.0.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [obsidian, link-hierarchy, graph, note-enrichment, thoughts, beliefs]
    related_skills: [obsidian, obsidian-thoughts-beliefs, obsidian-notes]
---

# Obsidian: Graph Enrichment & Link Hierarchy

## Overview
This skill governs the conventions for link directions and relationship structures between different tiers of notes in Justin's Obsidian vault. By enforcing a unidirectional link hierarchy, we keep high-level notes clean and leverage Obsidian's native backlinks to construct effortless, zero-maintenance historical timelines of thinking.

---

## Note Tier Hierarchy
Justin's notes are organized into a hierarchy of permanence and synthesis. Links should flow **from less-permanent notes to more-permanent notes** (pointing upwards in synthesis):

```
+--------------------------------------------+
|  Tier 1 (Raw/Ephemeral Inputs)             |
|  - Notes, Sources, Decisions, Memories     |
+---------------------+----------------------+
                      | (can link to other Tier 1 notes
                      |  or pointing UPWARDS to T2 / T3)
                      v
+--------------------------------------------+
|  Tier 2 (Emergent/Synthesized Thoughts)    |
|  - Thoughts                                |
+---------------------+----------------------+
                      | (can link to other Tier 2 notes
                      |  or pointing UPWARDS to T3)
                      v
+--------------------------------------------+
|  Tier 3 (Permanent/Conviction Beliefs)     |
|  - Beliefs                                 |
+--------------------------------------------+
```

### The Rules of Link Direction

1. **Tier 1 (Notes, Sources, Decisions, Memories):**
   - Can link to **one another** (e.g., a Decision linking to a Source, or a Memory linking to a Note).
   - Can link to **any note below** in the hierarchy (Thoughts and Beliefs).
2. **Tier 2 (Thoughts):**
   - Can link to **one another** (e.g., a Thought linking to another Thought).
   - Can link to **Beliefs** (Tier 3).
   - *Should NOT link back up to Tier 1 notes.*
3. **Tier 3 (Beliefs):**
   - Can link to **one another** (e.g., a Belief linking to another Belief).
   - *Should NOT link back up to Thoughts or Tier 1 notes.*

---

## Implications & Design Decisions

### 1. Backlinks as the Timeline
Rather than manually updating a high-level Thought or Belief to list all resources, events, or decisions associated with it:
- Link *from* the specific Tier 1 note (e.g., a meeting log or reading clipping) *to* the high-level Thought/Belief.
- Use Obsidian's **Backlinks Pane** on the Thought or Belief note to view the chronological evolution of that idea over time.
- **Timeline Ordering:** No date prefixes or timestamps are required in the filenames of Tier 1 notes (Notes, Sources, Decisions, Memories) to maintain a chronological timeline. Instead, rely entirely on Obsidian's native **Backlinks pane sorting** (e.g., sorting the list by "Created time" or "Modified time") to view the chronological progression of ideas over time. This preserves clean, normal-spaced capitalized titles across the entire vault without sacrificing the temporal view.

### 2. Low-Friction Writing
- It is always easier to link *from* what you are currently writing (the context of today's work or a newly encountered source) *to* a pre-existing stable concept. You do not need to interrupt your flow to edit a long-standing permanent note.

### 3. Clear Separation of Opinions vs. Principles
- **Thoughts** (Category: `[[Thoughts]]`) are emergent, open reflections, research questions, or current opinions.
- **Beliefs** (Category: `[[Beliefs]]`) are highly trusted, semi-permanent frameworks, convictions, or proven mental models.
- Concepts must prove their durability to move from a Thought to a Belief.
