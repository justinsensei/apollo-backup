import os
import re
import argparse

def normalize_name(filename):
    name, _ = os.path.splitext(filename)
    name = name.lower()
    words = re.findall(r'[a-z0-9]+', name)
    return "-".join(words)

def build_wikilink_map(old_vault):
    old_to_new_map = {}
    for root, dirs, files in os.walk(old_vault):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if f.endswith(".md"):
                base_title, _ = os.path.splitext(f)
                norm = normalize_name(f)
                old_to_new_map[base_title.lower()] = norm
    return old_to_new_map

def make_transform_fn(old_to_new_map):
    pattern = r'\[\[([^\]]+)\]\]'
    
    def replace_link(match):
        inner = match.group(1)
        if '|' in inner:
            target_part, display = inner.split('|', 1)
        else:
            target_part, display = inner, None
            
        if '#' in target_part:
            base_target, section = target_part.split('#', 1)
            section = '#' + section
        else:
            base_target, section = target_part, ""
            
        base_target_clean = base_target.strip()
        base_target_lower = base_target_clean.lower()
        
        if base_target_lower in old_to_new_map:
            norm_target = old_to_new_map[base_target_lower]
            disp = display if display else base_target_clean
            return f"[[{norm_target}{section}|{disp}]]"
        return match.group(0)
        
    return lambda content: re.sub(pattern, replace_link, content)

def clean_frontmatter_and_body(raw_content, transform_wikilinks, strip_meeting=False):
    cleaned = raw_content
    if raw_content.startswith("---"):
        end = raw_content.find("\n---", 3)
        if end > 0:
            fm_block = raw_content[3:end]
            body_block = raw_content[end+4:]
            
            # Clean fm lines
            fm_lines = []
            for line in fm_block.split("\n"):
                if line.startswith("id:"):
                    id_val = line.split(":", 1)[1].strip().strip("'").strip('"')
                    fm_lines.append(f"id: {id_val}")
                elif line.startswith("daily_note:"):
                    fm_lines.append(line)
                elif line.startswith("aliases:"):
                    continue
                elif line.strip() == "- null" or line.strip() == "null" or line.strip() == "-":
                    continue
                elif line.strip():
                    fm_lines.append(line)
            
            cleaned_fm = "\n".join(fm_lines).strip()
            
            # Body cleanup
            body_cleaned = body_block
            body_cleaned = re.sub(r'(?m)^[ \t]*#zettel[ \t]*$', '', body_cleaned)
            if strip_meeting:
                body_cleaned = re.sub(r'(?m)^[ \t]*#meeting[ \t]*$', '', body_cleaned)
                body_cleaned = re.sub(r'(?m)^[ \t]*#meetings[ \t]*$', '', body_cleaned)
                body_cleaned = re.sub(r'(?m)^[ \t]*#meeting #raptor[ \t]*$', '#raptor', body_cleaned)
            
            body_cleaned = transform_wikilinks(body_cleaned).strip("\n")
            cleaned = f"---\n{cleaned_fm}\n---\n\n{body_cleaned}\n"
    else:
        cleaned = transform_wikilinks(raw_content)
    return cleaned

def main():
    parser = argparse.ArgumentParser(description="Migrate and sanitize historical notes into the active vault.")
    parser.add_argument("--src", required=True, help="Path to historical source directory")
    parser.add_argument("--dest", required=True, help="Path to destination directory inside active vault")
    parser.add_argument("--strip-meeting", action="store_true", help="Strip meeting-specific inline tags")
    args = parser.parse_args()
    
    if not os.path.exists(args.src):
        print(f"Error: Source directory {args.src} does not exist.")
        return
        
    os.makedirs(args.dest, exist_ok=True)
    
    print("Scanning old vault to build wikilink map...")
    # Find the top-level old vault from the src path (assuming it is inside a vault repo)
    # We walk up to find the root of the old vault or just use src as the basis for wikilink mapping
    old_vault_root = args.src
    while old_vault_root != "/" and not os.path.exists(os.path.join(old_vault_root, ".git")):
        parent = os.path.dirname(old_vault_root)
        if parent == old_vault_root:
            break
        old_vault_root = parent
    
    print(f"Old vault root resolved to: {old_vault_root}")
    wikilink_map = build_wikilink_map(old_vault_root)
    transform_fn = make_transform_fn(wikilink_map)
    
    # Collect files to migrate
    files_to_migrate = []
    for root, dirs, files in os.walk(args.src):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if f.endswith(".md"):
                files_to_migrate.append((f, os.path.join(root, f)))
                
    print(f"Found {len(files_to_migrate)} markdown files to migrate.")
    
    success = 0
    for filename, src_path in files_to_migrate:
        try:
            norm = normalize_name(filename)
            with open(src_path, 'r', encoding='utf-8', errors='replace') as fh:
                raw = fh.read()
                
            cleaned = clean_frontmatter_and_body(raw, transform_fn, strip_meeting=args.strip_meeting)
            dest_path = os.path.join(args.dest, f"{norm}.md")
            
            with open(dest_path, 'w', encoding='utf-8') as fh:
                fh.write(cleaned)
            success += 1
        except Exception as e:
            print(f"Error migrating {filename}: {e}")
            
    print(f"Successfully migrated {success}/{len(files_to_migrate)} files to {args.dest}")

if __name__ == "__main__":
    main()
