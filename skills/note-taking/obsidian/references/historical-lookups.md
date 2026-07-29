---
name: did-i-already-do-this
description: Look up whether Justin has already done something he may have forgotten.
triggers:
  - "did I already do X"
  - "have I done X"
  - "did I send / write / finish / complete X"
  - "did I ever X"
---

# Did I Already Do This? Or Where / When Is My Appointment?

Justin captures completed work, appointment details, and correspondence in **Obsidian**, **Gmail**, or **Google Calendar**. Check in this order:

## 1. Obsidian notes / work logs
Use the `obsidian` skill to search notes. Work logs, meeting notes, and project notes are the most likely places. Search by keyword; also check dated work log entries if a rough timeframe is known. Include filed query syntheses (`category: [[Thoughts]]` notes with `## Question` sections) as search targets.

## 2. Google Calendar & Gmail (via gws_multi.py)
When searching for bookings, appointments, confirmations, or correspondence, query the Google Workspace API:
- **Calendar Lookup:** Search for upcoming or past events across all accounts over a broad date range:
  ```bash
  python3 ~/.hermes/skills/productivity/google-workspace/scripts/gws_multi.py --account all calendar list --start <YYYY-MM-DD>T00:00:00-04:00 --end <YYYY-MM-DD>T23:59:59-04:00 --max 100
  ```
- **Gmail Correspondence Search:** Search emails for keywords like the service provider name, "appointment", "intake", "evaluation", or "portal":
  ```bash
  python3 ~/.hermes/skills/productivity/google-workspace/scripts/gws_multi.py --account all gmail search "Keywords" --max 10
  ```
- **Get Specific Email Body:** Once an email ID is found, retrieve its body or metadata for links, portals, or confirmation details:
  ```bash
  python3 ~/.hermes/skills/productivity/google-workspace/scripts/gws_multi.py --account <account> gmail get <id>
  ```

## 3. Session search (last resort)
Use `session_search` to scan past conversation transcripts. Useful if the thing was discussed or decided here but may not have been formally captured anywhere.

## Notes
- If nothing turns up in any of the three, say so plainly — don't speculate that it was done.
- If you find it, report where you found it and any relevant details (date, project, note title).
