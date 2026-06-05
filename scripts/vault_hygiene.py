#!/usr/bin/env python3
"""
vault_hygiene.py — Obsidian vault hygiene check + auto-fix.
Leverages `gbrain lint --fix` for content fixes and misplaced file moving,
runs local checks for ID conflicts, missing IDs, and missing daily notes,
and automatically checks calendar events against vault notes to identify missing meeting notes.
"""

import os
import re
import json
import datetime
import subprocess
from collections import defaultdict
from pathlib import Path

VAULT = Path("/home/justin.guest/vault")
MEETINGS_DIR = VAULT / "meetings"

# 1. Run gbrain lint --fix to auto-fix and move files
print("Running gbrain lint...")
subprocess.run(["gbrain", "lint", str(VAULT), "--fix"], capture_output=True, text=True)

# 2. Walk the vault to detect ID conflicts, missing ID, missing daily_note
id_to_paths = defaultdict(list)
missing_ids = []
missing_daily_notes = []

# Folders to skip for manual checks
skip_dirs = {"Readwise", "utilities", ".git", ".trash", ".cursor", ".claude", "sources", "daily"}

for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_dirs]
    for f in sorted(files):
        if not f.endswith(".md") or f == "RESOLVER.md":
            continue
        path = Path(root) / f
        text = path.read_text(encoding="utf-8", errors="replace")
        
        # Parse frontmatter
        note_id = ""
        daily_note = ""
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end > 0:
                fm_raw = text[3:end]
                id_match = re.search(r"^id:\s*[\"']?(\d+)[\"']?", fm_raw, re.MULTILINE)
                dn_match = re.search(r"^daily_note:\s*[\"']?([^\"'\n]+)[\"']?", fm_raw, re.MULTILINE)
                if id_match:
                    note_id = id_match.group(1).strip()
                if dn_match:
                    daily_note = dn_match.group(1).strip()
        
        rel_path = path.relative_to(VAULT)
        if note_id:
            id_to_paths[note_id].append(rel_path)
        else:
            missing_ids.append(rel_path)
            
        if not daily_note or "[[" not in daily_note:
            missing_daily_notes.append(rel_path)

