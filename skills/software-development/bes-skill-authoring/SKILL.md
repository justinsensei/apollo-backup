---
name: bes-skill-authoring
description: "Author Bes-specific skills under ~/.hermes/skills/: frontmatter, validator, structure."
version: 1.0.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [skills, authoring, bes, conventions, skill-md]
    related_skills: [writing-plans, requesting-code-review]
---

# Authoring Bes Skills

## Overview

Bes skills are durable, procedural knowledge for specific kinds of work (vault conventions, work logs, narrower tools, daily rituals).

There are two places a SKILL.md can live:

1. **User-local (primary for Bes):** `~/.hermes/skills/<category>/<name>/SKILL.md` — personal, not shared. Created via `skill_manage(action='create')`.
2. **In-repo (for development of Hermes core):** `/home/bb/hermes-agent/skills/<category>/<name>/SKILL.md`.

Since Bes is a customized personal assistant for Justin, we focus almost exclusively on **User-local** skills under `~/.hermes/skills/` to codify personal rituals and Obsidian integration.

## When to Use

- Justin asks you to save an approach as a skill, or remember a procedure.
- You identify a stable, reusable workflow (e.g., custom data parsing, syncing scripts, platform integrations).
- You need to update or maintain an existing Bes-specific skill.

## Required Frontmatter

Source of truth: `tools/skill_manager_tool.py::_validate_frontmatter`. Hard requirements:

- Starts with `---` as the first bytes (no leading blank line).
- Closes with `\n---\n` before the body.
- Parses as a YAML mapping.
- `name` field present.
- `description` field present, ≤ **1024 chars** (`MAX_DESCRIPTION_LENGTH`).
- Non-empty body after the closing `---`.

Peer-matched shape used by every skill under `~/.hermes/skills/`:

```yaml
---
name: my-skill-name               # lowercase, hyphens, ≤64 chars (MAX_NAME_LENGTH)
description: Use when <trigger>. <one-line behavior>.
version: 1.0.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [short, descriptive, tags]
    related_skills: [other-skill, another-skill]
---
```

## Size Limits

- Description: ≤ 1024 chars (enforced).
- Full SKILL.md: ≤ 100,000 chars (enforced as `MAX_SKILL_CONTENT_CHARS`, ~36k tokens).
- Peer skills sit at **8-14k chars**. Aim for that range. If you're pushing past 20k, split into `references/*.md` and reference them from SKILL.md.

## Peer-Matched Structure

Every skill follows roughly:

```
# <Title>

## Overview
One or two paragraphs: what and why.

## When to Use
- Bulleted triggers
- "Don't use for:" counter-triggers

## <Topic sections specific to the skill>
- Quick-reference tables are common
- Code blocks with exact commands
- Bes-specific recipes and variables

## Common Pitfalls
Numbered list of mistakes and their fixes.

## Verification Checklist
- [ ] Checkbox list of post-action verifications

## One-Shot Recipes (optional)
Named scenarios → concrete command sequences.
```

Not every section is mandatory, but `Overview` + `When to Use` + actionable body + pitfalls are the minimum for the skill to feel like a peer.

## Directory Placement

User-local skills live under:
```
~/.hermes/skills/<category>/<skill-name>/SKILL.md
```

Categories currently in use (confirm with `skills_list`): `apple`, `autonomous-ai-agents`, `creative`, `daily-rituals`, `data-science`, `devops`, `email`, `gaming`, `github`, `mcp`, `media`, `mlops`, `note-taking`, `productivity`, `red-teaming`, `research`, `smart-home`, `social-media`, `software-development`.

Pick the closest existing category. For Bes notes and workflows, `note-taking` or `daily-rituals` is usually best. For technical scripts, `software-development` is best.

## Workflow

1. **Survey peers** in the target category:
   For example: `note-taking/obsidian` or `note-taking/work-log`.
2. **Draft** with `skill_manage(action='create', ...)` to create the user-local skill.
3. **Verify** using `skill_view(name=...)` once created (or in a fresh session).

## Editing Existing Skills

- **Small fix (typo, added pitfall, tightened trigger):** Use `skill_manage(action='patch', name=..., old_string=..., new_string=...)`.
- **Major rewrite:** Use `skill_manage(action='edit', name=..., content=...)` to supply the full new content.
- **Always verify** the edit — skills are living documents and should be maintained quietly as pitfalls arise.

## Common Pitfalls

1. **Leading whitespace before `---`.** The validator checks `content.startswith("---")`; any leading blank line or BOM fails validation.

2. **Description too generic.** Peer descriptions start with "Use when ..." and describe the *trigger class*, not the one task. "Use when debugging X" > "Debug X".

3. **Forgetting the author/license/metadata block.** Not validator-enforced, but every peer has it; omitting makes the skill look half-finished.

4. **Writing a skill that duplicates a peer.** Before creating, list skills and search. Prefer extending an existing skill to creating a narrow sibling.

5. **Embedding scanner-tripping command shapes in skill content.** Inside each subagent context block, tell the agent which JSON parser to use (`jq` is installed everywhere) and forbid unsafe shapes explicitly (e.g. `cmd | python3 -c`, `cmd | bash`, `cmd | node -e`, or `curl | sh`).

## Verification Checklist

- [ ] File created successfully via `skill_manage` (lives in `~/.hermes/skills/`)
- [ ] Frontmatter starts at byte 0 with `---`, closes with `\n---\n`
- [ ] No embedded `| python3 -c`, `| bash`, `| node -e`, or `curl ... | sh` patterns in example commands or subagent context blocks
- [ ] `name`, `description`, `version`, `author`, `license`, `metadata.hermes.{tags, related_skills}` all present
- [ ] Name ≤ 64 chars, lowercase + hyphens
- [ ] Description ≤ 1024 chars and starts with "Use when ..."
- [ ] Total file ≤ 100,000 chars (aim for 8-15k)
- [ ] Structure: `# Title` → `## Overview` → `## When to Use` → body → `## Common Pitfalls` → `## Verification Checklist`
