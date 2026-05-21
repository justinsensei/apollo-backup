---
name: manage-projects
description: "Create, update, and close Justin's projects — the cross-tool workflow that spans Todoist (a dedicated sub-Project nested under Work or Home) and Obsidian (a project note with a back-link). Use whenever Justin asks to create a project, add to-dos to a project, or close/complete a project."
version: 2.0.0
tags: [todoist, obsidian, projects, productivity]
related_skills: [todoist, obsidian]
---

# Managing Projects (Todoist + Obsidian)

A "project" (lowercase — GTD sense) maps to:

- **Todoist**: a dedicated **Project** (capital P) nested under the appropriate area (#Work or #Home)
- **Obsidian**: a project note (category `[[Projects]]`) with a `Todoist:` link in the body

Loose tasks (not part of any project) go directly into the Work or Home Project. Projects are for multi-task work that benefits from a dedicated container.

The two are linked **both ways**:
- Obsidian note body: `Todoist: <full project URL>`
- (No back-link needed in Todoist — the Project itself is the container)

## Canonical example: Bes Setup

**Todoist structure:**
```
Work (Project / area)
└── Bes Setup (Project / nested)
    ├── Schedule daily work log runs
    ├── Create a morning planning skill
    ├── Develop basic Obsidian vault hygiene routines
    ├── Set up v1 task extraction → Todoist
    ├── Set up v1 fact extraction → Obsidian
    ├── Set up v1 Todoist inbox triage
    └── Get Bes access to Notion
```

**Obsidian note** (`/home/justin.guest/vault/Bes Setup.md`):
```
---
id: "20260521094904"
daily_note: "[[2026-05-21 Thursday]]"
category: "[[Projects]]"
---
Todoist: https://app.todoist.com/app/project/bes-setup-6gh2QFcj2F67Rhxw
```

## Todoist project URL format

```
https://app.todoist.com/app/project/<slug>-<project-id>
```

Where `<slug>` is the project name lowercased with spaces replaced by hyphens. The real identifier is the alphanumeric `<project-id>` after the last `-`.

## Pattern: create a new project

1. **Create the Todoist Project** nested under the correct area:
   ```
   add-projects(projects=[{
     name: "<Project name>",
     color: "<inherit from area or blue>",
     parentId: "<Work id: 6ggxXvCWfccF6VWc | Home id: 6ggxXvF79JFwgc8G>"
   }])
   ```
   The response includes the project `id`.

2. **Add tasks** to that project (one `add-tasks` call, up to 25):
   ```
   add-tasks(tasks=[
     {content: "First to-do", projectId: "<new project id>"},
     {content: "Second to-do", projectId: "<new project id>"},
     ...
   ])
   ```
   Tasks are flat — no sub-tasks, no `parentId`.

3. **Create the Obsidian project note** (can be parallelized with step 2):
   - Filename: simple descriptive title, no timestamp (e.g. `Bes Setup.md`)
   - Location: vault root (`/home/justin.guest/vault/`)
   - `id`: current timestamp as `YYYYMMDDHHmmss`
   - `daily_note`: wikilink to today's daily note (`[[YYYY-MM-DD dddd]]`)
   - `category`: `"[[Projects]]"`
   - Body (below frontmatter): `Todoist: <full project URL>`

   ```markdown
   ---
   id: "20260521094904"
   daily_note: "[[2026-05-21 Thursday]]"
   category: "[[Projects]]"
   ---
   Todoist: https://app.todoist.com/app/project/project-name-<project-id>
   ```

Steps 1 must come first (need the project ID). Steps 2 and 3 can be parallelized.

## Pattern: look up a project

- From Obsidian: open the note, read the `Todoist:` URL, extract the project ID (last segment after the final `-`).
- From Todoist: `find-projects(searchText: "<project name>")`. Then `get-overview(projectId)` to see all its tasks.

## Pattern: add to-dos to an existing project

1. Find the Todoist Project (via `find-projects` or from the Obsidian note's `Todoist:` link).
2. Add tasks flat into that project: `add-tasks` with `projectId` set, no `parentId`.

## Pattern: close/complete a project

1. Complete all open tasks in the project via `complete-tasks`.
2. Archive the Todoist Project via `project-management(action: "archive", projectId: "...")`.
3. Optionally update the Obsidian note — add a completion date or short retro note at the bottom. Do this only if Justin asks.

## Routing

- Work-related project → nest under **Work** (`6ggxXvCWfccF6VWc`)
- Personal/home project → nest under **Home** (`6ggxXvF79JFwgc8G`)
- Ambiguous → ask Justin before creating

## Naming convention

**Obsidian note filename == Todoist Project name.** Always. No exceptions.

- Todoist Project: `Bes Setup`
- Obsidian note: `Bes Setup.md`

If a project is renamed in one place, rename it in the other immediately. This is the primary way to navigate between the two — the names must match for the link to be meaningful. Justin enforces this manually for now; eventually a vault hygiene routine will catch drift.

## Pitfalls

1. **Tasks are flat in a project.** No sub-tasks, no `parentId`. Each to-do is its own independent task in the project.
2. **Todoist Project URL slug is cosmetic.** The real ID is the alphanumeric string after the last `-`. Use that for lookups.
3. **`update-tasks` cannot set `parentId` to null.** Omit `parentId` entirely when moving a task to a new project — the move alone detaches it from any parent.
4. **Don't use the `project` label on tasks.** Under this model, the Project container does the organizing — no label needed.
