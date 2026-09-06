---
name: daily-routine
description: The user's day-to-day workflow with this AI setup — how sessions, resume/reload, skills, MCP, and desktop control fit together as a daily routine. Use when the user is starting work, resuming from yesterday, or wants to optimize how they work with the assistant. Triggers: 'start working', 'resume', 'what should i do today', 'daily routine', 'how do i use this setup day to day', 'kickoff'.
---

# Daily Routine with the AI Setup

## Morning / session start
1. **Resume, don't start fresh**: if a session exists from yesterday, `oc` (alias = `opencode -c`) in a terminal resumes the LAST session. This keeps context (todos, decisions, project state).
2. **Check project state** before acting:
   - Did anything change on disk since the last session? `git status` / `git log --oneline -5` if a repo.
   - Sessions are stored in `~/.local/share/opencode/opencode.db` — use `session_list`/`session_search` if they say "what were we doing?".
3. **Choose the right context**: fountain sessions live in `~/Desktop/progetti/fountain`, vibeos in `~/Desktop/vibeos`. Resuming from the right directory = the right session/project context.

## During the day
- **One session per project, resumed via `oc`.** Don't scatter work across throwaway sessions.
- **Config/skill/MCP changes** → `oc-reload` from a NEW terminal (kills TUI, restarts, resumes same session). This is the "poor man's hot reload".
- **Desktop/browser tasks** (opening sites, clicking around, screenshots, filling forms) → controlmcp skill (control_* tools are pre-allowed, no confirmations).
- **Long multi-step work** → use todos; the model tracks progress through them. The user should NOT need to repeat themselves — the session history + skills carry the context.
- **Uncertainty about the setup itself** → opencode-usage skill (config, restart mechanics, quirks).

## Best practices observed on this machine
- The user hates confirmation spam: work should flow. Only irreversible actions deserve a question (batch into one).
- Rest right after a restart: after `oc-reload`, the fresh session re-reads skills + config — verify one thing, then proceed.
- If the assistant gets "stuck" or the MCP `control` server dies mid-session (known eviction bug #17099): `oc-reload` fixes it. Don't retry the dead tool 5 times.
- The Gmail/browser world is reachable but separate: desktop control (Safari) and opencode (terminal) are two different surfaces. Use the right tool for the job.

## End of day / handoff
- Leave the session in a clean state: todos completed or explicitly noted as pending, code building, files saved.
- A resume (`oc`) must pick up a session where the user can say "continue" and the model knows exactly what's next — no re-explaining.
- When done with a thread, a `/handoff` (or just a final summary message) makes the next session trivial.

## Anti-patterns to avoid
- Killing/restarting opencode from INSIDE the TUI (causes "Unexpected server error" if a second instance grabs the live session) — always use `oc-reload` from another terminal.
- Two TUIs open on the same session simultaneously.
- Editing `opencode.jsonc` and expecting it to take effect without a restart.
- Making the user re-explain their setup (about-me/opencode-usage skills carry that knowledge into every session).