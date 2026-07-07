---
name: workspace-integrations
description: "Unified productivity and collaboration integrations: Google Workspace, Notion, Airtable, Microsoft Teams, Himalaya Email, Maps, and Yuanbao messaging."
version: 1.0.0
author: Hermes Agent Curator
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [productivity, integrations, google, notion, airtable, teams, mail, maps, yuanbao, apis, cli]
    related_skills: [obsidian, slack, linear, github]
---

# Workspace & Productivity Integrations

This unified skill is the master command center for all third-party collaboration platforms, cloud productivity tools, and communication APIs.

---

## Unified Best Practices for API Integrations

When interacting with external APIs (REST, CLI, or GraphQL), follow these absolute rules:

1. **Verify Credentials & Auth First:** Before performing any mutation, check connection health (e.g. `gws --check` or a light metadata read).
2. **Read Before Writing:** Always search or query to resolve the exact ID (e.g., Notion block ID, Airtable record ID, Google Calendar event ID) before making changes. Never guess resource IDs.
3. **Respect Rate Limits:**
   - Airtable: Capped at 5 requests/sec/base. Use batch endpoints (max 10 records per request).
   - Notion: Capped at ~3 requests/sec.
   - Google Workspace / Teams: Implement exponential backoff on `429 Too Many Requests`.
4. **Interactive vs Headless Modes:** For CLI tools like `himalaya` or `ntn`, use PTY mode (`pty=true`) if running interactive setup wizards, but default to piping or structured JSON outputs (`--output json`, `jq .`) for routine tasks.
5. **Protect User Privacy:** Always confirm with the user before sending emails, deleting files, sharing assets, or modifying central documents/databases. Show a diff/preview first.

---

## Core Integrations Reference Directory

Specific platforms, credentials, and execution commands are demoted to supporting subfiles for maximum discoverability and organization.

### 1. Google Workspace (Gmail, Calendar, Drive, Docs, Sheets)
- **Support Files:**
  - `references/google-workspace-api.md` (Detailed API CLI reference)
  - `references/gmail-search-syntax.md` (Gmail query grammar)
  - `scripts/google_api.py` (Compatibility wrapper)
  - `scripts/gws_multi.py` & `gws_bridge.py` (Multi-account management)
- **Key Capability:** Multi-account read-write for Docs, Calendar, Sheets, and Drive. Read-only mode for Gmail (`gmail.readonly`) as configured on Justin's workspace.

### 2. Notion
- **Support Files:**
  - `references/notion-api.md` (Detailed REST & `ntn` CLI reference)
  - `references/block-types.md` (Block JSON syntax and schemas)
- **Key Capability:** Accessing pages as Markdown, query and mutate data sources (databases), and deploying serverless Notion Workers (macOS/Linux).

### 3. Airtable
- **Support Files:**
  - `references/airtable-api.md` (Airtable REST curls & URL encoding)
- **Key Capability:** Lightweight database CRUD via `curl` and Personal Access Tokens (PATs). Uses `performUpsert` for idempotent record synchronization.

### 4. Microsoft Teams Meeting Pipeline
- **Support Files:**
  - `references/teams-meeting-pipeline.md` (Meeting ingestion CLI)
- **Key Capability:** Validate MS Graph subscriptions and replay transcript-ingestion jobs using `hermes teams-pipeline`.

### 5. Himalaya Email CLI
- **Support Files:**
  - `references/himalaya-email.md` (Himalaya setup and commands)
- **Key Capability:** Operates terminal-driven mailboxes via IMAP/SMTP configuration files.

### 6. Maps (OpenStreetMap & Overpass)
- **Support Files:**
  - `references/maps-api.md` (Maps client & categories reference)
  - `scripts/maps_client.py` (Maps client script)
- **Key Capability:** Lat/lon geocoding, reverse geocoding, nearby POI discovery, and routing distance/navigation without API keys.

### 7. Yuanbao (元宝)
- **Support Files:**
  - `references/yuanbao-group.md` (Yuanbao API & @mention workflow)
- **Key Capability:** Group and private messaging in "Pai" groups with automated @mention formatting.

---

## Troubleshooting & Debugging

| Service | Common Error | Root Cause & Resolution |
|---------|--------------|-------------------------|
| Google Workspace | `HttpError 403` | Insufficient scopes or read-only restriction. Re-authenticate via `$GSETUP --revoke` and grant upgraded scopes. |
| Notion | `404 Object Not Found` | Page or database hasn't been shared with the integration. Go to Notion UI `...` → `Connect to`. |
| Airtable | `403 Forbidden` | Personal Access Token is valid but base has not been added to the token's Access List. |
| Teams Pipeline | Expired Subscriptions | Webhooks expire in 72h. Check `hermes teams-pipeline subscriptions` and schedule `maintain-subscriptions` on cron. |
