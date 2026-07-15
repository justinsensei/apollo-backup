---
name: obsidian
description: Use when Justin asks you to search, read, write, or manage notes in the vault, OR when performing structural/physical vault maintenance (hygiene, task archiving, capitalization healing, link repair, and nightly cron plumbing).
version: 2.1.0
author: Apollo
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [obsidian, core, conventions, rules, pointers, thin-assistant, hygiene, maintenance, tasknotes, cron, links, automation]
    related_skills: [did-i-already-do-this, apollo-slack-ingest, apollo-telegram-ingest, apollo-email-dispatch, obsidian-semantic-lint, apollo-brain-ingest]
---

# Obsidian: Vault Operations & Schema Pointer

## Overview
Apollo is a **thin assistant** designed for lightweight mobile query, search, and automated background plumbing (ingestion and daily note/hygiene runs).

To prevent drift and eliminate duplication of maintenance overhead, **the Obsidian vault itself is the sole canonical source of truth for all schemas, formats, layout structures, and workflows.** These conventions are actively maintained under:
1. **Cursor Rules:** `/home/justin.guest/Developer/obsidian-vault/.cursor/rules/`
2. **Cursor Skills:** `/home/justin.guest/Developer/obsidian-vault/.cursor/skills/`

Apollo does not store hard-coded copies of note formats, category tables, or sorting rules. Instead, this skill acts as a dynamic runtime instruction directing Apollo to read the live rules directly from the filesystem prior to performing any note operations.

## When to Use
* **Use when** creating, editing, renaming, moving, searching, or reading any note in the vault.
* **Use when** running or reviewing automated ingestion pipelines (Slack, Telegram, Emails, Linear).
* **Use when** running daily scheduled hygiene checks.
* **Do not use for** modifying the underlying vault structures or schemas yourself (which is owned by Cursor).

## Rules of Engagement: Dynamic Rule Reading

Whenever you are asked to interact with files in the vault, you **must** obey the following rigid steps:

1. **Load Canonical Rules:** Read the live rules from the vault directory to retrieve current schemas, file naming conventions, and folders:
   * **General Rules (Categories, Folders, Links):** Read `/home/justin.guest/Developer/obsidian-vault/.cursor/rules/main.mdc`
   * **Note Formats & Frontmatter:** Read `/home/justin.guest/Developer/obsidian-vault/.cursor/rules/note-creation.mdc`
   * **Contacts Layouts (People/Orgs):** Read `/home/justin.guest/Developer/obsidian-vault/.cursor/rules/obsidian-contacts.mdc`
   * **File Operations (Moves, Renames, Links):** Read `/home/justin.guest/Developer/obsidian-vault/.cursor/rules/file-operations.mdc`
   * **Markdown & Syntax (Callouts, Math, YAML):** Read `/home/justin.guest/Developer/obsidian-vault/.cursor/rules/obsidian-syntax.mdc`
   * **Task Management (TaskNotes plugin & Archive):** Read `/home/justin.guest/Developer/obsidian-vault/.cursor/rules/tasknotes.mdc` and `/home/justin.guest/Developer/obsidian-vault/TaskNotes/Setup.md`
2. **Apply Rules Dynamically:** Treat the retrieved markdown contents as absolute constraints. For example:
   * Verify the exact frontmatter syntax required (e.g., `id: "YYYYMMDDHHmmss"` and `daily_note: "[[YYYY-MM-DD Weekday|YYYY-MM-DD Weekday]]"`).
   * Verify the correct category routing paths.
   * Verify filename formatting (e.g. `Title ID.md` vs `Title.md` vs `Title YYYY-MM-DD.md`).
3. **Execute Plumbing Safely:** When running automated daily cron jobs (like `vault_hygiene.py` or ingest feeds), cross-reference your script behavior against the retrieved rules to ensure the plumbing does not violate active vault conventions.

