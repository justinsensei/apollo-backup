Hermes handles infrastructure & skill management for Justin's agents. Defer skill migration/creation tasks to him.
§
Email: read Gmail via Google OAuth. Tokens at `~/.hermes/google_tokens/{work,personal-main,personal-junk}.json`. Cross-account wrapper: `python3 ~/.hermes/skills/productivity/google-workspace/scripts/gws_multi.py --account all|<name>|<csv> gmail search "..." --max N`. Single-account: set `HERMES_GOOGLE_TOKEN_FILE` and call `google_api.py`. Read-only. Do NOT use himalaya.
§
Obsidian uses a flatter structure: people and companies live in contacts/; concepts and projects live in notes/. Meetings (meetings/) and daily notes (daily/) remain separate. Frontmatter 'type' overrides are used to enforce gbrain page types.
§
App Store Connect issue emails are not Justin's to handle — ignore them when capturing action items from email.
§
Todoist is for actions only — no informational notes or FYIs. If something isn't actionable, don't capture it.
§
During inbox fills, Justin does not want generic meeting prep tasks suggested. Exclude standard team/internal syncs and brief chat slots unless explicit prep is required.
§
During inbox fills, do not suggest any task for a Linear issue if any existing Todoist task already references or is linked to that same issue ID.
§
Justin uses Apple Notes as a "filing cabinet" for references (previously in Obsidian References/), while continuing to use Obsidian for general note-taking.
§
Google Calendar has write access; Bes can directly schedule events on Justin's behalf (e.g., during morning briefings or from forwarded emails) using `gws_multi.py --account <name> calendar create` instead of creating 'Add to calendar' tasks in Todoist.
§
Vault hygiene ignores Copilot/Granola logs. Granola notes sync directly to /meetings and are auto-reconciled in-place via reconcile_granola.py.
§
Forwarded emails should not be copied to vault unless explicitly requested.
§
Obsidian horizontal rule: always use three hyphens `---` for a horizontal line, never two hyphens `--`.
§
Readwise script is at `~/sync_readwise.py`. It exports highlights tagged 'vault' (case-insensitive) to `vault/sources/` and runs `gbrain sync`.