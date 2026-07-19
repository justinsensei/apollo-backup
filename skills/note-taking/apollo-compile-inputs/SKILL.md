---
name: apollo-compile-inputs
description: Run vault compile-inputs — phased tick (all Readings→Sources, Source/Meetings/Others Proposals).
---

# Apollo Compile Inputs

## When

Cron tick or Justin asks to drain the compile queue.

## Steps

1. Ensure vault is current (pre-turn pull / apollo-vault-sync).
2. Read and follow exactly:
   `/home/justin.guest/Developer/obsidian-vault/.cursor/skills/compile-inputs/SKILL.md`
3. Also load if needed:
   - `.cursor/skills/extract-source/SKILL.md`
   - `.cursor/skills/draft-notebook-proposal/SKILL.md`
   - `.cursor/rules/agent-routing.mdc`
4. Run the **full phased tick** (not “one action then stop”):
   - Phase 1: extract **all** unprocessed Readings (newest first) → Sources in `Inputs/Sources/` with `status: "final"` (never Inbox)
   - Phase 2: ≤1 Source → Proposal (newest) if any
   - Phase 3: **all** pending Meetings → one Proposal each
   - Phase 4: if any pending Others → **one** theme-clustered digest Proposal covering all of them
5. Do **not** `git commit` — `apollo-vault-sync` owns commits.
6. Do **not** edit `Notebook/` or apply Proposals.
7. Delivery: Telegram summary when any file was written (include counts: Sources extracted, Reading Proposals, Meeting Proposals, digest Inputs); use `[SILENT]` on no-op.

## Flows reminder

- Flow A: Reading → Source (`Inputs/Sources/`) → Proposal (never Reading → Proposal; ≤1 Proposal per tick; extract all Readings)
- Flow B1: Meeting → Proposal (1:1; all pending in one tick)
- Flow B2: Others → one Inputs digest Proposal (theme-clustered)
