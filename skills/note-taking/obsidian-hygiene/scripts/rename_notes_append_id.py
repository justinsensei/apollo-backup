import os
import re
import sys
import subprocess
from pathlib import Path

def rename_notes_append_id(vault_path_str):
    vault_path = Path(vault_path_str)
    notes_path = vault_path / "Notes"
    rename_pairs = []

    # Identify rename candidates under Notes/ and all subdirectories
    for root, dirs, files in os.walk(notes_path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in sorted(files):
            if not f.endswith(".md") or f == "RESOLVER.md":
                continue
            full_path = Path(root) / f
            rel_path = full_path.relative_to(vault_path)
            rel_str = str(rel_path).replace("\\", "/")
            
            basename = f[:-3]
            
            # Check if basename already ends with 14-digit ID
            if re.search(r'\d{14}$', basename):
                continue
                
            # Parse ID from frontmatter
            try:
                content = full_path.read_text(encoding="utf-8", errors="ignore")
                match = re.search(r"^id:\s*['\"]?(\d+)['\"]?", content, re.MULTILINE)
                if match:
                    note_id = match.group(1).strip()
                    new_basename = f"{basename} {note_id}"
                    new_f = f"{new_basename}.md"
                    new_full_path = Path(root) / new_f
                    new_rel_path = new_full_path.relative_to(vault_path)
                    new_rel_str = str(new_rel_path).replace("\\", "/")
                    
                    rename_pairs.append({
                        "old_path": full_path,
                        "new_path": new_full_path,
                        "old_rel": rel_str,
                        "new_rel": new_rel_str,
                        "old_basename": basename,
                        "new_basename": new_basename
                    })
            except Exception as e:
                print(f"Error reading {rel_str}: {e}")

    if not rename_pairs:
        print("No files need suffix-ID renaming.")
        return

    print(f"Total notes to rename and heal: {len(rename_pairs)}")
    rename_pairs.sort(key=lambda x: len(x["old_basename"]), reverse=True)

    # Phase 1: Heal wikilinks in all vault files
    print("\nPhase 1: Healing wikilinks in all vault files...")
    total_links_healed = 0
    total_files_modified = 0

    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["Utilities", ".git", ".trash", ".cursor", ".claude"]]
        for f in sorted(files):
            if not f.endswith(".md") or f == "RESOLVER.md":
                continue
            full_path = Path(root) / f
            rel_path = full_path.relative_to(vault_path)
            rel_str = str(rel_path).replace("\\", "/")
            
            try:
                content = full_path.read_text(encoding="utf-8", errors="replace")
                file_modified = False
                
                for pair in rename_pairs:
                    old_b = pair["old_basename"]
                    new_b = pair["new_basename"]
                    
                    if old_b in content:
                        pattern = r'\[\[\s*' + re.escape(old_b) + r'\s*(?P<extra>[|#][^\]]*)?\]\]'
                        
                        def replace_target(match):
                            extra = match.group('extra') or ''
                            return f'[[{new_b}{extra}]]'
                            
                        content, count = re.subn(pattern, replace_target, content, flags=re.IGNORECASE)
                        if count > 0:
                            total_links_healed += count
                            file_modified = True
                            
                if file_modified:
                    full_path.write_text(content, encoding="utf-8")
                    total_files_modified += 1
            except Exception as e:
                print(f"Error updating links in file {rel_str}: {e}")

    print(f"Wikilink healing complete! Updated {total_links_healed} links across {total_files_modified} files.")

    # Phase 2: Rename files on disk
    print("\nPhase 2: Renaming files on disk...")
    total_renames = 0

    for pair in rename_pairs:
        try:
            if pair["new_path"].exists():
                print(f"⚠️ Destination already exists, skipping rename: {pair['new_rel']}")
                continue
            os.rename(pair["old_path"], pair["new_path"])
            total_renames += 1
        except Exception as e:
            print(f"❌ Error renaming {pair['old_rel']} to {pair['new_rel']}: {e}")

    print(f"Files renamed on disk: {total_renames}")

if __name__ == "__main__":
    import sys
    vault = sys.argv[1] if len(sys.argv) > 1 else "/home/justin.guest/vault"
    rename_notes_append_id(vault)
