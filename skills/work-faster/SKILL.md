---
name: work-faster
description: Use when you want to work faster and more efficiently. Provides techniques for parallel execution, context optimization, and task decomposition. Triggers: when you want faster results.
---

# Work Faster

Fire independent work in parallel, load only the context you need, stop searching the moment you have enough.

## 1. Parallel execution — wave, don't chain

Available sub-agents (defined in `opencode.jsonc`): `architect`, `coder`, `sysadmin`, `reviewer`, `tester`, `docs`. Built-in: `explore` (codebase grep, cheap), `general` (multi-step).

```text
# CORRECT — one wave, all independent, nothing waited on:
subagent(agent="explore",  background=true, prompt="Find auth patterns")
subagent(agent="explore",  background=true, prompt="Find error handling")
subagent(agent="sysadmin", background=true, prompt="Spin up the local dev DB")

# WRONG — sequential round-trips (each spawn costs a model call)
subagent(agent="explore", prompt="Find auth patterns")   # …wait… then next
```

Rules that make fan-out actually fast:
- **Wave, don't chain.** Fire all *independent* agents in one message; sequence only true dependencies (`tester`/`reviewer` wait until `coder` lands).
- **Disjoint surfaces.** Never two agents on the same file — that's a conflict, not parallelism.
- **Self-contained prompts.** A fresh child has zero context: include paths, goal, success criteria.
- **Don't poll.** Background children notify on completion — go do non-overlapping work meanwhile.
- **Match agent to work:** plan → `architect`; write/refactor → `coder`; shell → `sysadmin`; verify → `tester`/`reviewer`; prose → `docs`; search → `explore`.
- Parallelize without agents too: multiple independent tool calls (reads, searches) in one batch whenever the calls don't depend on each other.

Ownership split with `parallel-workers` skill: that one owns *policy* (what to break up, who does what); this file owns *mechanics* (how to fire and combine).

## 2. Context: load narrow, stop early

- Read one function via `offset`/`limit`, never whole files; targeted reads over full reads.
- Just-in-time loading — no pre-loading "just in case".
- **Stop conditions:** same info repeating across sources · enough to proceed · 2 search iterations with no new data · direct answer found.
- Don't re-explore what a background agent is already searching for; don't search patterns you already know.

## 3. Decomposition

Split complex work into parallel units — each **atomic** (one clear goal), **independent** (no blockers), **small enough** for focused execution.

```text
# WRONG: one massive "implement the entire auth system" task
# RIGHT: "JWT middleware" / "role-based access control" / "auth tests" as separate tracks
```

## 4. Routing cheap work cheaply

| Task | Route |
|---|---|
| Simple fix, typo, config | smallest/cheapest model or do it inline |
| Standard implementation | `coder` sub-agent |
| Hard logic / architecture | `architect`, or a stronger model when the user picks one (`models` search) |
| Codebase search | `explore` |
| Visual/UI judgment | needs a vision-capable model — say so if none |

Expensive models for simple tasks is the classic tax; grep you can do yourself beats spawning an agent for it.

## Pre-flight checklist

- [ ] Any steps independent → fired in one wave, background?
- [ ] Each track on a disjoint surface?
- [ ] Delegation prompts self-contained (child has no context)?
- [ ] Loading only what the current step needs?
- [ ] Will I stop searching at the first stop-condition hit?
