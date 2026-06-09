import os
import re
import sys
import json
import time
import argparse
from datetime import datetime, timedelta

def get_recent_files(vault_path, hours=48):
    target_folders = [
        'Daily Notes',
        'Logs/Meetings',
        'Logs/Readings'
    ]
    
    cutoff_time = time.time() - (hours * 3600)
    recent_logs = []
    
    for folder in target_folders:
        dir_path = os.path.join(vault_path, folder)
        if not os.path.exists(dir_path):
            continue
            
        for root, _, files in os.walk(dir_path):
            for f in files:
                if f.endswith('.md'):
                    path = os.path.join(root, f)
                    try:
                        mtime = os.path.getmtime(path)
                        if mtime >= cutoff_time:
                            # Read the content
                            with open(path, 'r', encoding='utf-8', errors='replace') as file_obj:
                                content = file_obj.read()
                            
                            # Strip frontmatter for reading if needed, but keeping it is fine.
                            # Get relative path for clean display
                            rel_path = os.path.relpath(path, vault_path)
                            
                            # Truncate content to avoid token overflow
                            truncated_content = content[:2000] if len(content) > 2000 else content
                            
                            recent_logs.append({
                                "path": rel_path,
                                "title": f[:-3],
                                "mtime": datetime.fromtimestamp(mtime).isoformat(),
                                "content": truncated_content
                            })
                    except Exception as e:
                        pass
                        
    # Sort by mtime descending
    recent_logs.sort(key=lambda x: x['mtime'], reverse=True)
    return recent_logs

def main():
    parser = argparse.ArgumentParser(description="Scan recent logs for note suggestion context.")
    parser.add_argument('--hours', type=int, default=48, help="Lookback hours (default 48)")
    parser.add_argument('--vault', type=str, default=None, help="Vault path")
    args = parser.parse_args()
    
    vault_path = args.vault or os.environ.get('OBSIDIAN_VAULT_PATH', '/home/justin.guest/vault')
    
    if not os.path.exists(vault_path):
        print(json.dumps({"error": f"Vault path {vault_path} does not exist"}))
        sys.exit(1)
        
    logs = get_recent_files(vault_path, args.hours)
    
    print(json.dumps({
        "logs": logs,
        "total_found": len(logs),
        "lookback_hours": args.hours
    }, indent=2))

if __name__ == '__main__':
    main()
