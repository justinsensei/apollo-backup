---
name: apollo-compile-inputs
description: Run vault compile-inputs — Phase 0 apply Ready to Apply, then phased Readings/Sources/Meetings/Others.
---

# Apollo Compile Inputs

## When

Cron tick or Justin asks to drain the compile queue.

## Steps

1. Ensure vault is accessible.
2. Read and follow exactly:
   `/home/justin.guest/Developer/obsidian-vault/.cursor/skills/compile-inputs/SKILL.md`
3. Also load if needed:
   - `.cursor/skills/apply-proposal/SKILL.md`
   - `.cursor/skills/extract-source/SKILL.md`
   - `.cursor/skills/draft-notebook-proposal/SKILL.md`
   - `.cursor/rules/agent-routing.mdc`
   - `.cursor/rules/note-creation.mdc`
4. **Note Voice & Prose Standards:** All keepable note bodies, draft proposals, document notes, and work logs MUST use complete sentences. Telegraphic fragments and shorthand bullets are prohibited. Headings and bullet headings may be bolded labels (`**Stage 1 (Static):** …`), but full sentences must follow.
5. Run the **full phased tick** (not “one action then stop”):
   - Phase 0: batch-apply **all** `Proposal - *.md` in `Inbox/Ready to Apply/` (one at a time; empty folder = no-op, continue)
   - Phase 1: extract **all** unprocessed Readings (newest first) → Sources in `Inputs/Sources/` (never Inbox)
   - Phase 2: ≤1 Source → Proposal (newest) if any
   - Phase 3: **all** pending Meetings → one Proposal each
   - Phase 4: if any pending Others → **one** theme-clustered digest Proposal covering all of them
5. Sync is managed by Obsidian Sync. Do not run git commit or push automatically (Git is reserved for manual safety commits before major changes).
6. Do **not** promote Thoughts/Beliefs/Decisions into Notebook. Apply only via `apply-proposal` rules (drafts → `Inbox/Notes/`; Proposals → `Utilities/Review/`). Never move files *into* Ready to Apply.
7. Delivery: Telegram summary when any file was written (include counts: Proposals applied, Sources extracted, Reading Proposals, Meeting Proposals, digest Inputs; list Inbox triage paths from Phase 0); use `[SILENT]` on no-op.

## Flows reminder

- Phase 0: Ready to Apply → Inbox/Notes drafts + archive Proposal (Justin gated by folder move)
- Flow A: Reading → Source (`Inputs/Sources/`) → Proposal (never Reading → Proposal; ≤1 Proposal per tick; extract all Readings)
- Flow B1: Meeting → Proposal (1:1; all pending in one tick)
- Flow B2: Others → one Inputs digest Proposal (theme-clustered)

## Pitfalls & Backlog Safety

- **Transcript Chunk Flooding**: `Inputs/Meetings/` can contain dozens of fragmented transcript chunks (e.g., files ending with `-1.md`, `-2.md`, etc.). Always ignore/skip these chunk files; only compile proposals from the primary/full non-chunk meeting files.
- **Massive Meeting Backlog**: If there is a large historical backlog of pending meetings (e.g., hundreds of unprocessed files), attempting to process "all pending" in a single tick will exceed token limits or timeout. In such cases, process only the most recent **2-3 full meetings** per tick, and work with the user to archive or batch-mark the old files with a `notebook_proposal:` marker to safely clear the backlog.

