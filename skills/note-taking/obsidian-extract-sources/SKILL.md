---
name: obsidian-extract-sources
description: An interactive workflow for compiling immutable `Inputs/Readings` into mutable, summary-focused `Notes/Sources`.
version: 1.2.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [obsidian, sources, readings, pkm, synthesis]
    related_skills: [obsidian, obsidian-ingest-log, wind-down]
---

# obsidian-extract-sources

## Overview

This skill facilitates the creation of "reading notes" (`Source` notes) from raw `Reading` inputs. It transforms the previous bibliographic function into an active, human-in-the-loop knowledge synthesis task.

The process is designed to be interactive. It finds unprocessed readings, allows for selection, generates a summary for preview, and upon confirmation, creates a new, properly formatted `Source` note in the `inbox/` for final triage.

## When to Use

- When you want to work through your backlog of readings and create synthesized notes.
- As part of a routine like `wind-down` to process one or two articles.
- When you have a specific topic in mind and want to find relevant readings to summarize.

## User-Requested Workflow

-   **Invocation:** The skill can be invoked manually or as a sub-skill.
-   **Selection:**
    -   *Unseeded:* Presents a random selection of 5 unprocessed `Readings`.
    -   *Seeded:* (Future) Presents readings relevant to a given keyword.
-   **Preview:** The proposed text of the new `Source` note (frontmatter + summary) is displayed in the chat for review before creation.
-   **Creation:** Upon confirmation, the new `Source` note is written to the `inbox/` directory, not directly into `Notes/Sources/`. This allows for manual review and triage.
-   **Looping:** The interactive session should offer to process another reading, get a new batch, or exit.

## Implementation Pitfalls & Lessons Learned

-   **Discovery of Unprocessed Readings:**
    -   **Failed Approach:** An initial attempt to use a Python script with `os.walk` to find unprocessed readings by checking for backlinks became overly complex and repeatedly failed in difficult-to-debug ways. This approach is brittle.
    -   **Correct Approach:** A much more robust and transparent method is to use the `terminal` tool with `ripgrep` (`rg`). A simple `rg -L -v "filename"` check against the `Notes/Sources/` and `inbox/` directories is sufficient to determine if a `Reading` has already been processed. Avoid complex, stateful Python file I/O for simple discovery tasks.

-   **LLM Invocation in Scripts:**
    -   **Problematic:** Using `hermes-agent delegate-task` from a Python script for simple text generation proved unreliable. It introduces unnecessary complexity and potential configuration issues for the subagent.
    -   **Preferred:** The `hermes-agent prompt` command is a more direct, simple, and robust method for getting a model completion from within a script. For single-shot text generation, it is the superior choice. `delegate-task` should be reserved for complex sub-tasks requiring their own tool use and reasoning loops.