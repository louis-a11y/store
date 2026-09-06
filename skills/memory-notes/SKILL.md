---
name: memory-notes
description: Use when recording or recalling project knowledge in opencode — what to store in memory (opencode-mem), what NOT to store, search cadence, pruning stale notes, and where memory complements skills.
---

## Goal
Use the memory system (opencode-mem plugin + memory tool) as a durable project brain: store the right facts, retrieve them fast, and prune what goes stale — without competing with skills.

## What memory is for vs what skills are for

| Thing | Storage |
|---|---|
| Preferences, decisions, command workflows, project facts | **Memory** (fast retrieval, per-project) |
| Stable "how to do X" procedures (bake into steps) | **Skill** (~/.config/opencode/skills/<name>/SKILL.md) |
| Transient state (in-progress todos, current diff) | Session only — NOT memory |
| Code | Files — never memory |

The rule of thumb: memory = facts and decisions you'd want on ANY task; skills = procedures that trigger on keywords.

## What to store (high value)

- Preference decisions: "user wants terse replies", "no confirmation for reversible actions", "ask only if irreversible".
- Project facts: how to run/build/test each project (fountain: npm run dev:https + run.sh; vibeos: make run / debug).
- Environment facts: MCP servers connected, brew prefix (/opt/homebrew), tools at ~/tools/.
- Recurring workflow commands that took 2+ tries to get right.

## What NOT to store

- Code, quotes of errors (store the FIX, not the log), transient dir listings.
- Anything likely to change weekly (versions drift — keep "brew is at /opt/homebrew", not version numbers).
- Facts that live in a skill already (duplication = drift).

## Search cadence

- Search memory BEFORE answering anything that smells project-specific: "have we solved this before / does the user have a preference here?" — one `memory search` call is cheap.
- Use memory when a session restarts on a project you've worked on (`oc` resumes; memory fills the gaps in under a second).
- If a search returns nothing, that's an answer too — don't re-search the same phrasing; broaden the query once, then move on.

## Pruning / hygiene

- When a note is superseded (new decision), UPDATE it — don't append a conflicting one.
- If a stored fact is contradicted by the live system (e.g. new MCP server), correct the note that session.
- Every few weeks: list memory per project and delete notes that describe processes that changed ("we no longer use X").
- Memory is per-project scoped (`scope: "project"`) — keep cross-project facts (machine prefs) in a user/global-scope note.

## Pitfalls

- **Storing reactions** ("that was annoying") — worthless in 2 weeks; store the underlying decision.
- **Storing what the code says** — the code IS the source of truth; memory is for what the code doesn't say (why, what was decided, who prefers what).
- **Never trusting memory over the live system**: if memory and reality disagree (version, path), reality wins — update memory.
- **Silent drift**: memory that's never pruned becomes a distraction — stale notes get searched and mislead. Prune on change, not annually.