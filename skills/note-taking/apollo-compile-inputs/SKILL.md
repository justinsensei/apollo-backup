---
name: apollo-compile-inputs
description: Run vault compile-inputs — one Inputs→Inbox action per tick (Reading→Source or Input→Proposal).
version: 1.0.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [note-taking, obsidian, compile, inputs]
    related_skills: [obsidian, apollo-brain-ingest]
---

# Apollo Compile Inputs

## Overview
Automated compilation of raw inputs into structured vault drafts (Sources and Proposals) in the Inbox.

## When to Use
- Run during Cron ticks.
- Run when Justin asks to compile or drain the input queues.

## Steps
1. Ensure vault is current (pre-turn pull / apollo-vault-sync).
2. Read and follow exactly:
   `/home/justin.guest/Developer/obsidian-vault/.cursor/skills/compile-inputs/SKILL.md`
3. Also load if needed:
   - `.cursor/skills/extract-source/SKILL.md`
   - `.cursor/skills/draft-notebook-proposal/SKILL.md`
   - `.cursor/rules/agent-routing.mdc`
4. Execute **one** action, then stop.
5. Do **not** `git commit` — `apollo-vault-sync` owns commits.
6. Do **not** edit `Notebook/` or apply Proposals.
7. Delivery: Telegram summary only when a file was written; use `[SILENT]` on no-op.

## Flows Reminder
- Flow A: Reading → Source → Proposal (never Reading → Proposal)
- Flow B: Non-Reading Input → Proposal

## Common Pitfalls
- **Accidentally running multiple steps:** Always process exactly one action (one Reading to Source, or one Source to Proposal, or one non-Reading Input to Proposal) per tick.
- **Git Commits:** Do not run `git commit`. The `apollo-vault-sync` process manages the git tracking.

## Verification Checklist
- [ ] Vault has been updated prior to execution.
- [ ] Correct flow (A1, A2, or B) has been identified and executed.
- [ ] Exactly one action has been performed.
- [ ] No changes have been committed to git by this tool.
- [ ] Telegram notification is only sent if a file was written; otherwise silent.
