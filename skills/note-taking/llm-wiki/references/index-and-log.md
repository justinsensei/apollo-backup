# Utilities Log

Paths relative to `$OBSIDIAN_VAULT_PATH` (vault root). Owned by **llm-wiki** (`integrate-light`, `integrate-full`, `integrate-query`).

## Utilities/log.md

Append-only ingest audit trail. No YAML frontmatter — `vault_hygiene.py` skips `Utilities/`.

### Line format

```markdown
# Wiki Log

Append-only record of ingests, compiles, and filed queries. Do not edit prior lines.

## YYYY-MM-DD

- HH:MM | slack | [[YYYY-MM-DD - Title]] | inbox/foo.md | [[2026-06-10 Tuesday]]
- HH:MM | email | [[YYYY-MM-DD - Subject]] | Inputs/Emails/foo.md | [[2026-06-10 Tuesday]]
- HH:MM | reading | [[Reading Title]] | Inputs/Readings/foo.md | [[2026-06-10 Tuesday]]
- HH:MM | meeting | [[YYYY-MM-DD - Title]] | Inputs/Meetings/foo.md | [[2026-06-10 Tuesday]]
- HH:MM | query | [[Synthesis Title]] | Notes/foo.md | [[2026-06-10 Tuesday]]
- HH:MM | source-compile | [[Source Title]] | Notes/Title.md | [[2026-06-10 Tuesday]]
```

Fields: `time | type | wikilink-to-note | vault-relative-path | wikilink-to-daily-note`

No historical backfill — start empty (header only) when first created.

### Bootstrap on VM

After commit + `bes-pull`, create `Utilities/log.md` from `skills/note-taking/llm-wiki/templates/log.md` if it does not exist. Justin must do this once on the VM vault before the first integrate-light append.

## integrate-light updates

- **log.md:** one line per ingest, with daily note wikilink as last field
- No index.md maintenance
- No daily notepad bullet from integrate-light

## integrate-full updates

- Log `source-compile` lines in log.md when Sources are created or refreshed
- No index.md maintenance

## Lint log entries

Tier-3 monthly passes append a `lint` line (see [lint.md](lint.md)). Full reports live in `Utilities/reports/semantic-lint-YYYY-MM-DD.md`.

## Deferred: Utilities/index.md

A human browse catalog (`index.md`) is **not** maintained. Agents use `semantic_pointer.py`, folder taxonomy, and frontmatter instead.
