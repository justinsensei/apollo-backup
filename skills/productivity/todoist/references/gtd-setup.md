# Justin's GTD Setup in Todoist

Established: 2026-05-20. Designed in conversation with Bes.

## Design decisions

### Projects = areas of focus
Todoist Projects are areas of focus, not GTD projects. GTD projects (anything requiring 2+ actions) are tasks with subtasks inside each area.

### Active Projects
| Project | Color | Notes |
|---|---|---|
| Work | Blue | Professional work, SignLab |
| Personal | Green | Personal admin, life, family |
| Hermes (sub of Work) | — | Hermes Agent infra/setup; actioned by Hermes agent |

### Someday Maybe — sections, not Projects
Each Project has a "Someday Maybe" section. Rationale: keeps Someday Maybe items contextualized by area of focus. Items in these sections MUST get the `@someday` label (required because Todoist filters can't filter by section — the label is what makes the Next Actions filters work).

### Labels
| Label | Color | Meaning |
|---|---|---|
| @waiting | Orange | Delegated or blocked; you're waiting on someone/something |
| @someday | Grey | In a Someday Maybe section; excluded from Next Actions views |

### Filters
| Filter | Query | Color |
|---|---|---|
| Next Actions — Work | `#Work & !@waiting & !@someday` | Blue |
| Next Actions — Personal | `#Personal & !@waiting & !@someday` | Green |
| Waiting For | `@waiting` | Orange |

### Inbox
Default Todoist inbox. No special conventions yet. Process regularly (GTD weekly review TBD).

## Key conventions
- Drop tasks into Inbox first; process manually into Work or Personal.
- Anything going into a Someday Maybe section → always add `@someday`.
- Anything delegated or blocked → always add `@waiting`.
- Do NOT create Todoist Projects for individual GTD projects — use tasks+subtasks inside Work or Personal.

## What was deliberately excluded
- **References** — not implemented (Justin doesn't need them in Todoist).
- **Home** as a Project — considered, dropped. Personal covers it.
- Separate Someday Maybe Projects — rejected in favor of sections (preserves area context).
- Waiting For as a Project — rejected in favor of `@waiting` label + filter (cross-area view without extra sidebar noise).
