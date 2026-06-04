import os
import json
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
    
    # Calendar events
    cal_cmd = f"python3 {gws_script} --account all calendar list --start {target_date}T00:00:00 --end {tomorrow}T00:00:00 --max 50"
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
    
    out = {
        "target_date": target_date,
        "slack": slack_data,
        "linear": linear_data,
        "gws": gws_data
    }
    
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
