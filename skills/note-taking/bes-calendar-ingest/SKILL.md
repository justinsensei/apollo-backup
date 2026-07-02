---
name: bes-calendar-ingest
description: Sync, query, and ingest calendar events from Google Calendar (work and personal) to drive daily schedule planning and automated work logs.
version: 1.0.0
author: Bes
license: MIT
metadata:
  hermes:
    tags: [calendar, google-workspace, ingest, logs]
    related_skills: [google-workspace, work-log, morning-briefing, wind-down]
---

# Bes Calendar Ingest

Handles Google Calendar syncs across all of your accounts (work, personal-main, personal-junk) to drive schedule-planning, morning briefings, and automated work log accomplishments.

## Credentials & Tokens
- Tokens are located at: `~/.hermes/google_tokens/{work,personal-main,personal-junk}.json`
- Wrapped in the cross-account script: `~/.hermes/skills/productivity/google-workspace/scripts/gws_multi.py`

---

## Querying Schedule (Read-Only)

To retrieve schedule events for a specific timeframe (e.g. today or tomorrow):
```bash
python3 ~/.hermes/skills/productivity/google-workspace/scripts/gws_multi.py --account all calendar list --start <YYYY-MM-DD>T00:00:00<OFFSET> --end <YYYY-MM-DD>T23:59:59<OFFSET> --max 50
```

This schedule feeds directly into:
1. **Today's Daily Note:** Populates `## 📅 Schedule & Events`.
2. **Morning Briefing:** Drives the active schedule briefing.
3. **Daily Work Log:** Compiles and reconciles meeting attendances.

---

## Scheduling Events (Write Access)

Bes has write access to Google Calendar. You can directly schedule events on Justin's behalf (e.g., during briefings or from forwarded email instructions) rather than creating tasks in Todoist:
```bash
python3 ~/.hermes/skills/productivity/google-workspace/scripts/gws_multi.py --account work|personal-main calendar create --summary "Event Title" --start "2026-06-09T14:00:00" --end "2026-06-09T15:00:00" --description "Context..."
```
*Note: Specify the single correct target account; do not use `--account all` for write operations.*

---

## Handling Vacation & Meeting Cancellations

When Justin informs you that he is taking a day off, has cancelled work meetings, or is on vacation through a specific date, you must actively update the environment:

1. **Calculate Weekdays:** Determine the list of weekdays (Monday–Friday) between today and the specified target date.
2. **Update Days-Off Config:** Append these dates (in `YYYY-MM-DD` format, one per line) to `~/.hermes/days-off.txt`. This ensures the work-day checking system (`work_day.py`) evaluates them as non-work days, setting `is_work_day: False` and skipping work log reviewer warnings.
3. **Patch Daily Notes:**
   - Locate the daily notes in `~/Developer/obsidian-vault/Daily Notes/` for the affected dates.
   - Update the top `Preview Summary` blockquote to note the cancellation/vacation.
   - Under `## 🗓 Schedule & Events`, cross out the cancelled work meetings using strike-through syntax (e.g., `~~Meeting Name~~`) and append `— *Cancelled*`.
4. **Regenerate Briefing Cache:** Execute the morning cache compilation script:
   ```bash
   python3 ~/.hermes/scripts/generate_morning_cache.py
   ```
   Verify that the output confirms `Is Work Day: False, Work Log Status: skipped`.
5. **Audit Live Calendar Discrepancies:** Run a live Google Calendar query for the cancellation range. If meetings remain with `status: "confirmed"`, report the discrepancy clearly to Justin and ask if he wants you to delete them on his behalf.

