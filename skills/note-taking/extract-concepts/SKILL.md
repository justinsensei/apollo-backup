---
name: extract-concepts
description: |
  Extracts concepts from source notes, proposing links, revisions, or new concept notes.
tags:
  - obsidian
  - knowledge-management
  - synthesis
---

# Extract Concepts

This skill facilitates the creation of new knowledge by synthesizing information from `Source` notes into `Concept` notes. It takes a "seed" (either a direct path to a `Source` note or a topic query) and proposes three types of actions for user review:

1.  **Simple links:** Connecting `Source` notes to existing, relevant `Concept` notes.
2.  **Revisions:** Updating existing `Concept` notes with new information from `Source`s.
3.  **New Concepts:** Creating new `Concept` notes based on ideas found in the `Source`s.

This is an interactive, human-in-the-loop workflow. All proposals require user approval before execution.

## Workflow

### 1. Seed Interpretation

The skill begins by interpreting the user-provided seed.

1.  **Receive Seed:** The user provides either a path to a specific `Source` note or a general topic/query.
2.  **Identify Target Sources:**
    *   If the seed is a path, that file is the single target `Source`.
    *   If the seed is a query, use the `obsidian-semantic-pointer` tool to search for relevant notes within the `~/vault/Notes/Sources/` directory. The top 3-5 results become the target `Source` notes.

    ```bash
    # Example for a query seed
    ~/.hermes/bin/obsidian-semantic-pointer search "your query here" --vault-path ~/vault --filter-path "Notes/Sources/"
    ```

### 2. Content Aggregation & Discovery

Once the target `Source` notes are identified, the skill gathers the necessary context.

1.  **Read Sources:** Read the full content of all target `Source` notes.
2.  **Create Corpus:** Combine the content into a single text corpus.
3.  **Discover Related Concepts:** Use the `obsidian-semantic-pointer` tool again, this time searching the `~/vault/Notes/Concepts/` directory with the `Source` corpus as the query.
4.  **Read Concepts:** Read the full content of the top 3-5 related `Concept` notes found.

### 3. Synthesis and Proposal Generation

This is the core reasoning step, typically delegated to a sub-agent.

-   **Input:** The `Source` corpus and the content of related `Concept`s.
-   **Task:** Analyze the inputs and generate a structured set of proposals.

The proposals should be categorized into three types:

1.  **New Links:** Identify cases where a `Source` strongly relates to an existing `Concept` without necessitating a change to the `Concept` itself. Propose adding a wikilink (e.g., `[[Concept Title]]`) to the `Source` note.
2.  **Revisions to Existing Concepts:** Identify cases where a `Source` adds significant new information, nuance, or counter-arguments to an existing `Concept`. Propose specific edits to the `Concept` note, ideally in a diff-like format.
3.  **New Concepts:** Identify distinct, valuable ideas within the `Source` corpus that are not adequately covered by any existing `Concept`. Propose the creation of a new `Concept` note, including a suggested title and body content.

### 4. Interactive Review & Execution

The final phase involves user collaboration.

1.  **Present Proposals:** Display the generated proposals to the user, clearly grouped by type (Links, Revisions, New).
2.  **Await Approval:** Ask the user to approve or reject each proposal individually or in groups.
3.  **Execute Approved Actions:**
    *   **Links:** Use the `patch` tool to add the approved wikilinks directly into the `Source` notes.
    *   **Revisions:** Use the `patch` tool to apply the approved edits to the existing `Concept` note. **Then, move the modified note to `~/vault/inbox/` for final user review.**
        ```bash
        # Example move command
        mv "~/vault/Notes/Concepts/Updated Concept.md" "~/vault/inbox/"
        ```
    *   **New Concepts:** Use the `write_file` tool to create the new `Concept` note directly within `~/vault/inbox/`.

## Pitfalls

-   **Semantic Drift:** Semantic search is powerful but not perfect. The skill must be prepared for tangentially related or irrelevant results and avoid forcing connections where none exist.
-   **Over-creation:** The default should be to integrate with existing knowledge (linking and revising) before creating something new. Avoid proposing a new `Concept` for every minor detail.
-   **User Context:** The skill operates without the user's full mental model. Its proposals are best-effort suggestions and rely on the user for final validation and contextual fitness.
