#!/usr/bin/env python3
"""
Sync Apple Reminders to Obsidian Daily Note Scratchpad.
Runs on the host (where remindctl and interactive TCC permissions work perfectly),
and writes directly into the Obsidian Daily Note inside bes-vm via SSH.

Designed to be run as a cron job on the host.
"""

import datetime as dt
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

# Target Reminders List Configuration
# Default is "Reminders ⚠️" (223B68FA-6463-41AD-8B13-069CC61E821B)
# But can be customized to "Inbox" (38822AAB-CD3F-46BD-99E0-407AEAE12F93) or any list.
SOURCE_LIST_ID = "223B68FA-6463-41AD-8B13-069CC61E821B"  # "Reminders ⚠️"
REMINDCTL = "/opt/homebrew/bin/remindctl"


def log(msg: str) -> None:
    print(f"[sync-reminders-to-obsidian] {msg}", file=sys.stderr)


def fetch_active_reminders() -> list[dict]:
    """Fetch uncompleted reminders from the specified list on the host."""
    try:
        res = subprocess.run(
            [REMINDCTL, "all", "--json"],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        all_reminders = json.loads(res.stdout)
    except FileNotFoundError:
        log(f"ERROR: remindctl not found at {REMINDCTL}")
        sys.exit(2)
    except subprocess.CalledProcessError as e:
        log(f"ERROR: remindctl failed: {e.stderr.strip()}")
        sys.exit(2)
    except Exception as e:
        log(f"ERROR: failed to fetch reminders: {e}")
        sys.exit(2)

    return [
        r for r in all_reminders
        if r.get("listID") == SOURCE_LIST_ID and not r.get("isCompleted", False)
    ]


def ensure_daily_note_exists() -> None:
    """Trigger create_daily_note.py inside bes-vm via SSH."""
    try:
        subprocess.run(
            ["ssh", "bes-vm", "python3 ~/.hermes/scripts/create_daily_note.py"],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        log(f"ERROR: failed to ensure daily note exists on VM: {e.stderr.strip()}")
        sys.exit(2)


def read_remote_note(remote_path: str) -> str:
    """Read the content of today's Daily Note from bes-vm."""
    try:
        res = subprocess.run(
            ["ssh", "bes-vm", f"cat {shlex.quote(remote_path)}"],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        return res.stdout
    except subprocess.CalledProcessError as e:
        log(f"ERROR: failed to read remote Daily Note: {e.stderr.strip()}")
        sys.exit(2)


def write_remote_note(remote_path: str, content: str) -> None:
    """Write updated content back to the Daily Note on bes-vm using stdin."""
    try:
        cmd = [
            "ssh",
            "bes-vm",
            f"python3 -c \"import sys; open({repr(remote_path)}, 'w').write(sys.stdin.read())\"",
        ]
        res = subprocess.run(cmd, input=content, capture_output=True, text=True, timeout=30)
        if res.returncode != 0:
            log(f"ERROR: failed to write remote Daily Note: {res.stderr.strip()}")
            sys.exit(2)
    except Exception as e:
        log(f"ERROR: failed to write remote Daily Note: {e}")
        sys.exit(2)


def complete_reminder_locally(reminder_id: str) -> bool:
    """Complete a reminder on the host."""
    try:
        res = subprocess.run(
            [REMINDCTL, "complete", reminder_id, "--quiet"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return res.returncode == 0
    except Exception as e:
        log(f"WARNING: failed to complete reminder {reminder_id}: {e}")
        return False


def insert_reminders_to_scratchpad(content: str, reminders: list[dict]) -> tuple[str, list[str]]:
    """Insert reminders into # ✅ Tasks section of the global Scratchpad.md as - [ ] Title."""
    reminders_to_add = []
    synced_titles = []

    for r in reminders:
        title = r["title"]
        notes = r.get("notes", "").strip()
        
        # Format as - [ ] Title
        item_str = f"- [ ] {title}"
        reminders_to_add.append(item_str)
        synced_titles.append(title)
        
        if notes:
            for note_line in notes.splitlines():
                if note_line.strip():
                    reminders_to_add.append(f"\t- {note_line.strip()}")

    lines = content.splitlines()
    tasks_idx = -1
    next_header_idx = -1

    for idx, line in enumerate(lines):
        if line.strip().startswith("# ✅ Tasks"):
            tasks_idx = idx
            break

    if tasks_idx == -1:
        # If Tasks section doesn't exist, prepend it
        lines.insert(0, "# ✅ Tasks")
        tasks_idx = 0

    for idx in range(tasks_idx + 1, len(lines)):
        if lines[idx].strip().startswith("#"):
            next_header_idx = idx
            break

    if next_header_idx != -1:
        tasks_lines = lines[tasks_idx + 1 : next_header_idx]
    else:
        tasks_lines = lines[tasks_idx + 1 :]

    cleaned_tasks_lines = []
    for line in tasks_lines:
        if "<% tp.file.cursor(1) %>" in line:
            continue
        cleaned_tasks_lines.append(line)

    # Trim leading empty lines from existing tasks
    while cleaned_tasks_lines and not cleaned_tasks_lines[0].strip():
        cleaned_tasks_lines.pop(0)

    # Trim trailing empty lines from existing tasks
    while cleaned_tasks_lines and not cleaned_tasks_lines[-1].strip():
        cleaned_tasks_lines.pop()

    # Append new reminders (no leading line break before them)
    for item in reminders_to_add:
        cleaned_tasks_lines.append(item)

    # Trim trailing empty lines from the finalized tasks block
    while cleaned_tasks_lines and not cleaned_tasks_lines[-1].strip():
        cleaned_tasks_lines.pop()

    new_tasks_block = []
    # Ensure clean spacing around the tasks block
    if cleaned_tasks_lines:
        new_tasks_block.append("")
        new_tasks_block.extend(cleaned_tasks_lines)
        new_tasks_block.append("")

    if next_header_idx != -1:
        result_lines = lines[:tasks_idx + 1] + new_tasks_block + lines[next_header_idx:]
    else:
        result_lines = lines[:tasks_idx + 1] + new_tasks_block

    return "\n".join(result_lines), synced_titles


def main() -> int:
    active = fetch_active_reminders()
    if not active:
        # Silent when there is no work to do
        return 0

    log(f"Found {len(active)} reminders to sync.")

    # Get the file path for the global Scratchpad note in the Inbox
    remote_path = "/home/justin.guest/Developer/obsidian-vault/Inbox/Scratchpad.md"

    # Read, modify, and write back
    content = read_remote_note(remote_path)
    new_content, synced_titles = insert_reminders_to_scratchpad(content, active)
    write_remote_note(remote_path, new_content)

    log("Successfully appended reminders to Scratchpad.md inside VM.")

    # Complete the reminders locally
    completed_count = 0
    for r in active:
        rid = r["id"]
        title = r["title"]
        if complete_reminder_locally(rid):
            completed_count += 1
            log(f"Completed local reminder: {title}")
        else:
            log(f"Failed to complete local reminder: {title}")

    print(f"Synced {completed_count}/{len(active)} reminders to Obsidian Scratchpad.md:")
    for title in synced_titles:
        print(f"  • {title}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
