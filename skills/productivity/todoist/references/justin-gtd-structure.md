# Justin's GTD Structure in Todoist

Established 2026-05-20. May evolve — check this file before restructuring anything.

## Projects (areas of focus)

| Project | Color | Purpose |
|---|---|---|
| Work | Blue | All work next actions and projects |
| Personal | Green | Personal admin, health, family, finances |
| #Hermes (sub of Work) | — | Hermes Agent infra/setup tasks — actioned BY Hermes agent, not Justin |

## Sections (in each Project)

- **Someday Maybe** — items Justin is not committing to yet. Convention: anything dropped here also gets the `@someday` label (see below).
- Unsectioned area = active next actions.

## Labels

| Label | Color | Meaning |
|---|---|---|
| `@waiting` | Orange | Delegated or blocked — watching, not acting |
| `@someday` | Grey | In Someday Maybe section — not a current commitment |

**Why `@someday` exists:** Todoist filter syntax cannot exclude tasks by section. Without this label, "Next Actions" filters would surface Someday Maybe items. The label is the workaround — small discipline, big payoff. Apply it to every task dropped into a Someday Maybe section.

## Filters

| Filter | Query | Purpose |
|---|---|---|
| Next Actions — Work | `#Work & !@waiting & !@someday` | Work next actions only |
| Next Actions — Personal | `#Personal & !@waiting & !@someday` | Personal next actions only |
| Waiting For | `@waiting` | Cross-area delegated/blocked items |

## Inbox

Default Todoist inbox. No special conventions yet — Justin processes it manually. Items captured by Bes land here unless explicitly routed.

## Key design decisions (rationale)

- **Projects = areas of focus**, not GTD projects. GTD projects (multi-step work) live as tasks with subtasks inside Work or Personal.
- **No Home project** — Justin uses Work and Personal only for now.
- **No References project** — not using Todoist for reference material (that's Obsidian).
- **Someday Maybe as sections, not separate Projects** — keeps the Someday Maybe items contextualized by area of focus (Work vs Personal).
- **@waiting as label, not Project** — cross-area by nature; a filter is the right view.
