# integrate-query

Interactive Q&A with durable synthesis — file answers back to the vault.

**Scope:** Interactive sessions only (Telegram, Cursor, Slack DM with Justin). Cron jobs run integrate-light + integrate-entities only — no auto-filing from autonomous runs. No `Utilities/index.md` updates (deferred).

## Think vs Do split

| Trigger | Behavior |
|---------|----------|
| **Do** — Todoist, calendar, email send, task creation | Stay in analysis-over-action; wait for explicit go-ahead |
| **Think** — vault research, synthesis, comparison, decision analysis | Answer **and** file when durability threshold met |

## When to use

Justin asks a research/knowledge question where the answer should persist:
- "What do my notes say about X?"
- "Synthesize everything on Y"
- "Compare these two Sources"
- "Compare X and Y across my notes"

**Don't use for:** lookup-only questions (see Skip filing below).

## Durability threshold — file when ANY of:

- Synthesis draws on **3+ vault notes** (Inputs, Sources, Concepts, Projects, Contacts)
- Comparison or decision analysis across sources
- Cross-project or cross-contact connection Justin is likely to revisit
- Justin says "file this", "save to vault", "remember this synthesis"
- Same topic asked twice (file or update synthesis note; link it on the second occurrence)

## Skip filing when:

- Lookup-only ("what's the path to X?", "did I already do Y?" → use `did-i-already-do-this`)
- Ephemeral / tactical answer with no cross-note synthesis
- Answer already exists as a dedicated vault note (link to it instead)
- Justin explicitly says not to file

## Workflow

1. **Search** — `semantic_pointer.py search` + vault grep for relevant Inputs/Sources/Concepts/Projects/Contacts
2. **Synthesize** — compose answer citing upstream links (Concept→Source→Reading)
3. **Create or update** — see below
4. **Post-file** — log append, optional entity integration, chat one-liner

## Create vs update

- **Search first** for existing note on same topic (title grep + semantic search)
- If match: **append** `## YYYY-MM-DD update` section rather than duplicate
- If no match: create new note from [query-synthesis template](../templates/query-synthesis.md)

## Category routing

| Answer type | Category | Folder | Default? |
|-------------|----------|--------|----------|
| Personal synthesis / take | `[[Thoughts]]` | `Notes/` | **Default** for personal synthesis |
| Others' model extracted | `[[Concepts]]` | `Notes/` | External model extracted from sources |
| Fleeting answer / working scratch | `[[Notes]]` | `Notes/` | Working scratch only |
| Trusted principle | `[[Beliefs]]` | `Notes/` | **Confirm before filing** |
| Decision record | `[[Decisions]]` | `Notes/` | **Confirm before filing** |

**Confirm before filing** → `[[Beliefs]]`, `[[Decisions]]` (high-tier; one-line ask in chat).

## Note body structure

Use [query-synthesis template](../templates/query-synthesis.md). Required sections:

- `# Title` — question reframed as topic
- `## Question` — what Justin asked
- `## Synthesis` — the durable answer with wikilinks
- `## Sources consulted` — bullet list of upstream notes (Concept→Source→Reading rule)
- `## Related` — Projects/Contacts if relevant

## Post-file steps

1. Append `Utilities/log.md` line: `HH:MM | query | [[Title]] | Notes/path.md | [[daily note]]` (integrate-light, `query` token). See [integrate-light.md](integrate-light.md).
2. If synthesis names matched project/contact hubs → run `integrate_entities.py` on the **new note** (optional, same as ingest)
3. Chat closing: one quiet line — `→ filed [[Title]]` (Bes voice: minimal)

## Link rules

- Link to Sources when they exist; never skip Source to link Reading directly from Concepts
- Use shortest-path wikilinks per obsidian skill

## Frontmatter

Standard obsidian schema with `id`, `daily_note`, `category`. Timestamp-prefixed filename for Notes/Thoughts/Concepts; title-only for Beliefs/References-style if canonical.
