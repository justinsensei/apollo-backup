---
name: obsidian-extract-sources
description: Use when creating or recording cheat sheets, factsheets, guidelines, or other people's conceptual summaries under Notes/. Also contains the workflow for compiling immutable `Inputs/Readings` into mutable `Notes/Sources`.
version: 1.1.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [obsidian, references, sources, readings, compile]
    related_skills: [obsidian, obsidian-ingest-log, obsidian-suggest-promotions]
---

# obsidian-extract-sources

## Overview

This skill facilitates the creation of "reading notes" (`Source` notes) from raw `Reading` inputs. It transforms the previous bibliographic function into an active knowledge-synthesis task, where a human is always in the loop. The process is driven by an interactive script that generates a summary of a reading and creates a new, properly formatted `Source` note in the vault.

## When to Use

-   When you want to work through your backlog of readings and create synthesized notes.
-   As part of a routine like `wind-down` to process one or two articles.
-   When you have a specific topic in mind and want to find relevant readings to summarize.

## Invocation Workflows

This skill can be invoked in three ways via its main script (`scripts/main.py`):

1.  **Manual, Unseeded:**
    - **Trigger:** Run the skill with no arguments.
    - **Process:** The script presents a random selection of 5 `Readings` that do not have a corresponding `Source` note. You can choose one to process, request another batch of 5, or exit. Once a reading is chosen, a `Source` note is generated.
    - **Loop:** After creation, the skill will ask if you want to process another.

2.  **Manual, Seeded:** (To be implemented)
    - **Trigger:** Run the skill with a seed keyword or topic.
    - **Process:** The script will find up to 5 relevant `Readings` matching the seed. You choose one to process into a `Source` note.
    - **Loop:** After creation, you can process another from the same topic, provide a new seed, or exit.

3.  **Automatic, Sub-skill:**
    - **Trigger:** Called from another skill (e.g., `wind-down`) with a `--mode=single-run` flag.
    - **Process:** Same as the unseeded manual process, but it exits immediately after the first `Source` note is created, without offering another loop.

## Implementation Notes

-   **Core Logic:** The core extraction is handled by `scripts/create_source_note.py`. This script takes a path to a `Reading`, generates a summary using an LLM call, and creates the new `Source` file in `Notes/Sources/`.
-   **Interactive Wrapper:** The main workflow is managed by `scripts/main.py`, which finds unprocessed readings and handles user interaction.

## Pitfalls

-   **LLM Invocation in Scripts:** During development, using `hermes-agent delegate-task` within the script proved unreliable for simple text generation, failing due to subagent configuration complexities. The implementation was changed to use `hermes-agent prompt`, which is a more direct and robust method for getting a simple model completion from a script. For complex, multi-tool sub-tasks, `delegate-task` remains the right choice, but for single-shot generation, `prompt` is preferred.