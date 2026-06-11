import os
import json
import sqlite3
import subprocess
import urllib.request
from datetime import datetime, timedelta

def load_env():
    env = {}
    env_path = os.path.expanduser('~/.hermes/.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.strip().startswith('#') and '=' in line:
                    k, v = line.strip().split('=', 1)
                    env[k.strip()] = v.strip()
    return env

def get_target_date():
    # If TARGET_DATE is in environment, use it; otherwise default to yesterday
    target_date = os.environ.get('TARGET_DATE')
    if not target_date:
        yesterday = datetime.now() - timedelta(days=1)
        target_date = yesterday.strftime('%Y-%m-%d')
    return target_date

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            return json.loads(res.stdout)
        else:
            return {"error": res.stderr}
    except Exception as e:
        return {"error": str(e)}

def fetch_slack(target_date):
    # Calculate slack date limits (TARGET_DATE - 1 and TARGET_DATE + 1)
    t_dt = datetime.strptime(target_date, '%Y-%m-%d')
    after_date = (t_dt - timedelta(days=1)).strftime('%Y-%m-%d')
    before_date = (t_dt + timedelta(days=1)).strftime('%Y-%m-%d')
    
    slack_script = os.path.expanduser('~/.hermes/skills/social-media/slack/scripts/slack.py')
    
    # Query messages sent from @justin
    cmd_from = f"python3 {slack_script} search 'from:@justin after:{after_date} before:{before_date}' --limit 50"
    from_msgs = run_cmd(cmd_from)
    
    # Query messages addressed to @justin
    cmd_to = f"python3 {slack_script} search 'to:@justin after:{after_date} before:{before_date}' --limit 50"
    to_msgs = run_cmd(cmd_to)
    
    return {
        "from_msgs": from_msgs,
        "to_msgs": to_msgs
    }

def fetch_linear(target_date, api_key, user_id):
    if not api_key:
        return {"error": "Missing Linear API key"}
        
    t_dt = datetime.strptime(target_date, '%Y-%m-%d')
    tomorrow = (t_dt + timedelta(days=1)).strftime('%Y-%m-%d')
    
    query = """
    {
      issues(filter: {
        and: [
          { updatedAt: { gte: "%sT00:00:00.000Z", lt: "%sT00:00:00.000Z" } },
          { or: [
            { assignee: { id: { eq: "%s" } } },
            { creator:  { id: { eq: "%s" } } },
            { subscribers: { id: { eq: "%s" } } }
          ] }
        ]
      }, first: 50) {
        nodes {
          identifier
          title
          state { name type }
          updatedAt
          assignee { name }
          creator { name }
          team { key }
          url
          comments(filter: { createdAt: { gte: "%sT00:00:00.000Z" } }) {
            nodes {
              body
              user { name }
            }
          }
        }
      }
    }
    """ % (target_date, tomorrow, user_id, user_id, user_id, target_date)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }
    
    req = urllib.request.Request(
        "https://api.linear.app/graphql", 
        data=json.dumps({"query": query}).encode('utf-8'), 
        headers=headers
    )
    
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

def fetch_gws(target_date):
    gws_script = os.path.expanduser('~/.hermes/skills/productivity/google-workspace/scripts/gws_multi.py')
    t_dt = datetime.strptime(target_date, '%Y-%m-%d')
    tomorrow = (t_dt + timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Get local timezone offset dynamically (e.g. -04:00 or -05:00)
    local_offset = datetime.now().astimezone().strftime('%z')
    formatted_offset = f"{local_offset[:-2]}:{local_offset[-2:]}" if local_offset else "Z"
    
    # Calendar events with proper local timezone offset
    cal_cmd = f"python3 {gws_script} --account all calendar list --start {target_date}T00:00:00{formatted_offset} --end {tomorrow}T00:00:00{formatted_offset} --max 50"
    calendar_events = run_cmd(cal_cmd)
    
    # Gmail search (requires slashes)
    date_slash = t_dt.strftime('%Y/%m/%d')
    tomorrow_slash = (t_dt + timedelta(days=1)).strftime('%Y/%m/%d')
    
    work_mail_cmd = f"python3 {gws_script} --account work gmail search 'after:{date_slash} before:{tomorrow_slash}' --max 50"
    personal_mail_cmd = f"python3 {gws_script} --account personal-main gmail search 'after:{date_slash} before:{tomorrow_slash}' --max 50"
    
    return {
        "calendar": calendar_events,
        "gmail_work": run_cmd(work_mail_cmd),
        "gmail_personal": run_cmd(personal_mail_cmd)
    }

def fetch_vault_git(target_date):
    vault_path = os.environ.get('OBSIDIAN_VAULT_PATH', os.path.expanduser('~/vault'))
    if not os.path.exists(vault_path) or not os.path.exists(os.path.join(vault_path, '.git')):
        return {"error": f"Vault path {vault_path} is not a git repository or does not exist."}
    
    cmd = f"git log --since='{target_date} 00:00:00' --until='{target_date} 23:59:59' --name-status --pretty=format:'COMMIT:%h|%an|%s'"
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=vault_path)
        if res.returncode != 0:
            return {"error": res.stderr}
        
        lines = res.stdout.split('\n')
        commits = []
        current_commit = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('COMMIT:'):
                parts = line[7:].split('|')
                h = parts[0]
                an = parts[1] if len(parts) > 1 else ''
                s = parts[2] if len(parts) > 2 else ''
                is_justin = 'bes' not in an.lower()
                current_commit = {
                    "hash": h,
                    "author": an,
                    "subject": s,
                    "is_justin": is_justin,
                    "files": []
                }
                commits.append(current_commit)
            elif current_commit and current_commit["is_justin"]:
                parts = line.split('\t')
                if len(parts) >= 2:
                    status = parts[0]
                    if status.startswith('R') and len(parts) >= 3:
                        current_commit["files"].append({
                            "status": 'R',
                            "old_path": parts[1],
                            "path": parts[2]
                        })
                    else:
                        current_commit["files"].append({
                            "status": status,
                            "path": parts[1]
                        })
        
        added_files = set()
        modified_files = set()
        deleted_files = set()
        
        for commit in commits:
            if not commit["is_justin"]:
                continue
            for f in commit["files"]:
                status = f["status"][0]
                if status == 'A':
                    added_files.add(f["path"])
                elif status == 'M':
                    modified_files.add(f["path"])
                elif status == 'D':
                    deleted_files.add(f["path"])
                elif status == 'R':
                    deleted_files.add(f["old_path"])
                    added_files.add(f["path"])
                    
        return {
            "commits_count": len([c for c in commits if c["is_justin"]]),
            "added": list(added_files),
            "modified": list(modified_files - added_files),
            "deleted": list(deleted_files)
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    env = load_env()
    # Inject variables to environment for child processes
    for k, v in env.items():
        os.environ[k] = v
        
    target_date = get_target_date()
    print(f"Target Date: {target_date}")
    
    slack_data = fetch_slack(target_date)
    linear_data = fetch_linear(target_date, env.get('LINEAR_API_KEY'), env.get('LINEAR_USER_ID', '211987db-f790-4bfa-8c8e-518e1f704901'))
    gws_data = fetch_gws(target_date)
    vault_git_data = fetch_vault_git(target_date)
    
    out = {
        "target_date": target_date,
        "slack": slack_data,
        "linear": linear_data,
        "gws": gws_data,
        "vault_git": vault_git_data
    }
    
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
