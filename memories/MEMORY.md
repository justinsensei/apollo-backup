Hermes handles infra/skills. Defer migrations/creations to Justin.
§
Gmail (read-only): tokens under ~/.hermes/google_tokens/. Search via gws_multi.py. Do not use himalaya.
§
Obsidian routes: Notes/Contacts/, Notes/Daily Notes/, Notes/, Inputs/ (Readings/Meetings/Emails/Slack/Linear), Utilities/. Layer 2 compiled Sources in Notes/. Dividers: always `---`. Log appends to Utilities/log.md.
§
Ignore App Store Connect emails (not Justin's).
§
Todoist rules: Actions only. Inbox fills exclude generic prep, iMessage, archived mail, Linear Triage/Backlog/Completed/Canceled, and items already in Todoist.
§
Justin uses Apple Notes as a "filing cabinet" for references (previously in Obsidian References/), while continuing to use Obsidian for general note-taking.
§
Google Calendar has write access; Bes can directly schedule events on Justin's behalf (e.g., during morning briefings or from forwarded emails) using `gws_multi.py --account <name> calendar create` instead of creating 'Add to calendar' tasks in Todoist.
§
New contacts to vault/inbox/ (existing in Notes/Contacts/ updated in place). Scraps to inbox/. Forwarded emails to Inputs/Emails/. Inbox holds Bes-created reviews, Decisions, and Query syntheses.
§
Timelines are disabled in favor of native Backlinks. check_vault_signals.py is read-only, and integrate_entities.py only updates project State on decisions.
§
Tier-3 semantic lint (`wiki_semantic_lint.py`) runs monthly (1st, 8am cron `a3f8c2e91b04`). Report-only — orphans (inbound), stale Sources, promotion gaps, contradiction candidates. State: `~/.hermes/state/semantic_lint_last.json`. Structural lint stays in `vault_hygiene.py`.
§
Linear capture: Poller fetch_linear_brains.py queries comments and updates with obsidian_jg or 🧠 reaction by Justin. Ingested notes save under vault/inbox/ as Inputs/Linear.
§
Obsidian frontmatter category links (e.g., [[People]]) must be double-quoted (e.g., "[[People]]").
§
Always query and use Telegram/cron session history (titles/summaries from state.db) as a core input when creating work logs for Justin, ensuring that all Bes/Vault development chat sessions are captured.
§
The ~/.hermes/ directory on the VM is a live runtime directory, NOT a Git repository. Never run git init or git commands inside ~/.hermes/ or its subfolders (such as ~/.hermes/skills/). The actual Git repository for system-state backups is ~/bes-backup/. Always perform git commits, pushes, and status checks inside ~/bes-backup/ instead.
