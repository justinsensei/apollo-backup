# ADHD Product Design Principles & Pitfalls

This reference captures the condensed domain knowledge, design principles, and user-experience pitfalls compiled during the extraction and synthesis of ADHD-focused research and user feedback.

## 1. The Core Meta-Problems
*   **The "App Graveyard" & Setup Burden:** ADHD users frequently hyperfocus on building complex, highly customizable "perfect systems" (Notion databases, multi-app setups) only to abandon them within days. Feature-rich, under-opinionated systems that demand ongoing administrative maintenance are catastrophic for users with low executive function.
*   **Object Permanence vs. Cognitive Load:** For ADHD brains, "out of sight, out of mind" is literal. If tasks, files, or learning modules are tucked away inside nested lists or database folders, they cease to exist. However, displaying too much text or too many choices triggers immediate cognitive overload and avoidance.
*   **The "Streak" Shame Spiral:** Common gamification (Duolingo, habit trackers) relies on loss-aversion streak mechanics. When real-life chaos interrupts a streak, the reset triggers a deep sense of moral failure and shame, leading the user to delete or abandon the app entirely.

## 2. Design Principles for ADHD-Friendly Products

### A. Frictionless Capture & Ingestion
*   **Zero-Configuration Utility:** Provide value immediately on launch without demanding signups, configurations, or upfront goal setting (e.g., Goblin.tools).
*   **Ubiquitous Input Channels:** Support adding thoughts, tasks, and notes from anywhere (voice notes, SMS, snaps of worksheets) and use background AI to automatically parse and organize them.

### B. Time Externalization & Spatial UX
*   **Visual Timelines:** Do not represent time abstractly (standard calendar grids or dense text lists). Make duration spatial (color-coded blocks, progress rings, countdown visualizers) so users can physically "see" time.
*   **Glanceable Widgets:** Place highly visual, zero-friction widgets on the user's home screen so context remains ambiently visible without requiring them to open the app.

### C. Active Task Initiation & Deconstruction
*   **"Spiciness" (Granularity) Slider:** Provide on-demand, variable task deconstruction. Users in deep paralysis need big goals broken down into micro-actions (e.g., "pick up sponge," "turn on faucet").
*   **Scaffolding over Listing:** Replace long, overwhelming to-do lists with single-action transitions (e.g., one-click "Start" buttons for 5-minute micro-sessions).

### D. Resilient, Forgiving Re-entry
*   **"Session Save" (Context Restoration):** Actively capture and restore the user's exact working state. Rebuilding mental context is 50% more expensive for ADHD individuals; the product must recall what they were doing and why.
*   **The "Welcome Back" Ritual:** Explicitly build for irregular engagement. When a user returns after a gap, never show a red wall of overdue tasks, missed streaks, or penalties. Ask "What has changed?" and help them reprioritize fresh from a neutral state.

### E. Social Scaffolding
*   **Body Doubling:** Social presence is the most effective neurological trigger for task initiation. Introduce on-demand, synchronous, or virtual body-doubling mechanisms (e.g., Focusmate model) to help users cross the initiation gap.

## 3. Pedagogical Principles for ADHD Learning

### A. Hyperfocus Support
*   **Immersive Deep-Dives:** Traditional educational apps force users into artificial daily limits or Pomodoro-style interruptions. A great ADHD learning tool detects high-flow states and dynamically transitions the user from "bite-sized lessons" to rich, non-linear, branching exploration.

### B. Interest-Coupled Instruction
*   **Intrinsic Relevance:** Wrap arbitrary curriculum concepts in the learner's current obsessive interest (e.g., teaching fractions using skateboard ratios, or language through gaming).
