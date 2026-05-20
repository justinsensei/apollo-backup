# Justin's GTD Structure in Todoist

Last updated: 2026-05-20

## Philosophy

Lightweight GTD. Whole-life (work + personal). Main pain: doesn't trust the system; too much in his head; stuff falls through cracks.

No references list. Inbox is Todoist's default inbox — no special conventions yet (process manually).

## Projects (areas of focus)

| Project | Color | Notes |
|---------|-------|-------|
| Work | Blue | Work area of focus |
| Personal | Green | Personal + family + personal admin |
| Hermes *(sub-project of Work)* | — | Hermes Agent infra tasks. Actioned BY the Hermes infra agent, not Justin. |

**Rule:** Justin organizes manually. Don't restructure Projects without asking.

## Sections (inside each Project)

Each Project has one section:

- **Someday Maybe** — things not committed to yet but worth keeping

**Critical:** Todoist filters cannot filter by section. Items placed in Someday Maybe MUST also get the `@someday` label or they'll appear in Next Actions views.

## Labels

| Label | Color | Meaning |
|-------|-------|---------|
| `@waiting` | Orange | Delegated or blocked — tracking, not acting |
| `@someday` | Grey | In a Someday Maybe section — excluded from Next Actions |
| `@project` | Violet | Parent task of a multi-step GTD project |

**Convention:** GTD "projects" (anything requiring 2+ steps) are modeled as a parent task (labeled `@project`) with subtasks, NOT as separate Todoist Projects.

**Section + label pairing:** Every item added to a Someday Maybe section must get `@someday`. Every item that is delegated/blocked must get `@waiting`. Apply manually at capture time.

## Filters

| Filter | Query | Color |
|--------|-------|-------|
| Next Actions — Work | `#Work & !@waiting & !@someday` | Blue |
| Next Actions — Personal | `#Personal & !@waiting & !@someday` | Green |
| Waiting For — Work | `#Work & @waiting` | Orange |
| Waiting For — Personal | `#Personal & @waiting` | Green |

These are already live. Don't recreate or rename without asking.

## Design decisions and rationale

- **Someday Maybe as section (not Project):** keeps items contextualized by area of focus (Work vs Personal). Requires `@someday` label as workaround for Todoist's lack of section-based filtering.
- **Waiting For as label + filter (not Project):** cross-area visibility without extra sidebar clutter. Filtered per-area via Work/Personal filter pair.
- **GTD projects as subtasks (not Projects):** Justin carries dozens of active projects; separate Todoist Projects per project would make the sidebar unwieldy. Parent task + `@project` label scales better.
- **No Home Project:** Justin simplified to just Work and Personal.
- **Naming:** "Someday Maybe" (no slash).
