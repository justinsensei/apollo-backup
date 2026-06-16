---
name: obsidian-vault-jam
description: "Master interactive vault-gardening and jam sessions: guides entity enrichment, suggesting new notes, surfacing connections, and promoting files."
version: 1.1.0
author: Bes
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [obsidian, vault-jam, interactive, notes, suggest-links, suggest-notes, promotions, gardening]
    related_skills: [obsidian, obsidian-notes, obsidian-logs, obsidian-contacts]
---

# Obsidian: Vault Jam & Gardening Session

A **Vault Jam** is an interactive, collaborative session to perform intensive maintenance, gardening, and creative connection-building inside Justin's vault.

---

## 1. The Interactive Work Loop

When a Vault Jam is initiated, follow these phases sequentially:
- **Batching Rule:** For Phases 2, 3, and 4, always present exactly **5 suggestions** at a time. After presenting and processing approvals, ask Justin if he wants to see another batch of 5 or advance to the next phase.
- **Seeding Rule:** If Justin specifies a topic (e.g., "Let's do a vault jam around *special ed strategy*"), **seed every phase with that topic** using the seeding flags.

---

## 2. Phase 1 — Graph & Entity Enrichment

Clean layouts, repair broken links, and update metadata on incoming discussion logs.

1. **Vault Hygiene:** Run `python3 ~/.hermes/scripts/vault_hygiene.py`. Present a summary of any unresolved layout issues, duplicates, or broken links, and proactively resolve simple fixes.
2. **Review Slack Logs:** Scan recent Slack logs (`Logs/Slack/*.md`) created since the last run. For each new log:
   - Synthesize a brief, **2-3 sentence Topic Description** inside the file body.
   - Compile participants in the frontmatter `participants` list.
   - **Enforce Constraints:** Strip any raw transcripts, bulleted notes, or decisions from the body, keeping only the clean Topic Description pointer.

---

## 3. Phase 2 — Suggest New Notes

Identify conceptual gaps, insights, or missing definitions in recent logs and initialize stubs in `/Inbox/`.

1. **Candidates Discovery:**
   - **Unseeded:** Run `python3 ~/.hermes/skills/note-taking/obsidian-vault-jam/scripts/scan_recent_logs.py --hours 48` to scan the last 48 hours of logs.
   - **Seeded:** Bias your search heavily toward logs and meeting files matching the seed keyword. Search via `search_files(target='content', path='/home/justin.guest/vault/Logs', pattern='[keyword]')`.
2. **Pitch Format:** Present exactly **5 candidate stubs** with their category and 1-2 sentence rationales:
   `1. [[Proposed Title]] (category: "[[Thoughts]]") — Why: [1-2 sentence rationale]`
3. **Stub Creation:** Write approved notes to `/Inbox/` in the format `ID Title.md` with correct YAML frontmatter:
   ```yaml
   ---
   id: "YYYYMMDDHHmmss"
   daily_note: "[[YYYY-MM-DD Weekday|YYYY-MM-DD Weekday]]"
   category: "[[Thoughts]]" # or Concepts, Decisions, Notes
   ---
   ```

---

## 4. Phase 3 — Suggest Links

Surface cross-connections among existing `Thoughts` and `Beliefs` to enrich the knowledge graph.

1. **Link Rules (Hierarchy Constraints):** Suggested links must strictly follow the unidirectional hierarchy:
   - **Thought** $\rightarrow$ **Thought** (Valid)
   - **Thought** $\rightarrow$ **Belief** (Valid)
   - **Belief** $\rightarrow$ **Belief** (Valid)
   - *Never point a Belief to a Thought, or any higher tier to a raw Tier 1 note.*
2. **Candidates Discovery:**
   - **Unseeded:** Run `python3 ~/.hermes/skills/note-taking/obsidian-vault-jam/scripts/suggest_connections.py`
   - **Seeded:** Run `python3 ~/.hermes/skills/note-taking/obsidian-vault-jam/scripts/suggest_connections.py --seed "[topic]"`
3. **Pitch Format:** Present exactly **5 connection candidates**:
   `1. [[Source Note Title]] -> [[Target Note Title]] — Why: [1-2 sentence compelling rationale]`
4. **Writing Links:** Append approved links to the source note under a `## Connections` section:
   ```markdown
   
   ---

   ## Connections
   - [[Target Note Title]] — Why: [1-2 sentence rationale]
   ```

---

## 5. Phase 4 — Suggest Promotions

Evaluate which notes are ready to be promoted up the vault's hierarchical tiers:
1. **Tier 1 (Ephemeral):** `[[Notes]]`, `[[Concepts]]`, `[[Decisions]]`
2. **Tier 2 (Emergent):** `[[Thoughts]]`
3. **Tier 3 (Permanent):** `[[Beliefs]]`

### Execution Steps
1. **Candidates Discovery:** Run `python3 ~/.hermes/skills/note-taking/obsidian-vault-jam/scripts/get_promotion_candidates.py` (add `--seed "[topic]"` if seeded).
2. **Pitch Format:** Select exactly **5 promotions** and present them with context:
   `1. [[Current Note Title]] -> Promote to [[Beliefs]] (or Thoughts) — Reasoning: [Why its content and backlink profile justify promotion].`
3. **Promotion & Transition:**
   - Use `patch` to update `category` in frontmatter.
   - **Adjust Filename:** Rename file on disk to conform to category naming rules (retaining ID for Thoughts, ensuring no ID prefix for Projects, or keeping ID suffix for Beliefs).
   - **Thoughts $\rightarrow$ Beliefs Synthesis:** Synthesize tenets and applications. Append **Core Tenets** (exactly 3, numbered) and **Application** guidelines (exactly 2 scenario bullets) under a horizontal rule divider.
   - **Link Hygiene Check:** Scan outgoing links of the promoted note. If it contains downward links (e.g. Belief linking to a raw meeting note), flag these for Justin or convert them to plain text.
