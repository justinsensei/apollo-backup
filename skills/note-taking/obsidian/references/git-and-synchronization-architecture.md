# Git and Synchronization Architecture

This reference document outlines the exact architecture, scripts, and behaviors for Justin's Hermes / Apollo VM and the Obsidian vault.

---

## 1. Obsidian Vault — Sync Contract (LOCKED 2026-08-24)

**Live sync plane: Obsidian Sync only.**
**GitHub: cold history / intentional rollbacks only — never a second sync plane.**

| Layer | Job | Who writes |
|---|---|---|
| **Obsidian Sync** | Live truth across Mac + Apollo (+ phone) | Continuous file sync |
| **GitHub (`obsidian-vault`)** | Large-grain restore points | Justin on Mac only, intentional commits |

### Hard rules (Apollo / Hermes must obey)

1. **Do not** `git add`, `git commit`, `git push`, `git pull`, or `git fetch` in `/home/justin.guest/Developer/obsidian-vault`.
2. **Do not** start, enable, or reinstall `apollo-vault-sync`, `apollo-vault-backup`, or any other vault auto-git / nightly checkpoint service.
3. Wait for **Obsidian Sync** when a referenced note is missing on disk. If still missing, report that — do not invent a git sync workaround.
4. At most **one** writer to `origin/main` for the vault: Justin's Mac. Apollo is never that writer.
5. Syncthing is **not** part of the vault sync story (retired). Do not reintroduce it for `obsidian-vault`.

### Disabled services (must stay off)

```bash
systemctl --user stop apollo-vault-sync apollo-vault-backup
systemctl --user disable apollo-vault-sync apollo-vault-backup
# Confirm:
systemctl --user is-enabled apollo-vault-sync apollo-vault-backup
systemctl --user is-active apollo-vault-sync apollo-vault-backup
```

Expected: `disabled` / `inactive` (or `not-found`). If either is active, stop/disable immediately and alert Justin.

### Git on the Mac (Justin only)

- Manual safety commits before bulk/risky work, e.g. `safety: before meeting sibling cleanup`.
- Optional sparse checkpoints (weekly) from **one** machine — never from Apollo.
- Obsidian Git plugin: installed but **disabled**; auto-backup / auto-pull / auto-push off (`autoSaveInterval: 0`, `autoBackupAfterFileChange: false`, `autoPullOnBoot: false`, `disablePush: true`).

### Why this exists (do not regress)

Auto-git on the vault fights apply/archive and Sync:

- **2026-08-13:** `apollo-vault-sync` commit `fa51031a5` renamed applied Proposals `Utilities/Review/` → `Inbox/Proposals/` and dropped apply creates from HEAD (sync ghosts).
- **2026-08-15+:** `apollo-vault-backup` nightly checkpoints re-added Inbox Proposal/Notes ghosts and Granola meeting siblings from a divergent VM tree.

Any commit with subject `apollo: …` / `backup: daily vault checkpoint` / message `Auto-committed by apollo-vault-*` is a **regression**. Stop the service; do not treat those commits as valid sync.

Vault pointer: [[Vault sync contract Obsidian Sync primary 20260824164801]]

### Paths

- **Vault on Apollo:** `/home/justin.guest/Developer/obsidian-vault`
- **Vault on Mac:** `/Users/justin/Developer/obsidian-vault`

---

## 2. Hermes Configuration Backup (`apollo-autocommit` / `apollo-backup`)

This section is **Hermes config only** (`~/.hermes/` → `apollo-backup` repo). It does **not** apply to the Obsidian vault.

The Hermes configuration, custom skills, custom scripts, cron jobs, and memory stores are backed up into a dedicated Git repository.

- **Local Source Paths:** Subset of `/home/justin.guest/.hermes/`
  - *Tracked Files:* `SOUL.md`, `config.yaml`
  - *Tracked Folders:* `skills/`, `hooks/`, `cron/`, `memories/`, `scripts/`
