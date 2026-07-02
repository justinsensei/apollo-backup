#!/usr/bin/env python3
import subprocess
import json
import sys
import os

HERMES_HOME = os.path.expanduser("~/.hermes")
VENV_PY = os.path.join(HERMES_HOME, "hermes-agent", "venv", "bin", "python3")
SCRIPTS_DIR = os.path.join(HERMES_HOME, "scripts")

def run_script(script_name, args=None):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    cmd = [VENV_PY, script_path]
    if args:
        cmd.extend(args)
    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        if res.returncode != 0:
            sys.stderr.write(f"Error running {script_name} {' '.join(args or [])} (rc={res.returncode}): {res.stderr}\n")
            return None
        
        out = res.stdout.strip()
        if not out:
            return []
        try:
            return json.loads(out)
        except json.JSONDecodeError as e:
            sys.stderr.write(f"Error decoding JSON from {script_name}: {e}\nRaw output: {out}\n")
            return None
    except Exception as e:
        sys.stderr.write(f"Exception running {script_name}: {e}\n")
        return None

def main():
    failed = []
    
    # Fetch Slack brains
    slack_brains = run_script("fetch_slack_brains.py")
    if slack_brains is None:
        failed.append("Slack (fetch_slack_brains.py)")
        slack_brains = []
    
    # Fetch Linear brains
    linear_brains = run_script("fetch_linear_brains.py")
    if linear_brains is None:
        failed.append("Linear (fetch_linear_brains.py)")
        linear_brains = []
    
    # Fetch Gmail/Apollo Inbox forwards
    email_brains = run_script("poll_apollo_inbox.py", ["--json"])
    if email_brains is None:
        failed.append("Email/Apollo Inbox (poll_apollo_inbox.py)")
        email_brains = []
    
    # Fetch Telegram brains
    telegram_brains = run_script("fetch_telegram_brains.py")
    if telegram_brains is None:
        failed.append("Telegram (fetch_telegram_brains.py)")
        telegram_brains = []
    
    # Output unified dict
    unified = {
        "slack": slack_brains,
        "linear": linear_brains,
        "emails": email_brains,
        "telegram": telegram_brains
    }
    print(json.dumps(unified, indent=2))
    
    if failed:
        sys.stderr.write(f"CRITICAL: Failed to ingest from: {', '.join(failed)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
