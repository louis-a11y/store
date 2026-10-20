---
name: parallel-workers
description: Dispatch multiple independent sub-agents in parallel to execute concurrent tasks without blocking each other.
metadata:
  opencode/autoinvoke: "true"
---

## Rules for Parallel Execution
1. When receiving a complex prompt or multiple independent tasks, break the work down into multiple separate sub-tasks.
2. Delegate tasks simultaneously using parallel agent calls:
   - Call `@architect` for planning software architectures and/or mapping dependencies.
   - Call `@coder` for writing and/or refactoring code.
   - Call `@sysadmin` for executing shell/background tasks.
   - Call `@docs` for updating documentation and/or READMEs, API specs, docstrings.
   - Call `@reviewer` for log inspection and/or code reviewing.
   - Call `@tester` for unit tests and/or checking for breakages.
3. Fire every independent agent in ONE wave (background, non-blocking); sequence only true dependencies (e.g. `@tester`/`@reviewer` wait for `@coder`).
4. Give each agent a disjoint surface — never two agents on the same file.
5. Combine the results once all sub-agents complete their sub-tasks.

**Mechanics** (background flags, wave batching, self-contained prompts, don't-poll): see the `work-faster` skill §1a.