- **Local Git Repository:** `/home/justin.guest/apollo-backup` (also known as `bes-backup`)
- **Remote Repo:** `apollo-backup` on GitHub (Use SSH remote: `git@github.com:justinsensei/apollo-backup.git`)
- **Watcher Script:** `/home/justin.guest/.local/bin/apollo-autocommit`
- **Daemon Service:** `apollo-autocommit.service` (systemd-user service)
- **Log Source:** `journalctl --user -u apollo-autocommit`

### Sync Mechanism
1. **Trigger:** `inotifywait` monitors the tracked subset of `~/.hermes/` recursively.
2. **Debounce:** Accumulates events for **5 seconds**.
3. **One-way Copy & Push (Unidirectional):**
   - Re-mirrors files using `cp -p` and directories using `rsync -a --delete` to propagate file removals cleanly into `~/apollo-backup/`.
   - Forces the addition of custom/diverged user skills (overriding standard `.gitignore` rules) by comparing local hashes with the default bundled twins.
   - Commits with the subject `auto: <filename>` or `auto: N files changed` and pushes to GitHub.

### Pull Syncing & The `apollo-pull` Wrapper
Although the background daemon `apollo-autocommit` only pushes, you can safely pull down remote updates (such as edited config files, new/renamed skills, or updated scripts) from GitHub using the custom `apollo-pull` utility.
* **Command Path:** `/home/justin.guest/.local/bin/apollo-pull`
* **Execution Flow:**
  1. Stops the `apollo-autocommit` daemon to prevent file-system race conditions.
  2. Syncs any local untracked/unsynced edits from `~/.hermes/` back into `~/apollo-backup/` and auto-commits them.
  3. Pulls and rebases from the remote repository (`origin main`).
  4. On success, reverse-syncs files from the Git repo back into the live `~/.hermes/` runtime directory.
  5. Restarts the `apollo-autocommit` daemon automatically on exit.

### Critical Pitfalls & Rules
- **Use `apollo-pull` for Remote Updates:** Never run raw `git pull` in `~/apollo-backup/` to apply remote changes. Bypassing `apollo-pull` means files will *not* be reverse-synced into the active `~/.hermes/` live environment. Always run `apollo-pull` instead.
- **Editing Configs Elsewhere:** If you edit files inside the `apollo-backup` remote repository elsewhere (e.g., via the GitHub UI, another clone, or on another machine) and push them, the local VM will **not** receive those updates automatically until you execute `apollo-pull`.
- **Handling Push Conflicts:** If the remote has diverged, local modifications on the VM will trigger push failures in `apollo-autocommit`. Run `apollo-pull` immediately to reconcile the divergent branches and re-apply synced states.
- **Syncing Manual VM Changes:** If you manually update or create files under the tracked `~/.hermes` directories, the daemon will automatically detect, rsync, and push them within 5 seconds.
- **Never confuse repos:** `apollo-pull` / `apollo-autocommit` touch Hermes backup only — never the Obsidian vault.

---

## 3. Syncthing — RETIRED for the vault

**STATUS: RETIRED.** Syncthing is not used for `obsidian-vault`. Live sync is Obsidian Sync (Section 1). Do not re-enable Syncthing for the vault folder; dual sync + auto-git caused Inbox Proposal ghosts and meeting-sibling piles.

Historical notes (diagnostics only, if a leftover Syncthing install is found):

### The Emoji Conversion Quirk (😎)
In messaging clients (such as Telegram), the character combination of `B` and `)` (capital B and a closing parenthesis) automatically converts to the cool-guy emoji: 😎.
Because Syncthing outputs transferred data volumes in parentheses (e.g., `(273 B)` and `(214 B)`), these metrics will frequently arrive in chat screens as `(273 😎` and `(214 😎`. This is normal and represents small metadata keepalive packets, not file transfer speeds.

### Diagnostic Queries via REST API (legacy)
Syncthing ran an HTTP API on port `8384`. If still installed:

```bash
curl -s -H "X-API-Key: <API_KEY>" http://localhost:8384/rest/system/connections
curl -s -H "X-API-Key: <API_KEY>" "http://localhost:8384/rest/db/status?folder=obsidian-vault"
```

If a vault folder is still configured in Syncthing, remove it and rely on Obsidian Sync.
