---
name: session-handoff
description: Use when ending, resuming, or transferring opencode sessions — /handoff summaries, what to record, resuming with oc/opencode -c, when to start fresh. Fits the user's workflow: opencode with SQLite session DB, multiple TUI windows.
---

## Goal
Never lose work across sessions: capture the right state in a handoff, resume smoothly, and know when a fresh session beats continuing one.

## The user's mechanics

- `opencode -c` (alias `oc`) resumes the LAST session — the most recent one by `time_updated`.
- `opencode -s <id>` (`ses_...`) resumes a specific session.
- Sessions persist in `~/.local/share/opencode/opencode.db`.
- `/exit` (or `ctrl+x q`) quits the TUI cleanly; `/exit` + `oc` in the same terminal = in-place restart WITHOUT a new terminal window.
- New terminal window = new session context; don't open windows when /handoff + resume works.

## The /handoff structure (what to record)

1. **Objective** — the one line of what this session was trying to do.
2. **Important Details** — facts learned: paths, versions, commands that work, user preferences.
3. **Work State** — Completed / Active / Blocked, each with concrete evidence (files touched, tests run).
4. **Next Move** — the exact next action, in command form if possible.
5. **Relevant Files** — absolute paths, with one-line annotations.
6. **Explicit Constraints** — VERBATIM user requirements (user said "do not X").
7. **Agent Verification State** — what was verified, what's pending, what failed.
8. **Delegated Agent Sessions** — session ids of subagents, which can/cannot be resumed.

## When to write a handoff

- Ending a session mid-task (a short "what we did so far" is also a handoff).
- Before a restart (`/exit` + `oc`) if the next turn might lose thread.
- Before switching projects (fountain ↔ vibeos ↔ AI setup) — different contexts, keep the thread clean.

## Resume or fresh?

| Situation | Move |
|---|---|
| Same task, same project | Resume (`oc` / `-s`) |
| Task done, new task, same project | Fresh session; keep the config in a skill |
| Different project entirely | Fresh session |
| Context feels heavy (long logs, old greps) | Fresh session, handoff the tail |
| 2 opencode windows open | Keep them on separate projects; don't stack sessions |

## Pitfalls

- `oc` resumes the *last touched* session — if you touched another project's session since, `-s` is the reliable way back.
- Restart isn't hot-reload: new skills/config are picked up on restart (`/exit` + `oc`), but the RUNNING session keeps its loaded context.
- Don't store ephemera in handoffs (transient logs, one-off greps) — those bloat the next session's context.
- If a test/occasionally-fails-command produced pre-existing failures, mark them explicitly so the next session doesn't "fix" unrelated things.