# 3. Check for missing meeting notes based on calendar events (last 4 days)
missing_meetings = []
try:
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=4)
    end_date = today
    
    start_str = start_date.strftime("%Y-%m-%dT00:00:00")
    end_str = end_date.strftime("%Y-%m-%dT23:59:59")
    
    # Query Google Calendar via gws_multi.py wrapper
    cmd = [
        "python3",
        "/home/justin.guest/.hermes/skills/productivity/google-workspace/scripts/gws_multi.py",
        "--account", "all",
        "calendar", "list",
        "--start", start_str,
        "--end", end_str,
        "--max", "100"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if res.returncode == 0:
        events = json.loads(res.stdout)
        
        # Criteria for relevant meetings
        meeting_keywords = ["sync", "huddle", "1-on-1", "1:1", "meeting", "call", "review", "workshop", "check-in", "check in", "interview", "discussion", "status", "align", "appointment"]
        ignored_keywords = ["home", "hold", "out of office", "ooo", "lunch", "placeholder", "focus time", "travel", "blocked", "gym", "drums", "music", "ortho", "celebration", "commencement", "last day", "birthday", "urology", "autoworx"]
        
        relevant_events = []
        for ev in events:
            title = ev.get("summary", "").strip()
            title_lower = title.lower()
            if "T" not in ev.get("start", ""):  # Skip all-day events
                continue
            if any(k in title_lower for k in ignored_keywords):
                continue
            is_work = ev.get("account") == "work"
            has_keyword = any(k in title_lower for k in meeting_keywords)
            if is_work or has_keyword:
                relevant_events.append(ev)
                
        # Parse existing meeting notes
        existing_notes = []
        if MEETINGS_DIR.exists():
            for f in MEETINGS_DIR.glob("*.md"):
                content = f.read_text(encoding="utf-8", errors="replace")
                created_time = None
                title = ""
                if content.startswith("---"):
                    end = content.find("\n---", 3)
                    if end > 0:
                        fm_raw = content[3:end]
                        created_match = re.search(r"^created:\s*[\"']?([^\"'\n]+)[\"']?", fm_raw, re.MULTILINE)
                        title_match = re.search(r"^title:\s*[\"']?([^\"'\n]+)[\"']?", fm_raw, re.MULTILINE)
                        if created_match:
                            created_str = created_match.group(1).strip()
                            try:
                                if "T" in created_str:
                                    created_time = datetime.datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                                else:
                                    created_time = datetime.datetime.strptime(created_str.split(".")[0], "%Y-%m-%d %H:%M:%S")
                                    created_time = created_time.replace(tzinfo=datetime.timezone.utc)
                            except Exception:
                                pass
                        if title_match:
                            title = title_match.group(1).strip()
                existing_notes.append({
                    "filename": f.name,
                    "created_time": created_time,
                    "title": title
                })
                
        def clean_words(text):
            words = re.findall(r'[a-z0-9]+', text.lower())
            stopwords = {"and", "with", "meeting", "sync", "call", "huddle", "1-on-1", "1:1", "check-in", "check", "in", "appointment"}
            return {w for w in words if len(w) > 2 and w not in stopwords}
            
        for ev in relevant_events:
            ev_title = ev.get("summary", "").strip()
            ev_start_str = ev.get("start", "")
            ev_start_dt = datetime.datetime.fromisoformat(ev_start_str)
            if ev_start_dt.tzinfo is None:
                ev_start_dt = ev_start_dt.replace(tzinfo=datetime.timezone.utc)
                
            ev_date_str = ev_start_str.split("T")[0]
            ev_words = clean_words(ev_title)
            
            found = False
            for note in existing_notes:
                # 1. Date must match
                if not note["filename"].startswith(ev_date_str):
                    continue
                    
                # 2. Check if creation times are close (within 45 minutes)
                if note["created_time"] is not None:
                    time_diff = abs((note["created_time"] - ev_start_dt).total_seconds())
                    if time_diff < 45 * 60:
                        found = True
                        break
                        
                # 3. Textual overlap
                note_words = clean_words(note["filename"] + " " + note["title"])
                if ev_words and ev_words.intersection(note_words):
                    found = True
                    break
                    
                # 4. Normalization match
                norm_ev = re.sub(r'[^a-z0-9]+', '', ev_title.lower())
                norm_note = re.sub(r'[^a-z0-9]+', '', note["filename"].lower() + note["title"].lower())
                if norm_ev in norm_note or norm_note in norm_ev:
                    found = True
                    break
                    
            if not found:
                missing_meetings.append((ev_date_str, ev_title, ev_start_dt.strftime("%H:%M"), ev.get("account")))
except Exception as e:
    print(f"Warning: Calendar check failed gracefully: {e}")

# 4. Format output for vault_hygiene_cron.py
lines = []

# ID Conflicts
id_conflicts = {nid: paths for nid, paths in id_to_paths.items() if len(paths) > 1}
if id_conflicts:
    lines.append("## 🔴 ID conflicts")
    for nid, paths in sorted(id_conflicts.items()):
        for p in paths:
            lines.append(f"  - {p}: id={nid} shared by {len(paths)} notes")

# Missing ID
if missing_ids:
    lines.append("\n## 🔴 Missing ID")
    for p in sorted(missing_ids):
        lines.append(f"  - {p}")

# Missing daily_note
if missing_daily_notes:
    lines.append("\n## 🔴 Missing daily_note")
    for p in sorted(missing_daily_notes):
        lines.append(f"  - {p}")

# Missing Meeting Notes
if missing_meetings:
    lines.append("\n## ⚠️ Missing meeting notes")
    for dt, title, time, acc in sorted(missing_meetings):
        lines.append(f"  - {dt} {time} | {title} ({acc})")

if lines:
    print("\n".join(lines))
else:
    print("✅ Vault looks clean — no issues found.")
