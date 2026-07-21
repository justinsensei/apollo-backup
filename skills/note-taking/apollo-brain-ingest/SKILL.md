---
name: apollo-brain-ingest
description: Master Justin's automated note-taking, ingestion, and logging pipeline (Brain Feeds Ingest). Coordinates email forwarding, Linear reactions, Telegram bookmarks, and central vault logging/entity integration.
version: 1.0.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [obsidian, ingest, brain, feeds, email, linear, telegram, logging, cron]
    related_skills: [obsidian, google-workspace]
---

# Apollo Brain Ingestion & Logging Pipeline

Automated collection pipeline for incoming personal knowledge artifacts. This skill governs the extraction, transformation, target formatting, vault routing, central audit logging, and project-entity linking for Justin's diverse incoming feeds.

## Overview & Unified Cron Job

The ingestion feeds are executed in parallel by a unified cron job **"Unified Brain Feeds Ingest"** (`284c08eb12b7`) running every 30 minutes in the background.

- **Unified Orchestrator:** `/home/justin.guest/.hermes/scripts/fetch_unified_ingest.py` runs three distinct pollers in parallel:
  - `poll_apollo_inbox.py --json` (Gmail / Email Dispatch)
  - `fetch_linear_brains.py` (Linear bookmarks)
  - `fetch_telegram_brains.py` (Flagged Telegram sessions)
- **Workflow Phase:**
  1. **Scan:** Pollers query external sources / local session databases and yield uncompleted candidates in a combined JSON structure.
  2. **Write:** The agent processes each candidate, transforming it into the specific note formats required and saving to folders in `Inputs/` (e.g. `Inputs/Linear/`, `Inputs/Telegram/`, `Inputs/Emails/`, or `/Inbox/`).
  3. **Acknowledge:** Runs marking-processed commands (e.g., `--mark-processed`) to advance watermarks and database flags so items are not processed twice.
  4. **Log & Connect:** Logs the ingestion event to `Utilities/log.md` and runs `integrate_entities.py` to link new updates to existing projects.

---

## 1. Email Forwarding & Dispatch (formerly `apollo-email-dispatch`)

Justin forwards emails to `goff.justin+apollo@gmail.com` with a one-line instruction at the top of the body. A Gmail filter labels it `Apollo/Inbox`, and `poll_apollo_inbox.py` detects it.

### Core Principle: Dual-Action Dispatch
Analyze the instruction line (`instruction` field from the loaded context) for keywords to trigger one or both of the following:

#### Action A: File Email (Save to Vault Inbox)
- **Trigger Keywords:** Contains `File this`, `file this`, `file`, `save this`, `save`, `archive this` or the instruction is **empty/none** (default fallback).
- **Target File:** `/home/justin.guest/Developer/obsidian-vault/Inbox/<Title> <ID>.md`
  *(Where `Title` is a cleaned, capitalized version of the subject, and `ID` is the 14-digit creation timestamp `YYYYMMDDHHmmss` at write time).*
- **Note Frontmatter & Body:**
  ```yaml
  ---
  id: "<YYYYMMDDHHmmss at write time>"
  daily_note: "[[<YYYY-MM-DD Weekday>|YYYY-MM-DD Weekday]]"
  category: "[[Scraps]]"
  ---
  ```
  Include `# [Cleaned Subject]`, standard email metadata (From, To, Date), a `## Context` section with Justin's instruction line, a concise summary of the content, and the cleaned plaintext body of the email.

#### Action A.b: Log Email (Save to Inputs/Emails/)
- **Trigger Keywords:** Contains `log this`, `log email`, `log thread`, `save as email log`, `log`.
- **Target File:** `/home/justin.guest/Developer/obsidian-vault/Inputs/Emails/YYYY-MM-DD - <Cleaned Subject>.md`
- **Note Frontmatter:**
  ```yaml
  ---
  id: "<YYYYMMDDHHmmss at write time>"
  daily_note: "[[<YYYY-MM-DD Weekday>|YYYY-MM-DD Weekday]]"
  category: "[[Emails]]"
  type: email
  original_url: "https://mail.google.com/mail/u/0/#search/rfc822msgid:<Message-ID>"
  ---
  ```
  Write a high-quality summary of the thread discussions and decisions. Do not copy the email contents verbatim.

#### Action B: Create an Obsidian Task (Task it) — ⚠️ UPDATED FOR TASKNOTES ⚠️
- **Trigger Keywords:** Contains `Task`, `task`, `TODO`, `todo`, `to do`, `To do`.
- **Process:**
  1. Since Todoist has been retired, write the task as a raw `- [ ]` checkbox directly inside today's Daily Note under the notepad or capture section.
  2. **Task Format:** `- [ ] <Task Name> #task` (e.g., `- [ ] Follow up on invoice #task`).
  3. Include any relevant context, due dates, or link references in the daily note bullet context.
  4. The nightly vault hygiene sweep will automatically promote this raw checkbox into a TaskNote file under `TaskNotes/Tasks/`.

