# Semantic Lint (tier-3)

Structural checks belong to `obsidian-hygiene` / `vault_hygiene.py`. This reference covers **tier-3 semantic health** — report-only, never auto-edits.

## Schedule

| Pass | When | How |
|------|------|-----|
| **Monthly (cron)** | 1st of month, 8:00 AM | `wiki_semantic_lint_cron.py` → Telegram if issues |
| **On-demand** | "run wiki lint", wind-down after integrate-full | Agent reads report + deep contradiction review |

Cron job id: `a3f8c2e91b04`. State: `~/.hermes/state/semantic_lint_last.json`. Vault report: `Utilities/reports/semantic-lint-YYYY-MM-DD.md`.

## Trigger phrases

- "run wiki lint"
- "check for contradictions"
- "are my Sources stale?"
- "tier-3 lint" / "semantic lint"

## Automated checks (`wiki_semantic_lint.py`)

Run structural baseline first:

```bash
python3 ~/.hermes/scripts/vault_hygiene.py
python3 ~/.hermes/scripts/wiki_semantic_lint.py
```

| Check | What it finds |
|-------|----------------|
| **Maturity orphans** | `Notes/` pages (Thoughts, Concepts, Beliefs, Sources, etc.) with zero inbound links |
| **Stale summaries** | Source `## Summary` older than linked Reading mtime |
| **Promotion opportunities** | Substantial Readings with no compiled Source |
| **Missing link chains** | Concept/Belief/Thought links directly to Reading when Source exists |
| **Contradiction candidates** | Belief/Thought shares wikilinks with Decision/Meeting/Slack from last 30 days — **review only** |

Scopes recent activity using `Utilities/log.md` entries since the last lint run.

### JSON / cron

```bash
python3 ~/.hermes/scripts/wiki_semantic_lint.py --json   # machine output + state file
python3 ~/.hermes/scripts/wiki_semantic_lint_cron.py      # monthly Telegram wrapper
```

Appends one line to `Utilities/log.md`:

```markdown
- 08:00 | lint | [[semantic-lint-YYYY-MM-DD]] | Utilities/reports/semantic-lint-YYYY-MM-DD.md | tier-3 (N issues)
```

## Agent pass (on-demand contradictions)

After the script baseline, the agent reviews **contradiction candidates** and any Belief/Thought vs newer Decision/Meeting pairs surfaced in the monthly report:

1. Read `Utilities/reports/semantic-lint-*.md` (latest) + recent `log.md`
2. For each candidate pair, read both notes — flag genuine contradictions vs harmless overlap
3. Append refined findings to the report or present in wind-down / morning briefing
4. **Never auto-edit Beliefs** — surface for Justin

### Stale / promotion resolution

- Stale summaries → `integrate-full` refresh for scoped Sources
- Promotion opportunities → offer Source note creation (integrate-full template)
- Missing link chains → relink Concept through Source, not Reading
- Maturity orphans → propose backlinks to project hubs or daily notes

## Output format

```markdown
## Wiki semantic lint — YYYY-MM-DD

### Maturity orphans (no inbound links)
- `Notes/Some Concept.md` (Concepts)

### Stale summaries
- [[Source Title]]: reading updated 2026-05-28, summary 2026-05-01

### Promotion opportunities
- [[Reading Title]]: no compiled Source yet

### Missing link chains
- `Notes/Concept X.md` → Reading `Inputs/Readings/foo.md` (Source: `Notes/foo.md`)

### Contradiction review candidates
- `Notes/Belief A.md` vs `inbox/2026-06-01 - Decision - Foo.md` — shared: k12 gtm
```

## Surfacing

- **Morning briefing Phase 1:** read `semantic_lint_last.json`; if `surfaced: false` and `tier3_issues` non-empty, append wiki lint block (same style as tier-2 hygiene). Set `surfaced: true` after presenting.
- **Wind-down Phase 4:** if monthly report is <7 days old, mention count in EIIRP summary before integrate-full.

## Delegation

| Owner | Checks |
|-------|--------|
| `vault_hygiene.py` | ID, folders, ghosts, structural orphans (zero in+out) |
| `wiki_semantic_lint.py` | Tier-3 semantic (this doc) |
| Agent + integrate-full | Contradiction adjudication, Source refresh, hub linking |
