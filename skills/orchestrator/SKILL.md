---
name: parallel-workers
description: Dispatch multiple independent sub-agents in parallel to execute concurrent tasks without blocking each other.
metadata:
  opencode/autoinvoke: "true"
---

## Rules for Parallel Execution
1. Break a complex prompt or multiple independent tasks into separate sub-tasks.
2. Delegate simultaneously (parallel agent calls): `@architect` (architecture/dependency mapping), `@coder` (write/refactor code), `@sysadmin` (shell/background tasks), `@docs` (docs, READMEs, API specs, docstrings), `@reviewer` (log inspection/code review), `@tester` (unit tests/breakage checks).
3. Fire every independent agent in ONE wave (background, non-blocking); sequence only true dependencies (e.g. `@tester`/`@reviewer` wait for `@coder`).
4. Give each agent a disjoint surface — never two agents on the same file.
5. Combine the results once all sub-agents complete their sub-tasks.

**Mechanics** (background flags, wave batching, self-contained prompts, don't-poll): see the `work-faster` skill §1a.
