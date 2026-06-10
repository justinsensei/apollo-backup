#!/usr/bin/env python3
"""
wiki_semantic_lint_cron.py — Monthly cron wrapper for wiki_semantic_lint.py.

Runs tier-3 semantic lint and prints a Telegram-friendly summary when issues exist.
Empty stdout → no Telegram message (watchdog pattern).
"""

import subprocess
import sys
import os
import json

script = os.path.join(os.path.dirname(__file__), "wiki_semantic_lint.py")

result = subprocess.run(
    [sys.executable, script, "--json"],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    print("**Wiki semantic lint failed:**\n")
    print(result.stderr.strip() or result.stdout.strip())
    raise SystemExit(result.returncode)

try:
    data = json.loads(result.stdout)
except json.JSONDecodeError:
    print("**Wiki semantic lint failed:** invalid JSON output")
    raise SystemExit(1)

issue_count = data.get("issue_count", 0)
if issue_count == 0:
    raise SystemExit(0)

report_path = data.get("report_path", "")
lines = [
    f"**Wiki semantic lint — {data['run_at'][:10]}** ({issue_count} items)",
    "",
]

if report_path:
    lines.append(f"Full report: `{report_path}`")
    lines.append("")

for item in data.get("tier3_issues", [])[:12]:
    lines.append(f"• {item}")

remaining = len(data.get("tier3_issues", [])) - 12
if remaining > 0:
    lines.append(f"• …and {remaining} more in the vault report")

print("\n".join(lines))
