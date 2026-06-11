---
name: vault-schema-change
description: Use when Justin asks to change, update, or migrate any Obsidian vault schema rules, frontmatter properties, folder structure, or note types. Ensures synchronization of skills, docs, scripts, folders, and notes.
platforms: [linux, macos]
version: 1.0.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [obsidian, schema, migration, hygiene, scripts]
    related_skills: [obsidian, obsidian-hygiene, bes-skill-authoring]
---

# Vault Schema Change and Migration

## Overview
This skill outlines the standard operating procedure for designing, executing, and verifying schema changes in Justin's Obsidian vault. A schema change is any structural update that alters note frontmatter rules, folder layouts, note category definitions, or linter criteria. 

Because the vault, the python utility scripts, and Bes's procedural skills are tightly coupled, any schema change must be propagated systematically across all three layers to avoid linter errors, sync conflicts, and broken automation.

---

## When to Use
- Justin asks to add, rename, or delete a YAML frontmatter property (e.g., adding `status` or renaming `daily_note` to `creation_date`).
- Justin asks to change the target folder of a note category (e.g., moving `[[Decisions]]` from `Notes/` to `Notes/Decisions/`).
- Justin asks to introduce a new note category with specific folder routing and frontmatter fields.
- Justin asks to alter baseline formatting or capitalization rules enforced by linter scripts.

**Don't use for:**
- Writing general notes, contacts, or work logs.
- Simple, one-off text editing inside individual notes.
- Routine daily/weekly note-triage.

---

## Step-by-Step Procedure

### Phase 1: Analysis & Impact Mapping
Before modifying any files, identify every component affected by the proposed change. Search for occurrences of the target field, category, or path across the environment:
1. **Search Skills:** `search_files(path="~/.hermes/skills", pattern="category-name-or-property")` to see which skills document this behavior.
2. **Search Scripts:** `search_files(path="~/bes-backup/scripts", pattern="category-name-or-property")` to find references in linter or fetcher scripts (e.g., `vault_hygiene.py`, `wiki_semantic_lint.py`, `integrate_entities.py`).
3. **Analyze Vault Notes:** Estimate the number of notes in the physical vault (`~/vault/`) that will need to be updated.

### Phase 2: Design & Verification (Dry Run Plan)
Always write out a structured implementation plan and present it to Justin before taking destructive action.
- Outline the exact frontmatter/path differences (Before vs. After).
- Enumerate the skills, scripts, and notes to be modified.
- Include the source code of any temporary migration scripts you plan to run.

### Phase 3: Updating Skills & Documentation
Update all procedural skills first so that future sessions and subagents don't revert or violate the new schema.
1. Use `skill_manage(action='patch')` to update:
   - `obsidian` (specifically the frontmatter schema section and the global routing table).
   - Category-specific skills (e.g. `obsidian-notes`, `obsidian-people`, `obsidian-projects`, `obsidian-decisions`).
   - `obsidian-hygiene` (if the reporting sections or folder hierarchies change).
2. Validate updated skills using the conformance script:
   ```bash
   python3 ~/.hermes/scripts/test_skills_conformance.py --skill <skill-name>
   ```

### Phase 4: Updating Python Scripts & Automation
Enforce the new schema in the active python scripts so that subsequent runs do not fail or flag false positives.
1. Use the `patch` tool to update the schema rules in:
   - `/home/justin.guest/bes-backup/scripts/vault_hygiene.py` (update `expected_folder_prefix` and/or frontmatter checks).
   - `/home/justin.guest/bes-backup/scripts/wiki_semantic_lint.py` (if any semantic checks are impacted).
2. If necessary, test the scripts locally to ensure no syntax errors are introduced.

### Phase 5: Executing Physical Note Migration
When hundreds of notes need their frontmatter or paths updated, write a targeted Python script to handle the migration safely and systematically.
1. **Script Template (`/home/justin.guest/bes-backup/scripts/migrate_<schema_name>.py`):**
   ```python
   #!/usr/bin/env python3
   import os
   import re
   import yaml
   from pathlib import Path

   VAULT = Path(os.environ.get("OBSIDIAN_VAULT_PATH", "/home/justin.guest/vault"))

   def migrate_note(path, dry_run=True):
       with open(path, 'r', encoding='utf-8') as f:
           content = f.read()

       # Parse frontmatter
       fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
       if not fm_match:
           return False

       fm_raw = fm_match.group(1)
       body = content[fm_match.end():]

       try:
           # Use safe_load to inspect, but edit carefully to preserve comments/quotes
           data = yaml.safe_load(fm_raw)
       except Exception as e:
           print(f"Failed to parse YAML in {path.name}: {e}")
           return False

       # Perform the schema change condition (example: adding a field)
       modified = False
       if 'target_property' in data:
           # Do some transformation
           # ...
           modified = True

       if modified and not dry_run:
           # Rebuild note safely
           # Note: wrapped wikilinks must have double quotes (e.g. "[[Category]]")
           # ...
           with open(path, 'w', encoding='utf-8') as f:
               f.write(new_content)
           return True
       return modified
   ```
2. **Run Dry Run First:** Execute the migration script with a `--dry-run` flag to print which files would be changed and how, without writing to disk.
3. **Execute:** Once verified, run the script to apply the changes to the physical notes.

### Phase 6: Post-Migration Validation
Ensure everything is clean and in its proper place.
1. Run the local hygiene script to check the physical notes:
   ```bash
   python3 /home/justin.guest/bes-backup/scripts/vault_hygiene.py
   ```
   *Verify there are no new 🔴 Wrong folder, 🔴 Missing ID, or 🔴 syntax errors in the stdout.*
2. Check that the `bes-vault-sync` background service is running and successfully pushing changes to GitHub.

---

## Common Pitfalls

1. **Forgetting to update `vault_hygiene.py` before migrating notes.** If the migration script updates notes to the new schema while the hygiene script still expects the old schema, the background cron/hygiene runs will immediately flag all migrated notes as critical violations.
2. **YAML Parsing Exceptions on Wikilinks.** YAML frontmatter parsing will fail if double brackets are not wrapped in double quotes (e.g., `category: [[People]]` fails, whereas `category: "[[People]]"` passes). Always wrap any wikilink added to the frontmatter in double quotes.
3. **Modifying `bes-backup/` scripts without testing them.** An uncaught syntax error in `vault_hygiene.py` will break the daily morning/evening cron runs and block the background sync pipeline. Always smoke-test script modifications.
4. **Incorrect/Incomplete regex when matching frontmatter boundaries.** Ensure the regex matches the very start of the file (`^---`) and handles both `\r\n` and `\n` line endings.
5. **Overwriting or losing existing custom fields or comments** in frontmatter when stringifying objects back to YAML. Use line-by-line regex patching or specialized YAML parsers rather than a destructive dump that erases formatting.

---

## Verification Checklist

- [ ] Identified all affected skills, scripts, and directories in Phase 1
- [ ] Drafted and confirmed the Migration Plan with Justin
- [ ] Patched all schema-documenting skills and verified with `test_skills_conformance.py`
- [ ] Updated `/home/justin.guest/bes-backup/scripts/vault_hygiene.py` and confirmed no syntax errors
- [ ] Ran migration script in `--dry-run` mode first and inspected diff outputs
- [ ] Executed physical note migration across `~/vault/`
- [ ] Ran `vault_hygiene.py` on the live vault and confirmed a zero-error/zero-warning report
- [ ] Verified that changes are synced to the remote GitHub repository
