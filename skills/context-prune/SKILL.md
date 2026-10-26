---
name: context-prune
description: Trim stale context, memory, and session noise to cut token cost. Triggers: prune context, reduce tokens, clean session, trim bloat, memory cleanup.
---
# Context Prune (Free / No Paid)

When: session feels heavy, token count high, repeated context, old tasks still referenced.

Actions (local, free):
- List `~/.omo/agent/sessions/` — archive old session `.jsonl` (move to `/tmp/archive/` or delete if unneeded)
- Clear `~/.omo/memory/` transient notes not referenced in 3+ sessions
- Trim `opencode.jsonc` agent descriptions to <120 chars if verbose
- Reset `PI_RULES_MAX_RULE_CHARS` / `PI_RULES_MAX_RESULT_CHARS` to 4000 / 12000 if not already low
- Drop stale `senpi-task/tasks/*.json` from finished runs (read results first, then delete)

Skip: do NOT drop active session files or auth credentials (`auth.json`).
