---
name: apollo-compile-inputs
description: Run vault compile-inputs — Phase 0 apply Ready to Apply, then phased Readings/Sources/Meetings/Others.
---

# Apollo Compile Inputs

## When

Cron tick or Justin asks to drain the compile queue.

## Steps

1. Ensure vault is current (pre-turn pull / apollo-vault-sync).
2. Read and follow exactly:
   `/home/justin.guest/Developer/obsidian-vault/.cursor/skills/compile-inputs/SKILL.md`
3. Also load if needed:
   - `.cursor/skills/apply-proposal/SKILL.md`
   - `.cursor/skills/extract-source/SKILL.md`
   - `.cursor/skills/draft-notebook-proposal/SKILL.md`
   - `.cursor/rules/agent-routing.mdc`
4. Run the **full phased tick** (not “one action then stop”):
   - Phase 0: batch-apply **all** `Proposal - *.md` in `Inbox/Ready to Apply/` (one at a time; empty folder = no-op, continue)
   - Phase 1: extract **all** unprocessed Readings (newest first) → Sources in `Inputs/Sources/` (never Inbox)
   - Phase 2: ≤1 Source → Proposal (newest) if any
   - Phase 3: **all** pending Meetings → one Proposal each
   - Phase 4: if any pending Others → **one** theme-clustered digest Proposal covering all of them
5. Do **not** `git commit` — `apollo-vault-sync` owns commits.
6. Do **not** promote Thoughts/Beliefs/Decisions into Notebook. Apply only via `apply-proposal` rules (drafts → `Inbox/Notes/`; Proposals → `Utilities/Review/`). Never move files *into* Ready to Apply.
7. Delivery: Telegram summary when any file was written (include counts: Proposals applied, Sources extracted, Reading Proposals, Meeting Proposals, digest Inputs; list Inbox triage paths from Phase 0); use `[SILENT]` on no-op.

## Flows reminder

- Phase 0: Ready to Apply → Inbox/Notes drafts + archive Proposal (Justin gated by folder move)
- Flow A: Reading → Source (`Inputs/Sources/`) → Proposal (never Reading → Proposal; ≤1 Proposal per tick; extract all Readings)
- Flow B1: Meeting → Proposal (1:1; all pending in one tick)
- Flow B2: Others → one Inputs digest Proposal (theme-clustered)
