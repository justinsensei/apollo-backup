# Justin's Forwarded Email Examples and Expected Dispatches

This reference provides exact mockups of inputs and output tool calls to guide the agent's reasoning.

## Case 1: File Only (with Context)

### Input `instruction`:
```
File this. I like the idea about the flux capacitor. I wonder if we could use it for the improbablity engine.
```

### Expected Behavior:
- **Intents:** File only.
- **Vault Note Path:** `/home/justin.guest/Developer/obsidian-vault/Inbox/2026-06-05-cool-science-idea.md` (assuming subject was "Cool Science Idea")
- **Context section in markdown:**
  ```markdown
  ## Context
  I like the idea about the flux capacitor. I wonder if we could use it for the improbablity engine.
  ```

---

## Case 2: Task Only (with Context & Due Date)

### Input `instruction`:
```
Task due Friday. Gotta finish the book before the weekend.
```

### Expected Behavior:
- **Intents:** Task only.
- **Vault Note Update:**
  - Append a task checkbox directly to today's Daily Note:
    `- [ ] Finish the book before the weekend #task [due:: 2026-06-12]` (assuming Friday's date)

---

## Case 3: Dual Action (File + Task)

### Input `instruction`:
```
File this. I like the idea about the flux capacitor. I wonder if we could use it for the improbablity engine.
Task due Friday. Gotta finish the book before the weekend.
```

### Expected Behavior:
- **Intents:** Both File and Task.
- **Step 1: File Email to Vault:**
  - Save to `/home/justin.guest/Developer/obsidian-vault/Inbox/...`
  - Put "I like the idea about the flux capacitor..." under `## Context`.
- **Step 2: Create TaskNote/Daily Note Task:**
  - Append a task checkbox directly to today's Daily Note:
    `- [ ] Finish the book before the weekend #task [due:: 2026-06-12]`
