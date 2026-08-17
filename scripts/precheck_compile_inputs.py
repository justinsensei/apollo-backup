#!/usr/bin/env python3
import subprocess
import os
import sys

VAULT_DIR = "/home/justin.guest/Developer/obsidian-vault"

def sync_semantic_index():
    print("--- Running Incremental Semantic Indexing ---")
    script_path = os.path.expanduser("~/.hermes/scripts/semantic_pointer.py")
    if not os.path.exists(script_path):
        print("⚠️ Semantic pointer script not found.")
        return
    try:
        env = os.environ.copy()
        env_file = os.path.expanduser("~/.hermes/.env")
        if os.path.exists(env_file):
            with open(env_file) as ef:
                for line in ef:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip().strip('"\'')
        res = subprocess.run([sys.executable, script_path, "index"], env=env, capture_output=True, text=True, timeout=120)
        if res.returncode == 0:
            output = res.stdout.strip()
            if output:
                print(output)
            else:
                print("Index up to date.")
        else:
            print(f"⚠️ Indexing returned code {res.returncode}: {res.stderr.strip()[:200]}")
    except Exception as e:
        print(f"⚠️ Semantic indexing check skipped: {e}")

def main():
    # 0. Sync semantic vector embeddings incrementally first
    sync_semantic_index()

    # Scan for candidate files for compile-inputs
    print("\n--- Scanning for Compile-Inputs Candidates ---")
    
    # 1. Unprocessed Readings in Inputs/Readings/
    readings_dir = os.path.join(VAULT_DIR, "Inputs", "Readings")
    readings = []
    if os.path.isdir(readings_dir):
        for f in os.listdir(readings_dir):
            if f.endswith(".md"):
                if not f[:-3].endswith("-") and len(f) > 13:
                    date_part = f[-13:-3]
                    if len(date_part) == 10 and date_part[4] == '-' and date_part[7] == '-':
                        continue
                readings.append(os.path.join("Inputs", "Readings", f))
                
    print(f"Unprocessed Readings found: {len(readings)}")
    for r in readings[:5]:
        print(f"  - {r}")
        
    # 2. Eligible Sources without notebook_proposal: in Inputs/Sources/ or Inbox
    sources_dir = os.path.join(VAULT_DIR, "Inputs", "Sources")
    inbox_dir = os.path.join(VAULT_DIR, "Inbox")
    
    def check_frontmatter_no_proposal(filepath):
        try:
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()
                if content.startswith("---"):
                    parts = content.split("---")
                    if len(parts) >= 3:
                        frontmatter = parts[1]
                        if "category:" in frontmatter:
                            cat_line = [line for line in frontmatter.splitlines() if line.startswith("category:")]
                            if cat_line:
                                is_source = "[[Sources]]" in cat_line[0] or "Sources" in cat_line[0]
                                if is_source and "notebook_proposal:" not in frontmatter:
                                    return True
                        if "Inputs/Sources" in filepath and "notebook_proposal:" not in frontmatter:
                            return True
        except Exception:
            pass
        return False

    sources_candidates = []
    if os.path.isdir(sources_dir):
        for root, _, files in os.walk(sources_dir):
            for file in files:
                if file.endswith(".md"):
                    p = os.path.join(root, file)
                    if check_frontmatter_no_proposal(p):
                        rel_p = os.path.relpath(p, VAULT_DIR)
                        sources_candidates.append(rel_p)
                        
    inbox_sources = []
    if os.path.isdir(inbox_dir):
        for file in os.listdir(inbox_dir):
            if file.endswith(".md"):
                p = os.path.join(inbox_dir, file)
                if check_frontmatter_no_proposal(p):
                    rel_p = os.path.relpath(p, VAULT_DIR)
                    inbox_sources.append(rel_p)
                    
    print(f"Eligible Sources without proposals: {len(sources_candidates) + len(inbox_sources)}")
    for s in (sources_candidates + inbox_sources)[:5]:
        print(f"  - {s}")
        
    # 3. Eligible non-Reading Inputs without notebook_proposal:
    other_inputs = []
    input_dirs = ["Meetings", "Scraps", "Emails", "Slack", "Telegram"]
    for d in input_dirs:
        d_path = os.path.join(VAULT_DIR, "Inputs", d)
        if os.path.isdir(d_path):
            for root, _, files in os.walk(d_path):
                for file in files:
                    if file.endswith(".md"):
                        p = os.path.join(root, file)
                        try:
                            with open(p, 'r', errors='ignore') as f:
                                content = f.read()
                                if "notebook_proposal:" not in content:
                                    other_inputs.append(os.path.relpath(p, VAULT_DIR))
                        except Exception:
                            pass
                            
    print(f"Eligible Non-Reading Inputs without proposals: {len(other_inputs)}")
    for o in other_inputs[:5]:
        print(f"  - {o}")

if __name__ == "__main__":
    main()