#### Other Intent Shapes (Legacy Support)
- **Person/Company Notes:** "Person note for <Name>" or "New company <Name>" → Create `<Firstname> <Lastname> <ID>.md` under `Inbox/` or in `Notebook/Contacts/` per standard contacts layouts.
- **Project Notes:** "New project <Name>" → Create `<Project Name>.md` (no ID) under `Inbox/` or `Notebook/Projects/`.
- **Append to existing note:** "Add to <note title>" → Find closest match vault-wide and append a dated bullet: `- YYYY-MM-DD | Ingest — <context/details>`.

---

## 2. Linear Comment & Update Ingestion (formerly `apollo-linear-ingest`)

Captures Linear comments, project updates, and initiative updates carrying the `:obsidian_jg:` reaction or `🧠`/`brain` reaction added by Justin.

- **Target Path:** `/home/justin.guest/Developer/obsidian-vault/Inputs/Linear/YYYY-MM-DD - Linear - [Title].md`
- **Frontmatter & Note Structure:**
  ```yaml
  ---
  id: 'YYYYMMDDHHmmss'                 # Numerical string of item's createdAt timestamp
  daily_note: "[[Daily Notes/YYYY-MM-DD Weekday|YYYY-MM-DD Weekday]]"
  category: "[[Linear]]"
  original_url: "https://linear.app/..."
  author: "Author Name"
  associated_with: "https://linear.app/..."
  ---
  ```
  Below frontmatter, include `# 📥 Linear Capture: [Title]`, metadata bullets, and a high-quality 2-3 sentence **Topic Description** synthesizing the context, parent issue, and thread.

---

## 3. Telegram Conversation Ingestion (formerly `apollo-telegram-ingest`)

Captures flagged Telegram conversation sessions as structured, searchable summary records.

- **Triggering:** Flagged when Justin reacts to a bot response using the `🧠` emoji or includes `🧠` in a chat message.
- **State Database:** `/home/justin.guest/.hermes/state.db` contains schema columns `brain_flagged` and `ingested` in the `sessions` table.
- **Target Path:** `/home/justin.guest/Developer/obsidian-vault/Inputs/Telegram/YYYY-MM-DD - Telegram - [Title].md`
- **Frontmatter & Note Structure:**
  ```yaml
  ---
  id: 'YYYYMMDDHHmmss'                 # Based on session start time
  daily_note: "[[Daily Notes/YYYY-MM-DD Weekday|YYYY-MM-DD Weekday]]"
  category: "[[Telegram]]"
  session_id: "YYYYMMDD_HHMMSS_xxxxxxxx"
  source_db: "/home/justin.guest/.hermes/state.db"
  ---
  ```
  Below frontmatter, include `# 📥 Telegram Session Capture: [Title]`, session ID, and a multi-bullet high-quality **Summary** of topics, decisions made, and open questions.

---

## 4. Ingest Event Logging & Entity Integration (formerly `obsidian-ingest-log`)

This step ensures immediate traceability and semantic alignment every time a note is added to `Inputs/`.

### Phase A: Log Append (`integrate-light`)
Append a single line to the central log file:
- **Target File:** `/home/justin.guest/Developer/obsidian-vault/Utilities/log.md`
- **Log Format:** A single line with timestamp, type of ingest, a wikilink to the new note, its path, and a daily note wikilink.
- **Rules:** Never modify the body of the ingested input files under `Inputs/`. They are strictly **immutable**.

### Phase B: Entity Integration (`integrate-entities`)
- **Script:** Runs `integrate_entities.py <input_note_path>`.
- **Action:** Scans the input note for project identifiers. If a clear link is resolved, it updates the `## State` section of the corresponding project note under `Notebook/Projects/<Project Name>.md` with a concise summary.
- **Rules:** Update-only operation. Never create new project notes or stubs automatically here.

---

## Guidelines & Apollot Practices

- **Verify Writes:** After writing any note, verify the file exists on disk and is non-empty before reporting success.
- **Emails with Whitespace:** Some transactional HTML emails have empty text parts containing only whitespace (`\r\n`). When extracting bodies in custom scripts, always check `if not body.strip():` to correctly trigger fallback HTML extraction.
- **No Infinite Loops:** Skip processing any emails or messages originating from the bot itself.
- **No Daily Note Writing:** Do NOT append or write to the Daily Note (the Notepad section is completely retired). The pipeline runs hands-off and logs exclusively to `Utilities/log.md` and through `integrate_entities.py`.
- **Traceability Checklist:**
  - [ ] Target note created under `Inbox/` or `Inputs/`
  - [ ] Frontmatter includes canonical `id`, `daily_note`, and `category`
  - [ ] Central wiki log (`Utilities/log.md`) updated with the new creation
  - [ ] `integrate_entities.py` triggered for downstream project state updates
