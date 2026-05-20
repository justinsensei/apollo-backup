---
name: work-log
description: Use when Justin asks to "create a work log", "log today's work", "write a work log", or otherwise wants today's work activity summarized and appended to today's daily note in the Obsidian vault. Vault-only version — synthesizes from the daily note plus chat input; does not pull from external integrations.
platforms: [linux, macos]
---

# Work Log

Summarize today's work activity and append a structured Work Log block to **today's daily note** in the Obsidian vault. Do NOT create a separate file.

This is the vault-only shape of the skill — there are no Slack / Gmail / Calendar / Linear / git integrations wired up yet. Synthesize from whatever Justin wrote into the daily note during the day, plus whatever he brain-dumps in chat. When integrations get wired up later, patch this skill to add them as additional gather sources.

## Step 1 — Resolve vault path

Read `OBSIDIAN_VAULT_PATH` from env (typically `/home/justin.guest/vault` inside `bes-vm`). Do not hard-code. If unset, fall back to `~/Documents/Obsidian Vault`. See the `obsidian` skill for full path-handling conventions.

## Step 2 — Find today's daily note

Daily-note filename format: `YYYY-MM-DD DayName.md` (e.g. `2026-05-20 Wednesday.md`).

Justin's vault convention: **current** daily notes live in the vault root; **archived** daily notes live in `Daily Notes/`. Check the root first:

1. `<vault>/<YYYY-MM-DD DayName>.md` — primary
2. `<vault>/Daily Notes/<YYYY-MM-DD DayName>.md` — fallback (rare; means today's note already got archived, which is unusual mid-day)

Use `search_files` with `target: "files"` to locate. If neither exists, tell Justin "Today's daily note doesn't exist yet — create it first." and stop.

## Step 3 — Gather raw material

Two sources, both lightweight:

1. **Read today's daily note** with `read_file`. Scan for anything that looks like work activity — decisions, things he completed, things he started, links to other notes, meeting notes, blockers he mentioned.
2. **Ask Justin in chat** what else he worked on that isn't already in the note. Keep the prompt short: *"Anything you worked on today that isn't already in the daily note? Decisions, blockers, conversations, side-quests — anything."* If he says "nothing" or "that's all," move on.

Do not invent or pad. If the raw material is thin, the Work Log will be thin. That's correct — fabricating activity would be worse than a short log.

## Step 4 — Synthesize three sections

Produce a Work Log block with three section headings. Omit any section that has no real content (don't include an empty heading).

### `### Today's Highlights`
The most important things that happened — shipped work, key conversations, decisions reached, code written, problems solved. Be specific: name the people, projects, and outcomes. Past tense. 4–8 bullets typically; fewer is fine if it was a quiet day.

### `### Decisions Made`
Consequential decisions only. For each, bold the decision itself; include owner if not obvious. Skip if no real decisions were made — don't promote tasks or observations into "decisions."

### `### Open Questions / Blockers`
Unresolved questions, pending actions, known blockers as of end-of-day. Skip if none.

Writing style: concise, specific, past tense for highlights. Match the voice of prior work logs if Justin has any (grep for `## 💼 Work Log` in the daily-notes archive to find examples).

## Step 5 — Append to the daily note

Use `patch` (anchored append) or `write_file` (whole-note rewrite). Append this block at the **end** of the note, preserving everything above:

```
## 💼 Work Log

### Today's Highlights
[bullets]

### Decisions Made
[bullets]

### Open Questions / Blockers
[bullets]

---
*Sources: daily note + chat input.*
```

When integrations are wired up, the `*Sources:* …` line should reflect the real sources used and their counts (e.g. `"Slack (12 messages across #product-leads, DMs) | Linear (5 issues)"`). For now, keep it accurate to vault-only.

Do NOT add a separate frontmatter block. Do NOT modify anything else in the file.

## Step 6 — Don't commit

Justin's `bes-vault-sync` watcher auto-commits and pushes the vault to `obsidian-vault` on GitHub within seconds of any write. Do NOT manually `git add` or `git commit` — it races the watcher and creates spurious commits.

## Important behaviors

- **No duplicate Work Log blocks.** If the daily note already contains `## 💼 Work Log`, ask Justin: replace, update, or skip? Don't append a second one silently.
- **Omit empty sections.** A Work Log with only Highlights is better than one with empty "Decisions Made" / "Open Questions" headings.
- **No file creation.** The only write operation is appending to the existing daily note.
- **Skip cleanup of the daily note.** Don't reformat or tidy what Justin already wrote — the Work Log block is additive.

## Future: when integrations come online

When Notion / Linear / Slack / Gmail / Calendar / git access lands, patch this skill to add a new gather step between the daily-note read and the chat prompt. Pattern:

1. Per-source gather in parallel, filtered to today's date.
2. Discard personal / irrelevant content per source.
3. Update the `*Sources:* …` footer to enumerate the real sources and counts.

Don't ship integration-dependent code until the integration is actually wired — half-wired branches that "skip if missing" age badly. When the time comes, write the gather step against the real tool, then patch this SKILL.md.
