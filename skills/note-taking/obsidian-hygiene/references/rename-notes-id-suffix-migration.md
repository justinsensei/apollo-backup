# Note ID Suffix Mass Migration (June 2026)

## Overview
In June 2026, a mass migration was performed on Justin's vault to ensure that **every note under `/Notes/` and its subdirectories (including projects, contacts, and references)** has its unique 14-digit frontmatter ID appended as a suffix to the filename (e.g. `Title ID.md`).

This serves as a robust, redundant backup link-repair mechanism: if files are renamed or categories are shifted, the ID remains intact, allowing automated link healers to repair broken links instantly.

---

## Technical Playbook

### 1. Pre-Migration Sanitization (The Nested Link Loop Problem)
When scanning links across a legacy vault, look out for extreme line sizes caused by infinite bracket nesting bugs from past, buggy auto-linkers. Specifically, look for lines with thousands of repetitions of:
`[[Jim Massie]] [[Jim Massie]] [[Jim Dieterle|Dieterle]]|[[Jim Dieterle|Dieterle]]`

**remedy Script Pattern:**
Always scan and shrink these line lengths back to standard single links first before running any renaming or global regex updates:
```python
if len(line) > 1000 and ("[[Jim Massie]]" in line or "[[Jim Dieterle" in line):
    # Reconstruct a clean line
    new_line = "- [x] [Get help with the tax clearance certificate stuff (ask [[Jim Massie]] or [[Jim Dieterle]])](things://...)"
```

### 2. Suffix-ID Note Renaming and Healing
Use `scripts/rename_notes_append_id.py` to systematically rename any files under `/Notes/` (including `/Notes/Contacts/` and `/Notes/Projects/`) that do not yet have their frontmatter ID in their filename.
- **Phase 1 (Heal Links First):** Scan all markdown files in the entire vault. For each rename pair, perform a case-insensitive search and replace using:
  `pattern = r'\[\[\s*' + re.escape(old_basename) + r'\s*(?P<extra>[|#][^\]]*)?\]\]'`
  Replace with:
  `[[<new_basename>\g<extra>]]`
- **Phase 2 (Rename Files):** Execute the actual filesystem `os.rename` from the old path to the new path.
- **Phase 3 (Index Update):** Run `python3 ~/.hermes/scripts/semantic_pointer.py index` to update vector search embeddings.
