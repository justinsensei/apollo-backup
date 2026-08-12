# Slack User-Token API Reference

Operate Justin's Slack workspace (SignLab) via user-token (`xoxp-`) API.

## Auth & Posture
- Auth: `SLACK_USER_TOKEN` (`xoxp-...`)
- Posts appear as Justin himself. Default to read-only operations unless requested or approved.
- Scopes: channels/groups/im/mpim history+read, users:read, search:read, files:read, reactions:read, chat:write, reactions:write.

## CLI Wrapper
Use `scripts/slack.py`:
- `slack whoami`: Test auth identity
- `slack channels [--type public|private|im|mpim|all]`: List conversations
- `slack read <channel_id> [--since 24h|2d] [--text]`: Fetch recent messages
- `slack thread <channel_id> <thread_ts> [--text]`: Fetch thread replies
- `slack search '<query>'`: Search messages
- `slack post <channel_id> "<text>" [--thread <ts>]`: Post message
- `slack react <channel_id> <ts> <emoji>`: Add reaction

## Automated Brain Log Capture (`🧠`)
When Justin reacts to a Slack message with `🧠`:
- `scripts/fetch_slack_brains.py` detects reacted messages.
- Synthesizes thread context or 11-message window into `Inputs/Slack/YYYY-MM-DD-slug.md` in Obsidian vault.
- Marks thread processed in `~/.hermes/processed_slack_brains.json`.
