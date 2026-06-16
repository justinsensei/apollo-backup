---
name: apple-integrations
description: "Master macOS & Apple integrations: Apple Notes, Reminders, iMessage, Find My, and background computer-use."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Apple, macOS, Notes, Reminders, iMessage, Find-My, Computer-Use, Automation]
---

# Apple & macOS Integrations Playbook

This master skill governs all secure integrations between the virtual machine environment and the macOS host/iCloud services, as well as background desktop GUI automation.

---

## 1. Apple Notes (VM-to-Host Proxy)

Use this section to create, view, or search the Apple Notes "filing cabinet" on the macOS host over SSH via the `mac-host-notes` alias.

### Quick Commands

```bash
# List folders in the filing cabinet
ssh mac-host-notes list-folders

# List notes in a specific folder
ssh mac-host-notes list-notes "'References/ID Docs'"

# Search notes
ssh mac-host-notes search-notes "tax return"

# Create a new note
ssh mac-host-notes create-note "Personal" "My Note Title" "<h1>Note Title</h1><p>HTML Content</p>"
```

### Quoting Pitfall (SSH Argument Escaping)
SSH flattens arguments into a single string. Double-quote folder names containing spaces, then single-quote them inside your SSH call:
- **Correct:** `ssh mac-host-notes list-notes "'References/ID Docs'"`
- **Incorrect:** `ssh mac-host-notes list-notes "References/ID Docs"`

---

## 2. Apple Reminders (via remindctl)

Manage Reminders on the macOS host which sync automatically across Apple devices via iCloud.

### Quick Reference

```bash
# View today's reminders
remindctl today

# List all reminders lists
remindctl list

# Create a new reminders list
remindctl list Shopping --create

# Add a timed reminder
remindctl add --title "Hairdresser" --due "2026-05-15 14:00"

# Add reminder with an early nudge/alarm
remindctl add --title "Prep presentation" --due "2026-05-15 10:00" --alarm "2026-05-15 09:30"
```

### Due Date vs Alarm Trigger
- `--due` sets the actual due date/time of the reminder.
- `--alarm` sets the notification trigger/early nudge time. Verify with `remindctl today --json` rather than assuming the due date shifted when the UI groups items by alarm time.

---

## 3. iMessage (Read-Only SSH Proxy)

Read recent iMessages from allowlisted chats on the macOS host via `mac-host` wrapper `bes-imsg`. Note: Access is read-only; sending replies is not supported.

### Accessible Chats
Bes can query 13 allowlisted chats (including Nana, Kathy, CVS, family groups, etc.).

### Quick Reference

```bash
# List available chats and their IDs
ssh mac-host bes-imsg chats

# Read recent messages from a specific chat ID (e.g. chat-id 1, limit 10)
ssh mac-host bes-imsg recent --chat-id 1 --limit 10

# Sweep recent messages across all allowlisted chats (e.g. past 24 hours)
ssh mac-host bes-imsg recent-all --since 24h
```

---

## 4. Find My Location Tracking

Track registered Apple devices and AirTags via the FindMy macOS app using AppleScript, screenshots, and Peekaboo UI automation.

### Method A: AppleScript + Screenshot (Basic)
```bash
# Open Find My
osascript -e 'tell application "FindMy" to activate'
sleep 3

# Take a screenshot of Find My window
screencapture -w -o /tmp/findmy.png
```
Use `vision_analyze(image_url="/tmp/findmy.png", question="Where is the keys AirTag?")` to parse locations.

### Method B: Peekaboo UI Automation (Recommended)
```bash
# Open Find My and capture annotated elements
osascript -e 'tell application "FindMy" to activate'
sleep 3
peekaboo see --app "FindMy" --annotate --path /tmp/findmy-ui.png

# Click on a specific device element by annotated ID (e.g. element B3)
peekaboo click --on B3 --app "FindMy"

# Capture detail view
peekaboo image --app "FindMy" --path /tmp/findmy-detail.png
```

---

## 5. macOS Computer Use (Universal Background GUI Driver)

Drive the macOS desktop in the background via the `computer_use` tool without moving the user's cursor or stealing keyboard/window focus.

### Canonical Workflow
1. **Capture First:** Capture the active app view to discover interactive elements:
   ```
   computer_use(action="capture", mode="som", app="Safari")
   ```
2. **Action by Index:** Click, type, or interact targeting the element number from the captured index (more reliable than coordinates):
   ```
   computer_use(action="click", element=7, capture_after=True)
   ```
3. **Verify:** Re-capture or request `capture_after=True` to confirm the state change.

### Background Operations Rules
1. **Never use `raise_window=True`** unless explicitly directed by the user. Let input routing execute background-only.
2. **Scope captures to a specific app** (`app="Safari"`) to reduce visual noise and preserve privacy.
3. **Don't switch Spaces.** The background driver can interact with windows located on any Space.
