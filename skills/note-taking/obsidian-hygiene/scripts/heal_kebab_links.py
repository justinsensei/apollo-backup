import os
import re
from pathlib import Path
from collections import defaultdict

def heal_kebab_links(vault_path_str):
    vault_path = Path(vault_path_str)
    id_map = {}
    existing_basenames = {}

    # 1. Walk vault to map ID -> Note Name
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["Inputs", "Readwise", "Utilities", ".git", ".trash", ".cursor", ".claude", "Daily Notes"]]
        for f in sorted(files):
            if not f.endswith(".md") or f == "RESOLVER.md":
                continue
            full_path = Path(root) / f
            basename_no_ext = f[:-3]
            existing_basenames[basename_no_ext.lower()] = basename_no_ext
            
            try:
                content = full_path.read_text(encoding="utf-8", errors="ignore")
                match = re.search(r"^id:\s*['\"]?(\d+)['\"]?", content, re.MULTILINE)
                if match:
                    id_map[match.group(1)] = basename_no_ext
            except Exception as e:
                print(f"Error reading {f} for ID: {e}")

    # 2. Find and heal broken links with 14-digit IDs
    changes_to_apply = defaultdict(list)

    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["Utilities", ".git", ".trash", ".cursor", ".claude"]]
        for f in sorted(files):
            if not f.endswith(".md") or f == "RESOLVER.md":
                continue
            full_path = Path(root) / f
            rel_path = full_path.relative_to(vault_path)
            rel_str_f = str(rel_path).replace("\\", "/")
            
            try:
                content = full_path.read_text(encoding="utf-8", errors="replace")
                wikilinks = re.findall(r'<!--.*?-->|\[\[([^\]]+)\]\]', content)
                
                for link in wikilinks:
                    if not link or link.startswith("<!--"):
                        continue
                    target_part = link.split('|')[0].strip()
                    file_target = target_part.split('#')[0].strip()
                    
                    if not file_target:
                        continue
                    
                    norm_target = file_target.replace("\\", "/").lower().strip()
                    resolved = norm_target in existing_basenames or (norm_target + ".md") in existing_basenames
                    
                    if not resolved:
                        id_match = re.search(r'\d{14}', file_target)
                        if id_match:
                            target_id = id_match.group(0)
                            if target_id in id_map:
                                changes_to_apply[rel_str_f].append((file_target, id_map[target_id]))
            except Exception as e:
                print(f"Error scanning {f}: {e}")

    # 3. Apply changes in-place
    total_files_changed = 0
    total_links_healed = 0

    for file_path, replacements in sorted(changes_to_apply.items()):
        full_file_path = vault_path / file_path
        content = full_file_path.read_text(encoding="utf-8", errors="replace")
        
        for old_target, new_target in replacements:
            pattern = r'\[\[\s*' + re.escape(old_target) + r'\s*(?P<extra>[|#][^\]]*)?\]\]'
            
            def replace_target(match):
                extra = match.group('extra') or ''
                return f'[[{new_target}{extra}]]'
                
            new_content, count = re.subn(pattern, replace_target, content, flags=re.IGNORECASE)
            if count > 0:
                content = new_content
                total_links_healed += count
                
        full_file_path.write_text(content, encoding="utf-8")
        total_files_changed += 1

    print(f"Healed {total_links_healed} links across {total_files_changed} files.")

if __name__ == "__main__":
    import sys
    vault = sys.argv[1] if len(sys.argv) > 1 else "/home/justin.guest/vault"
    heal_kebab_links(vault)
