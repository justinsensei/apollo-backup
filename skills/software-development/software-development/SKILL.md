---
name: software-development
description: "Core Software Engineering Workflows: Plan Mode, TDD, Systematic Debugging, and Pre-Commit Reviews."
version: 1.0.0
author: Hermes Agent Curator
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [software-development, engineering, planning, tdd, debugging, code-review, verification, workflow]
    related_skills: [subagent-driven-development, apollo-skill-authoring, runtime-debugging]
---

# Software Engineering Workflows

This umbrella skill captures the core development cycle and engineering practices required for high-quality code. It synthesizes planning, testing, debugging, and verification into a cohesive workflow.

---

## 1. Plan Mode (Implementation & Spike Prototypes)

Use this workflow when designing a feature, breaking down complex requirements, or feeling out an idea with a spike.

### Core Behavior
- **Planning Only:** For this phase, do not write production code or edit project files.
- **Deliverable:** A markdown plan saved under `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md`.
- **Granularity:** Break down features into bite-sized tasks (2-5 minutes of focused work each).

### Spike Prototypes
When validating feasibility, comparing approaches, or exploring unknown architectures, run a disposable **spike**:
1. **Decompose** into 2-5 independent feasibility questions.
2. **Build** inside standalone directories under `spikes/` with a bias toward runnability (CLIs, tests, simple servers).
3. **Verdict:** Close each spike with a `README.md` containing `VALIDATED`, `PARTIAL`, or `INVALIDATED`.

### Plan Template
```markdown
# [Feature Name] Implementation Plan

> **For Hermes:** Use subagent-driven-development to implement this task-by-task.

**Goal:** [One sentence goal]
**Architecture:** [Approach overview]
**Tech Stack:** [Libraries/Technologies]

---
### Task 1: [Descriptive Name]
**Objective:** [One sentence objective]
**Files:**
- Create/Modify: `exact/path/to/file.py`
- Test: `tests/path/to/test.py`

**Step 1: Write failing test**
**Step 2: Verify failure (RED)**
**Step 3: Minimal implementation**
**Step 4: Verify pass (GREEN)**
**Step 5: Commit**
```

---

## 2. Test-Driven Development (TDD)

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

### The Red-Green-Refactor Cycle
1. **RED — Write Failing Test:**
   - Focus on behavior, not implementation details.
   - Run the specific test and watch it fail for the expected reason (`pytest tests/test_file.py::test_name -v`).
2. **GREEN — Minimal Code:**
   - Write the simplest code to make the test pass. Hardcoding and duplication are acceptable in this phase.
3. **REFACTOR — Clean Up:**
   - Remove duplication, improve naming, simplify logic.
   - Ensure the test suite remains green throughout.

---

## 3. Systematic Debugging

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Never guess or apply "quick fixes". Always follow the four phases:

### Phase 1: Root Cause Investigation
1. **Read Error Messages:** Analyze stack traces and line numbers carefully.
2. **Reproduce Consistently:** Write an automated test or trigger command.
3. **Check Recent Changes:** Check `git diff` and recent commits (`git log -10`).
4. **Trace Data Flow:** Trace variables and upstream call stacks to their origin.

### Phase 2: Pattern Analysis
- Find working examples of similar code in the codebase.
- Compare working against broken to identify differences.

### Phase 3: Hypothesis and Testing
- Formulate a single, specific root-cause hypothesis.
- Make the *smallest possible change* to test the hypothesis.

### Phase 4: Implementation & The Rule of Three
- Create a failing regression test, implement the single fix, and verify.
- **Rule of Three:** If 3+ fixes have failed, **STOP and question the architecture**. Do not attempt a 4th fix without discussing architectural patterns or coupling issues with the user.

---

## 4. Pre-Commit Code Verification

Run this verification pipeline before committing or pushing changes to any git repository.

### Step-by-Step Pipeline
1. **Get the Diff:** Run `git diff --cached` (or `git diff HEAD~1 HEAD` if already committed).
2. **Static Security Scan:** Scan added lines (prefixed with `+`) for:
   - Hardcoded secrets (`api_key`, `secret`, `password`)
   - Shell injection (`os.system`, `subprocess(..., shell=True)`)
   - Dangerous calls (`eval(`, `exec(`, `pickle.loads(`)
   - SQL injection (`execute(f"..."`)
3. **Baseline Comparison:**
   - Detect project language (Python, JS/TS, Go, Rust).
   - Stash changes, run tests to establish **baseline_failures**, pop changes, and verify no *new* regressions or lint/type errors are introduced.
4. **Code Review Subagent:**
   - Dispatch an independent reviewer using `delegate_task`:
   ```python
   delegate_task(
       goal="Review the following git diff for security issues and logic errors...",
       context="Independent review. Return only JSON verdict.",
       toolsets=["terminal"]
   )
   ```
5. **Auto-Fix Loop:** (Max 2 cycles)
   - If security or logic errors are flagged, dispatch a code fix subagent to fix only those issues, then re-verify.
6. **Commit:** If clean, commit with `git commit -m "[verified] <description>"`.
