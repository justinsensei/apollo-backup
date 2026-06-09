Hermes handles infra/skills. Defer migrations/creations to Justin.
§
Gmail (read-only): tokens under ~/.hermes/google_tokens/. Search via gws_multi.py. Do not use himalaya.
§
Obsidian routes: Contacts/, Notes/, Logs/ (Meetings/Emails/Slack/Sources), Daily Notes/ (Tier 1 log input), Utilities/. Dividers: always `---`.
§
App Store Connect issue emails are not Justin's to handle — ignore them when capturing action items from email.
§
Todoist is for actions only — no informational notes or FYIs. If something isn't actionable, don't capture it.
§
Inbox fills: exclude generic meeting prep/internal syncs, and do not suggest tasks for Linear issues already linked/referenced in Todoist.
§
Justin uses Apple Notes as a "filing cabinet" for references (previously in Obsidian References/), while continuing to use Obsidian for general note-taking.
§
Google Calendar has write access; Bes can directly schedule events on Justin's behalf (e.g., during morning briefings or from forwarded emails) using `gws_multi.py --account <name> calendar create` instead of creating 'Add to calendar' tasks in Todoist.
§
Granola notes sync to meetings/ and are reconciled and moved to Logs/Meetings/ via vault_hygiene.py.
§
Forwarded emails should not be copied to vault unless explicitly requested.
§
Readwise script is at ~/sync_readwise.py. It exports highlights tagged 'vault' (case-insensitive) to vault/Logs/Sources/.
§
User prefers modular, composable skills (no monolithic files).
§
Default new conceptual notes to category 'Notes' (with timestamp ID) unless triaged. When promoting notes to 'Concepts', ensure they have a direct source link and check for duplicate files first to prevent redundancies.
§
Vault convention: Raw notes can contain embedded processing instructions directed at Bes using inline tasks ("- [ ] @bes <task>") or comment blocks ("%% bes-instructions ... %%").
§
Weekly summaries are requested manually on the first day of the week and delivered directly to the requesting Telegram conversation instead of running on a schedule.