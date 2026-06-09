---
name: bes-slack-ingest
description: Sync and ingest summarized Slack conversations into vault/Logs/Slack/ as markdown records.
version: 1.0.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [slack, obsidian, ingest, logs]
    related_skills: [obsidian, obsidian-logs, morning-briefing]
---

# Bes Slack Ingest

Captures, summarizes, and logs noteworthy Slack discussions, threads, or brain-dumps into your vault's `Logs/Slack/` folder. This prevents log pollution while keeping standard metadata connected.

## Synced Path
- `/home/justin.guest/vault/Logs/Slack/YYYY-MM-DD - Spaced Title.md`

---

## Slack Log Note Structure

Every Slack log note must start with this frontmatter format:

```yaml
---
id: 'YYYYMMDDHHmmss'                 # Numerical string based on first message's timestamp
daily_note: "[[Daily Notes/YYYY-MM-DD Weekday|YYYY-MM-DD Weekday]]" # Symmetrical daily note link
category: "[[Slack]]"                 # Quoted category link
channel: "channel-name"              # The source Slack channel
original_url: "https://slack.com/..." # Link to original discussion
participants:
  - "User A"
  - "User B"
---
```

Below the frontmatter, format the note body cleanly:
1. **Title:** Large H1 heading `# 💬 Slack Thread: [Cleaned Title]`
2. **Metadata:** Labeled key-value pairs (Channel, Date, Link, Participants)
3. **Executive Summary:** Bulleted or paragraph summary showing key discussion highlights, consensus, and action items. Do NOT copy raw text verbatim.
4. **Context & Outlines:** Bulleted log of who said what (synthesized, clean dialogue and thoughts)

---

## CLI Sync / Processing Command
To retrieve candidates and process them, the background poller runs:
- `python3 /home/justin.guest/.hermes/scripts/fetch_slack_brains.py --mark-processed <channel_id> <ts>`
