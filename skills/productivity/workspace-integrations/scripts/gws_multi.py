#!/usr/bin/env python3
"""Cross-account wrapper for the google-workspace skill.

Drives the underlying google_api.py once per registered account, tags each
returned record with its `account: <name>` source, and either lists them
per-account or merges them into a single result set.

USAGE
─────

  # List which accounts are registered (have a valid token)
  $GWS_MULTI accounts

  # Run a single command against a single account (explicit)
  $GWS_MULTI --account work gmail search "is:unread newer_than:1d" --max 5

  # Extract one field as raw text — avoids `| python3 -c` and `| jq`
  $GWS_MULTI --account personal-main gmail get MSG_ID --field body --max-len 2000

  # Run against ALL registered accounts and merge results
  $GWS_MULTI --account all gmail search "is:unread newer_than:1d" --max 5
  $GWS_MULTI --account all calendar list

  # Run against a comma-separated subset
  $GWS_MULTI --account work,personal-main calendar list

Each output row gets an `account` field added (or, when the underlying response
isn't a list of objects, the response is wrapped as
  {"account": "<name>", "data": <raw>}).

Per-account errors don't abort the whole run — they're collected and reported
in a top-level `_errors` field on the merged JSON output.

DESIGN
──────

This is a thin wrapper. The underlying google_api.py and setup.py do the real
work — this script just sets GOOGLE_ACCOUNT in env and invokes them as
subprocesses, then merges JSON output. Keeps the multi-account logic
contained in one small file that's easy to read and audit.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# Resolve sibling scripts robustly
SCRIPTS_DIR = Path(__file__).resolve().parent
GOOGLE_API_PY = SCRIPTS_DIR / "google_api.py"
SETUP_PY = SCRIPTS_DIR / "setup.py"

HERMES_HOME = Path(os.environ.get("HERMES_HOME") or (Path.home() / ".hermes"))
TOKENS_DIR = HERMES_HOME / "google_tokens"


def list_registered_accounts() -> list[str]:
    """Return account names that have a token file."""
    if not TOKENS_DIR.exists():
        # Could still have a legacy token at ~/.hermes/google_token.json
        if (HERMES_HOME / "google_token.json").exists():
            return ["work"]  # treat legacy as the work account
        return []
    return sorted(p.stem for p in TOKENS_DIR.glob("*.json"))


def account_token_path(account: str) -> Path:
    return TOKENS_DIR / f"{account}.json"


def check_account_auth(account: str) -> bool:
    """Return True if the account's token is currently valid (or refreshable)."""
    env = {**os.environ, "GOOGLE_ACCOUNT": account}
    result = subprocess.run(
        [sys.executable, str(SETUP_PY), "--check"],
        env=env,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def run_for_account(account: str, passthrough_args: list[str]) -> tuple[int, str, str]:
    """Invoke google_api.py with GOOGLE_ACCOUNT=<account>. Returns (rc, stdout, stderr)."""
    env = {**os.environ, "GOOGLE_ACCOUNT": account}
    result = subprocess.run(
        [sys.executable, str(GOOGLE_API_PY)] + passthrough_args,
        env=env,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def tag_records(raw_output: str, account: str):
    """Try to parse the JSON output and tag with `account`. Returns parsed value or {"account": ..., "raw": ...}."""
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        return {"account": account, "raw": raw_output.strip()}
    if isinstance(data, list):
        for row in data:
            if isinstance(row, dict):
                row["account"] = account
        return data
    if isinstance(data, dict):
        # Single-record response (e.g. gmail get) — add account key
        data["account"] = account
        return data
    return {"account": account, "data": data}


def main():
    parser = argparse.ArgumentParser(
        description="Cross-account wrapper for google-workspace skill.",
        add_help=False,
    )
    parser.add_argument(
        "--account",
        default="",
        help="Account name(s): 'work', 'personal-main', comma-separated, or 'all'. "
        "Omit to use the legacy single-token path.",
    )
    parser.add_argument(
        "--help",
        "-h",
        action="store_true",
        help="Show this help message and exit.",
    )
    args, passthrough = parser.parse_known_args()

    if args.help:
        parser.print_help()
        print()
        print("Pass-through arguments are forwarded to google_api.py — see its help:")
        print(f"  {GOOGLE_API_PY} --help")
        sys.exit(0)

    # Bookkeeping subcommand: "accounts" (list registered accounts)
    if passthrough and passthrough[0] == "accounts":
        registered = list_registered_accounts()
        if not registered:
            print(json.dumps({"accounts": [], "note": "No accounts registered yet."}, indent=2))
            sys.exit(0)
        out = []
        for acct in registered:
            valid = check_account_auth(acct)
            out.append({"account": acct, "auth_valid": valid})
        print(json.dumps({"accounts": out}, indent=2))
        sys.exit(0)

    # Resolve target accounts
    if args.account == "all":
        targets = list_registered_accounts()
        if not targets:
            print("ERROR: --account all requested but no accounts registered yet.", file=sys.stderr)
            sys.exit(2)
    elif args.account:
        targets = [a.strip() for a in args.account.split(",") if a.strip()]
    else:
        # No --account flag → legacy single-token path (no GOOGLE_ACCOUNT env injection)
        result = subprocess.run(
            [sys.executable, str(GOOGLE_API_PY)] + passthrough,
            capture_output=False,
        )
        sys.exit(result.returncode)

    # Fan out across targets, collect results
    merged_results = []
    errors = []
    single_record_results = []

    # Detect raw-text mode (passthrough opted out of JSON via e.g. --field).
    # In that case, don't try to parse stdout as JSON — emit it as-is, with a
    # per-account header when fanning out to multiple accounts. This makes the
    # `gmail get --field body` pattern work cleanly through the multi-account
    # wrapper without forcing the caller to pipe through python or jq.
    raw_text_mode = "--field" in passthrough

    if raw_text_mode:
        multi = len(targets) > 1
        any_ok = False
        for account in targets:
            rc, stdout, stderr = run_for_account(account, passthrough)
            if rc != 0:
                errors.append(
                    {
                        "account": account,
                        "exit_code": rc,
                        "stderr": stderr.strip()[:500] or stdout.strip()[:500],
                    }
                )
                if multi:
                    print(f"=== {account} (ERROR rc={rc}) ===", file=sys.stderr)
                    print(stderr.strip()[:500] or stdout.strip()[:500], file=sys.stderr)
                continue
            any_ok = True
            if multi:
                print(f"=== {account} ===")
            sys.stdout.write(stdout)
            if not stdout.endswith("\n"):
                sys.stdout.write("\n")
        if errors and not any_ok:
            sys.exit(1)
        sys.exit(0)

    for account in targets:
        rc, stdout, stderr = run_for_account(account, passthrough)
        if rc != 0:
            errors.append(
                {
                    "account": account,
                    "exit_code": rc,
                    "stderr": stderr.strip()[:500] or stdout.strip()[:500],
                }
            )
            continue
        tagged = tag_records(stdout, account)
        if isinstance(tagged, list):
            merged_results.extend(tagged)
        else:
            single_record_results.append(tagged)

    # If passthrough included no JSON-producing command at all, just pass stdout through
    if not merged_results and not single_record_results and not errors:
        sys.exit(0)

    # Build the merged output
    if single_record_results and not merged_results:
        # Single-record responses across accounts -> emit as a list
        output = single_record_results
    else:
        output = merged_results
        # If there are also single-record entries (mixed responses), append them
        if single_record_results:
            output.extend(single_record_results)

    if errors:
        # Wrap output to attach error info without losing data
        envelope = {"_errors": errors, "results": output}
        print(json.dumps(envelope, indent=2))
        # Non-zero exit only if EVERY account errored
        sys.exit(1 if not output else 0)
    else:
        print(json.dumps(output, indent=2))
        sys.exit(0)


if __name__ == "__main__":
    main()
