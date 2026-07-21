Hermes handles infra/skills. Defer migrations/creations to Justin.
§
Gmail (read-only): tokens under ~/.hermes/google_tokens/. Search via gws_multi.py. Do not use himalaya.
§
Obsidian vault is at `~/Developer/obsidian-vault`. Routes: `~/Developer/obsidian-vault/Notebook/Contacts/`, `~/Developer/obsidian-vault/Inputs/Daily Notes/`, `~/Developer/obsidian-vault/Notebook/`, `~/Developer/obsidian-vault/Inputs/` (Readings/Meetings/Emails/Slack/Linear), `~/Developer/obsidian-vault/Utilities/`. Layer 2 compiled Sources in `~/Developer/obsidian-vault/Notebook/`. Dividers: always `---`. Log appends to `~/Developer/obsidian-vault/Utilities/log.md`.
§
Ignore App Store Connect emails (not Justin's).
§
Justin uses Apple Notes as a "filing cabinet" for references (previously in Obsidian References/), while continuing to use Obsidian for general note-taking.
§
Google Calendar has write access; Bes can directly schedule events on Justin's behalf (e.g., during morning briefings or from forwarded emails) using gws_multi.py --account <name> calendar create.
§
New contacts to vault/Inbox/ (existing in Notebook/Contacts/ updated in place). Scraps to Inbox/. Forwarded emails to Inputs/Emails/. Inbox holds Bes-created reviews, Decisions, and Query syntheses.
§
Always query and use Telegram/cron session history (titles/summaries from state.db) as a core input when creating work logs for Justin, ensuring that all Bes/Vault development chat sessions are captured.
§
The ~/.hermes/ directory on the VM is a live runtime directory, NOT a Git repository. Never run git init or git commands inside ~/.hermes/ or its subfolders (such as ~/.hermes/skills/). The actual Git repository for system-state backups is ~/bes-backup/. Always perform git commits, pushes, and status checks inside ~/bes-backup/ instead.
§
When writing Python scripts or calling execute_code, do not attempt to import from hermes_tools mcp-specific submodules. The hermes_tools library only exposes read_file, write_file, search_files, patch, and terminal. Standard MCP tools are not importable in Python. To call external APIs (Linear, Slack, etc.) from Python scripts, make direct HTTP requests using urllib.request and the corresponding token from .env (e.g. LINEAR_API_KEY).
§
A deep semantic vault lint runs monthly via cron, reporting on orphans, stale sources, and other quality issues.
§
Linear comments and updates are captured as vault inputs when Justin reacts with a 🧠 emoji.
§
Executive summaries in Obsidian notes should be formatted as a blockquote without the Executive summary: prefix. Example: > This is the summary.
§
New `Source` notes created by the `extract-sources` skill should be named `{Original Reading Title} {YYYY-MM-DD}.md`.
§
When creating `Source` notes from `Readings`, the primary goal is synthesis, not just summarization. This involves connecting the new information to existing notes in the vault by identifying points of agreement, tension, and practical application.
§
When building solutions, prefer creating simple, single-purpose utility tools that return raw data. The workflow logic for how to use that data should reside in the skill that calls the tool, not in the tool itself.
§
When creating new Concept notes, the generated ID (YYYYMMDDHHmmss) must be appended to the end of the filename, and the files must be written to ~/Developer/obsidian-vault/Inbox/ for review.
§
Daily briefing cache for 2026-06-17 showed stale candidates (MKD-1, John Kearney) which were actually completed on June 11. Live queries verified they were already done.
§
The vault hygiene checks for Missing ID, Missing Daily Note, Ghost Links, and Orphan Notes are strictly restricted to the Notebook/ folder and its subfolders to avoid false positives from temporary directories like Inbox/ and TaskNotes/.
§
Apollo may compile Inputs -> Sources + Inbox Proposals, and may batch-apply Proposals Justin has moved into Inbox/Ready to Apply/. Apollo must not promote Thoughts/Beliefs/Decisions into Notebook, must not edit trusted Notebook outside apply's Inbox-draft rules, and must never write or move files into Ready to Apply.
§
Vault sync is handled solely by Obsidian Sync. No automatic git push/pull/commit daemon runs on ~/Developer/obsidian-vault. Git is reserved strictly for manual safety commits before major structural changes or bulk operations.