## Common Pitfalls
1. **Improvising Conventions:** Relying on cached memory or general knowledge to write note properties, file names, or folder paths. Always read the live `.cursor/rules/` files from disk first.
2. **Hard-coding YAML properties in scripts:** If a Cursor rule shifts (e.g., taxonomy change), scripts should be reviewed for alignment to prevent automated pipeline drift.
3. **Failing to check for existing files:** Before creating any note or stub, search both `/Notes/` and `/Inbox/` by name to prevent duplicate stubs.
4. **Failing to update the central wiki log:** Any newly created note (including manual quick-captures or scraps in `Inbox/`) must be logged in `Utilities/log.md` under the correct daily header (creating the header in `## YYYY-MM-DD Weekday` format if it doesn't already exist for the current date).
   - **Wiki Log Line Format:** `- HH:MM | <type> | [[Note Title]] | <vault/relative/path.md> | [[YYYY-MM-DD Weekday]]` (where `<type>` is one of `reading`, `meeting`, `email`, `slack`, `telegram`, `query`, `source-compile`, `lint`).
5. **Over-strict Filename Normalization:** While `.cursor/rules/note-creation.mdc` specifies that projects should be named `Title.md (no ID)`, in practice many active project files in `Notes/Projects/` retain their 14-digit creation timestamp ID (e.g., `Animate Correct Answers 2026 20260612145350.md`). Check the actual folder contents to match existing naming conventions before stripping IDs during file moves or renames.
6. **Stale References to Renamed/Refactored Notes:** When renaming compiled sources or other knowledge notes (particularly replacing old `{Title} {YYYY-MM-DD}.md` style names with unique 14-digit ID names `{Title} {YYYYMMDDHHmmss}.md`), always scan the entire vault for incoming references to the old filename. Standard path-healing scripts like `heal_wikilinks.py` only simplify paths; they do not map changed filenames, leaving stale references as ghost links. Write and execute a targeted python script to perform find-and-replace for these changed targets.
7. **Self-Referential & Dated Ghost Links:** When compiled sources are created from raw readings, template scripts or manual actions can accidentally insert self-referential or cross-referential links using old dates and folder paths (e.g., `[[Notes/Sources/You, Me, or Adult ADHD 2026-06-15]]`) instead of referencing the actual filename which contains a 14-digit timestamp ID (e.g., `[[You, Me, or Adult ADHD 20260615153637]]`). Always heal these to use shortest-path, ID-matched wikilinks to avoid generating persistent structural ghost links.
8. **Misattributed Links in Immutable Ingested Content:** Transcript parsers (e.g. Granola) often automatically generate wikilinks for generic names (e.g. linking "Sam Ferris" to an existing son's note `[[Sam Goff 20260610120301|Sam]] Ferris`). Even if this creates semantically incorrect or broken links, remember that files under `Inputs/` (e.g. `Inputs/Meetings/`) are strictly **immutable**. Do **not** modify them during link-healing or triage runs. Instead, report the misattributed link to the user so they can manually fix it or approve a manual override, and link the new contact correctly in other editable areas (such as the updated Organization note).

## Triage & Relocation Workflow (Moving from Inbox to Notes)

When the user asks to move/triage a scrap, concept, or decision note from `Inbox/` to its permanent home under `Notes/`:

1. **Update Frontmatter Category:** Patch the note's frontmatter to change its category from its temporary staging category (e.g., `category: "[[Scraps]]"`) to its permanent target category (e.g., `category: "[[Decisions]]"` or `category: "[[Concepts]]"`).
2. **Move the File:** Relocate the file using the Shell tool `mv` to the target directory matching the category routing table in `main.mdc` (e.g., `Notes/` for `"[[Decisions]]"` or `"[[Concepts]]"`). Maintain the unique `Title ID.md` filename structure.
3. **Log the Note Chronologically:** Check if the note is already logged in the central wiki log (`Utilities/log.md`). If it is not, insert a new entry chronologically under its original creation date header based on its 14-digit ID timestamp.
   - **Line Format:** `- HH:MM | query | [[Note Title ID]] | Notes/Note Title ID.md | [[YYYY-MM-DD Weekday]]`
4. **Run Hygiene Validation:** Manually run the structural hygiene validation script to verify that no ghost links or folder boundary violations are introduced:
   `python3 ~/.hermes/scripts/vault_hygiene_cron.py`

## Vault Hygiene & Structural Plumbing

Unlike semantic linting (which audits note content for meaning), physical and structural hygiene ensures files are in correct folders, filenames follow capitalizations, stale or completed tasks are archived, and cross-references (wikilinks) remain functional.

### Daily Vault Hygiene Pipeline
The pipeline runs autonomously every night at 9:00 PM via the cron job **"vault-hygiene"** (`0b12d967fdf6`), running `vault_hygiene_cron.py`.
The script runs silently under a **watchdog pattern**:
- Normal successful runs or quiet auto-fixes produce **no stdout**, meaning no Telegram alert is sent.
- Warnings or errors (flagged by `# 🔴` or `# ⚠️` markers) are surfaced to Telegram.

### Core Hygiene Operations

#### 1. TaskNotes Sweep & Archive (Daily)
TaskNotes represent actionable work items. Completed or abandoned items are swept out of active view to keep folders tidy:
- **`TaskNotes/Tasks/` (Subfolders):** Notes with `status: done` (case-insensitive) are moved to `TaskNotes/Archive/`.
- **`TaskNotes/` Root Directory (no subfolders):** Notes with `status: done` or `status: dropped` (case-insensitive) are moved to `TaskNotes/Archive/`.
- **Link Healing:** When a note is moved to `Archive/`, the pipeline scans all Markdown files in the vault and updates their internal wikilinks (e.g., `[[TaskNotes/Some Task]]` -> `[[TaskNotes/Archive/Some Task]]`) to prevent broken links.
- **Filename Collisions:** If an archived task has a filename collision in `Archive/`, the script appends a numeric suffix (e.g., `Some Task_1.md`).

#### 2. EIIRP Task Promotion (Checkbox-to-Note Conversion)
- **Operation:** Scans the last 96 hours of Daily Notes for raw markdown checkboxes formatted as `- [ ] <Task Name> #task`.
- **Promotion:** Automatically promotes these checkboxes into separate physical TaskNote files in `TaskNotes/Tasks/` using the standard TaskNote schema, keeping the vault highly organized.

#### 3. Filename Capitalization & Link Healing
- **Standard Proper Nouns & Acronyms:** Matches files against pre-defined rules (e.g. `ai` -> `AI`, `signlab` -> `SignLab`, `typescript` -> `TypeScript`) and renames mismatched files.
- **Link Repair:** Updates references across all files in the vault to use the corrected, newly renamed capitalized filepath.

#### 4. Folder Boundary Constraints
- **Scope Rule:** Folder-wide health audits (Missing ID, Missing Daily Note, Ghost Links, and Orphan Notes) are strictly restricted to the `Notes/` directory and its subdirectories.
- **Why:** This avoids false positives and warning noise from temporary or inbox files in `Inbox/` or `TaskNotes/`.

#### 5. Automated ID Conflict Resolution
- **Operation:** When multiple notes in the vault share the same 14-digit `id` field in their frontmatter, the pipeline automatically resolves the conflict.
- **Resolution:**
  - Keeps the alphabetical/first file's ID unchanged.
  - Increments the ID for subsequent conflicting files until a globally unique ID in the vault is found.
  - Rewrites the frontmatter `id:` field in the resolved files.
  - If the conflicting ID is present in the filename, renames the file to match the new ID.
  - Heals any incoming wikilinks to the renamed files across the entire vault.

---

### Technical & Environment Architecture: The Bidirectional Sync Gotcha
On the VM environment, changes to tracked scripts (like `vault_hygiene.py`) and configurations have a strict directory mapping.
- **The Pitfall:** The VM's active runtime directory is **`~/.hermes/`**, but there is also a backup repository at **`~/apollo-backup/`**.
- **The Mirror Mechanism:** The system runs a background daemon `apollo-autocommit.service` which watches `~/.hermes/` and mirrors its contents into `~/apollo-backup/` (using `rsync --delete`).
- **How to Avoid Reversion:** You must **never** edit python scripts directly in `~/apollo-backup/scripts/` or files under `~/apollo-backup/`. If you do, your changes will be silently deleted and overwritten on the next sync event!
- **Rule:** Always apply patches and write files to the active runtime paths under **`~/.hermes/`** (e.g., `~/.hermes/scripts/vault_hygiene.py`). The background daemon will safely mirror and commit those changes to git.

---

## Expanded Verification Checklist
- [ ] Active rules (including `main.mdc`, `note-creation.mdc`, `obsidian-contacts.mdc`, `file-operations.mdc`, and `obsidian-syntax.mdc`) retrieved from `/home/justin.guest/Developer/obsidian-vault/.cursor/rules/` before executing the operation
- [ ] Note frontmatter, title, and location checked against the retrieved Cursor rules
- [ ] Newly created notes land in `/home/justin.guest/Developer/obsidian-vault/Inbox/` first (except raw feed folders bypass)
- [ ] Central wiki log (`Utilities/log.md`) updated with the new creation under the correct date header
- [ ] Run the hygiene script manually when auditing: `python3 ~/.hermes/scripts/vault_hygiene_cron.py`
- [ ] Verify stdout of hygiene script only contains legitimate unresolved errors or is empty for a clean state
- [ ] Confirm moved tasks exist in `TaskNotes/Archive/` and are deleted from their source paths
- [ ] Check `git -C ~/apollo-backup status` and ensure the autocommit service safely mirrored and pushed updates
