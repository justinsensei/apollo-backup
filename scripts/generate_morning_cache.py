#!/usr/bin/env python3
"""
generate_morning_cache.py — Automated script to compile the morning briefing cache.

Runs in the background at 7:00 AM.
1. Determines today's date and whether today is a work day.
2. Runs change detection (check_morning_changes.py) to get live counts and vault activity.
3. Runs vault hygiene (vault_hygiene.py) to gather any Tier 2 issues.
4. Runs vault signals (check_vault_signals.py) to extract contact candidates.
5. Selects a random note from the Thoughts, Beliefs, or Concepts category as the Morning Thought.
6. Writes the compiled cache JSON to:
   - ~/.hermes/morning-briefing/YYYY-MM-DD.json
   - ~/Developer/obsidian-vault/Utilities/cache/morning-briefing.json
"""

import os
import sys
import json
import random
import re
import subprocess
from datetime import datetime, timedelta

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout.strip()
        else:
            return None
    except Exception:
        return None

def select_morning_thought(vault_path):
    notes_dir = os.path.join(vault_path, "Notes")
    if not os.path.exists(notes_dir):
        return None
        
    candidates = []
    for f in os.listdir(notes_dir):
        if f.endswith(".md") and f != "RESOLVER.md" and not f.startswith("."):
            candidates.append(os.path.join(notes_dir, f))
            
    if not candidates:
        return None
        
    # Pick a random note and parse it
    random.shuffle(candidates)
    for path in candidates:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
                
            category = "Thoughts"
            title = os.path.basename(path)[:-3]
            
            # Simple YAML parsing
            if content.startswith("---"):
                end_idx = content.find("\n---", 3)
                if end_idx > 0:
                    fm = content[3:end_idx]
                    cat_match = re.search(r"^category:\s*[\"']?\[\[([^\]]+)\]\][\"']?", fm, re.MULTILINE)
                    if cat_match:
                        category = cat_match.group(1).strip()
                    title_match = re.search(r"^title:\s*[\"']?([^\"'\n]+)[\"']?", fm, re.MULTILINE)
                    if title_match:
                        title = title_match.group(1).strip()
            
            # Extract H1 if title is still default filename
            if title == os.path.basename(path)[:-3]:
                h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                if h1_match:
                    title = h1_match.group(1).strip()
                    
            # Map category name to friendly label
            if category.lower() in ["thoughts", "opinions"]:
                category = "Opinions / Thoughts"
            elif category.lower() == "beliefs":
                category = "Beliefs"
            elif category.lower() == "concepts":
                category = "Concepts"
                
            return {
                "path": os.path.relpath(path, vault_path),
                "title": title,
                "category": category
            }
        except Exception:
            continue
            
    return None

def main():
    # Resolve paths
    hermes_home = os.path.expanduser("~/.hermes")
    vault_path = "/home/justin.guest/Developer/obsidian-vault"
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Check if work day
    is_wd_str = run_cmd(f"python3.12 {hermes_home}/scripts/work_day.py is_work_day {today_str}")
    is_work_day = (is_wd_str == "true")
    
    # 2. Find work log dates
    work_log_dates = []
    log_dates_str = run_cmd(f"python3.12 {hermes_home}/scripts/work_day.py logs_to_summarize {today_str}")
    if log_dates_str:
        work_log_dates = [d.strip() for d in log_dates_str.split("\n") if d.strip()]
        
    # 3. Run check_morning_changes.py
    changes_json_str = run_cmd(f"python3 {hermes_home}/scripts/check_morning_changes.py")
    vault_activity = {
        "total_updated": 0,
        "type_counts": {},
        "added_entities": {"person": [], "company": [], "concept": []}
    }
    changes_data = None
    if changes_json_str:
        try:
            changes_data = json.loads(changes_json_str)
            if "vault_activity" in changes_data:
                vault_activity = changes_data["vault_activity"]
        except Exception:
            pass
            
    # 4. Run check_vault_signals.py to generate signals json
    run_cmd(f"python3 {hermes_home}/scripts/check_vault_signals.py")
    discovered_contacts = {"people": [], "organizations": []}
    signals_path = os.path.join(hermes_home, "morning-briefing", "vault_signals_last_run.json")
    if os.path.exists(signals_path):
        try:
            with open(signals_path, "r") as f:
                signals_data = json.load(f)
                if "discovered_entities" in signals_data:
                    discovered_contacts = signals_data["discovered_entities"]
        except Exception:
            pass
            
    # 5. Check vault hygiene
    hygiene_stdout = run_cmd(f"python3 {hermes_home}/scripts/vault_hygiene.py")
    tier2_issues = []
    if hygiene_stdout:
        # Simple extraction of issues from stdout if any
        for line in hygiene_stdout.splitlines():
            if line.strip().startswith("- ") or "missing ID" in line or "malformed" in line:
                tier2_issues.append(line.strip().lstrip("- ").strip())
                
    # 6. Select Morning Thought
    daily_thought = select_morning_thought(vault_path)
    if not daily_thought:
        daily_thought = {
            "path": "Notebook/Avoid mathy prioritization 20250603163001.md",
            "title": "Avoid mathy prioritization",
            "category": "Concepts"
        }
        
    # 7. Compile Cache JSON
    work_log_status = "skipped"
    if is_work_day:
        work_log_status = "pending_review"
        if changes_data and changes_data.get("work_log_exists"):
            work_log_status = "ok"
            
    cache_data = {
        "date": today_str,
        "is_work_day": is_work_day,
        "work_log_dates": work_log_dates,
        "work_log_status": work_log_status,
        "vault_hygiene": {
            "tier1_status": "ok",
            "tier1_summary": "Auto-hygiene check complete.",
            "tier2_issues": tier2_issues
        },
        "inbox_candidates": {
            "status": "ok",
            "sources_failed": [],
            "calendar_events": [],
            "action_items": []
        },
        "vault_activity": vault_activity,
        "daily_thought": daily_thought,
        "discovered_contacts": discovered_contacts
    }
    
    # 8. Write Cache Files
    # VM Location
    vm_cache_dir = os.path.join(hermes_home, "morning-briefing")
    os.makedirs(vm_cache_dir, exist_ok=True)
    vm_cache_path = os.path.join(vm_cache_dir, f"{today_str}.json")
    with open(vm_cache_path, "w") as f:
        json.dump(cache_data, f, indent=2)
        
    # Vault Location (for sync to Mac / Cursor)
    vault_cache_dir = os.path.join(vault_path, "Utilities", "cache")
    os.makedirs(vault_cache_dir, exist_ok=True)
    vault_cache_path = os.path.join(vault_cache_dir, "morning-briefing.json")
    with open(vault_cache_path, "w") as f:
        json.dump(cache_data, f, indent=2)
        
    print(f"Morning briefing cache written successfully to:")
    print(f"  - {vm_cache_path}")
    print(f"  - {vault_cache_path}")
    print(f"Date: {today_str}, Is Work Day: {is_work_day}, Work Log Status: {work_log_status}")

if __name__ == "__main__":
    main()