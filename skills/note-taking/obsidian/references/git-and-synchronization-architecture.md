# Git and Synchronization Architecture

This reference document outlines the exact architecture, scripts, and behaviors of the file synchronization and backup daemons running on Justin's Hermes VM.

---

## 1. Obsidian Vault Synchronization (`apollo-vault-sync`)

The Obsidian vault is configured as a fully bidirectional, real-time synced git repository.

- **Local Path:** `/home/justin.guest/Developer/obsidian-vault`
- **Remote Repo:** `obsidian-vault` on GitHub (Use SSH remote: `git@github.com:justinsensei/obsidian-vault.git`)
- **Watcher Script:** `/home/justin.guest/.local/bin/apollo-vault-sync`
- **Daemon Service:** `apollo-vault-sync.service` (systemd-user service)
- **Log Source:** `journalctl --user -u apollo-vault-sync`

### Git Authentication & SSH Remote Configuration
- **SSH Preference:** Always configure local repositories on the VM with SSH remotes (`git@github.com:...`) rather than HTTPS. The VM is authenticated to GitHub using a stable SSH key (`ssh -T git@github.com`).
- **Avoid HTTPS Credentials Pitfalls:** GitHub has deprecated password authentication for HTTPS Git operations. Using HTTPS remotes with a personal access token (PAT) stored in plain-text helpers is highly prone to expiration or mismatch failures (e.g., when local `.git-credentials-vault` files are empty or corrupt).
- **Repairing Authentication Failures:**
  If the `fs-event` synchronization or pull alerts with "Invalid username or token" or "Authentication failed":
  1. Set the remote URL to SSH:
     ```bash
     git -C ~/Developer/obsidian-vault remote set-url origin git@github.com:justinsensei/obsidian-vault.git
     ```
  2. Clean up any local or conflicting credential helpers:
     ```bash
     git -C ~/Developer/obsidian-vault config --local --unset-all credential.helper
     ```
  3. Verify with a dry-run fetch:
     ```bash
     git -C ~/Developer/obsidian-vault fetch --dry-run
     ```

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

---

## 3. Syncthing Peer-to-Peer Synchronization & Network Troubleshooting

Syncthing is utilized for real-time peer-to-peer file synchronization between the VM (`lima-apollo-vm`) and Justin's Mac Mini (`Justins-Mac-mini`), specifically synchronizing the `obsidian-vault` folder.

### The Emoji Conversion Quirk (😎)
In messaging clients (such as Telegram), the character combination of `B` and `)` (capital B and a closing parenthesis) automatically converts to the cool-guy emoji: 😎.
Because Syncthing outputs transferred data volumes in parentheses (e.g., `(273 B)` and `(214 B)`), these metrics will frequently arrive in chat screens as `(273 😎` and `(214 😎`. This is normal and represents small metadata keepalive packets, not file transfer speeds.

### Diagnostic Queries via REST API
Syncthing runs an HTTP API on the local interface (port `8384`). The active API key can be found in `~/.local/state/syncthing/config.xml` under `<gui><apikey>`.
You can query the Syncthing state programmatically from terminal:
```bash
# Check active connections and connection types (relay vs direct TCP)
curl -s -H "X-API-Key: <API_KEY>" http://localhost:8384/rest/system/connections

# Check synchronization status of the vault folder
curl -s -H "X-API-Key: <API_KEY>" "http://localhost:8384/rest/db/status?folder=obsidian-vault"
```

### Direct LAN Connections vs. Relay Fallbacks
* **Relay Fallback Issue:** Direct TCP LAN connections (`tcp://192.168.5.2:22000`) can occasionally drop with `reading length: EOF` due to hypervisor network timeouts, sleeping hosts, or firewall resets. When direct connections fail, Syncthing silently falls back to public WAN relays (`type: relay-server`). Public relays are heavily throttled (a few KB/s) and slow down syncing to a crawl.
* **Forcing Direct Connections:** To force Syncthing to bypass slow public WAN relays and maintain high-speed direct peer connections on the private network:
  1. Open the local config file: `/home/justin.guest/.local/state/syncthing/config.xml`
  2. Set `<relaysEnabled>false</relaysEnabled>` under the `<options>` tag.
  3. Set `<address>tcp://192.168.5.2:22000</address>` (explicit target IP rather than `dynamic`) for the remote device configuration.
  4. Restart the user service:
     ```bash
     systemctl --user restart syncthing
     ```
  5. Verify that `connections` reports `type: "tcp-client"` and `isLocal: true` rather than `"relay-server"`.
