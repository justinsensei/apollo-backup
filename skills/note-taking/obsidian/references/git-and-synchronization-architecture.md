# Git and Synchronization Architecture

This reference document outlines the exact architecture, scripts, and behaviors of the file synchronization and backup daemons running on Justin's Hermes VM.

---

## 1. Obsidian Vault Synchronization (`apollo-vault-sync`)

The Obsidian vault is configured as a fully bidirectional, real-time synced git repository.

- **Local Path:** `/home/justin.guest/Developer/obsidian-vault`
- **Remote Repo:** `obsidian-vault` on GitHub
- **Watcher Script:** `/home/justin.guest/.local/bin/apollo-vault-sync`
- **Daemon Service:** `apollo-vault-sync.service` (systemd-user service)
- **Log Source:** `journalctl --user -u apollo-vault-sync`

### Sync Mechanism
1. **Trigger:** `inotifywait` monitors the vault directory recursively (ignoring `.git/`, `.obsidian/workspace`, and temporary/trash directories).
2. **Debounce:** Accumulates filesystem events for **5 seconds** before initiating a sync loop to avoid commit storms.
3. **Rebase-first Sync:**
   - Runs `git pull --rebase --autostash` first to fetch changes pushed from Justin's Mac/devices, rebasing local changes on top.
   - If a merge conflict or network failure occurs during the pull phase, it aborts the rebase and sends a Telegram alarm to Justin.
4. **Auto-commit & Push:**
   - If files are modified locally, it auto-commits with the subject format `apollo: <filename>` or `apollo: N files changed` and pushes them to GitHub.

### Critical Pitfalls & Rules
- **Do NOT manually run git commands inside `/home/justin.guest/Developer/obsidian-vault`:** The background daemon races with manual git operations and will cause spurious commits, locked trees, or rebase loops.
- **Merge Conflicts:** If the daemon alerts about a merge conflict, it pauses until resolved. Resolve it by SSHing into the VM, executing manual rebase fixes in `~/Developer/obsidian-vault`, committing, and restarting the service:
  ```bash
  systemctl --user restart apollo-vault-sync
  ```

---

## 2. Hermes Configuration Backup (`apollo-autocommit` / `apollo-backup`)

The Hermes configuration, custom skills, custom scripts, cron jobs, and memory stores are backed up into a dedicated Git repository.

- **Local Source Paths:** Subset of `/home/justin.guest/.hermes/`
  - *Tracked Files:* `SOUL.md`, `config.yaml`
  - *Tracked Folders:* `skills/`, `hooks/`, `cron/`, `memories/`, `scripts/`
- **Local Git Repository:** `/home/justin.guest/apollo-backup`
- **Remote Repo:** `https://github.com/justinsensei/apollo-backup.git`
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
