---
name: work-faster
description: Use when you want to work faster and more efficiently. Provides techniques for parallel execution, context optimization, and task decomposition. Always triggers
---

# Work Faster

## Core Principles

Work faster by executing in parallel, managing context efficiently, and decomposing tasks properly.

## Techniques

### 1. Parallel Execution

**Always fire parallel tasks when operations are independent:**

```typescript
// CORRECT: Multiple independent searches in parallel
task(subagent_type="explore", run_in_background=true, prompt="Find auth patterns")
task(subagent_type="explore", run_in_background=true, prompt="Find error handling")
task(subagent_type="explore", run_in_background=true, prompt="Find config files")

// WRONG: Sequential searches (slow)
task(..., prompt="Find auth patterns")
// wait...
task(..., prompt="Find error handling")
// wait...
```

**Parallelize:**
- File reads (multiple files at once)
- Search operations (different patterns)
- Explore/librarian agents (always background)
- Independent edits (non-overlapping files)

#### 1a. Custom sub-agent fan-out

The `parallel-workers` skill defines *what* to delegate and to whom. This section is the *how*:
fire every custom sub-agent in a single wave, each with `run_in_background=true`, then keep
working on non-overlapping steps until their results land.

Custom sub-agents available (defined in `opencode.jsonc`):

| Agent | Delegate when |
|---|---|
| `architect` | Plan structure, map dependencies, high-level design |
| `coder` | Write or refactor code files |
| `sysadmin` | Run shell commands, manage background tasks |
| `reviewer` | Inspect logs, review diffs, double-check output |
| `tester` | Run test suites, check for breakages |
| `docs` | Update READMEs, docstrings, API specs |

```typescript
// One wave, all independent tracks, no waiting in between:
task(subagent_type="architect", run_in_background=true, prompt="Plan the auth module layout")
task(subagent_type="coder",     run_in_background=true, prompt="Implement JWT middleware per the plan")
task(subagent_type="sysadmin",  run_in_background=true, prompt="Spin up the local dev DB")
task(subagent_type="docs",      run_in_background=true, prompt="Draft the auth API reference")
// reviewer + tester come AFTER coder lands — they depend on the code existing.

// Dependent wave (only after coder returns):
task(subagent_type="tester",   run_in_background=true, prompt="Test the JWT middleware")
task(subagent_type="reviewer", run_in_background=true, prompt="Review the auth diff")
```

**Rules that make fan-out actually fast:**
- **Wave, don't chain.** Fire all *independent* agents in one message; only sequence true dependencies.
- **Give each agent a disjoint surface.** Never two agents editing the same file — that is a conflict, not parallelism.
- **Self-contained prompts.** A fresh child has zero context: include paths, goal, and success criteria.
- **One line `task_summary` per spawn** so the UI shows what was delegated.
- **Don't poll.** Background children notify on completion; go do other work meanwhile.
- **Match agent to work.** Planning → `architect`; writing → `coder`; shell → `sysadmin`; verification → `tester`/`reviewer`; prose → `docs`.

### 2. Context Management

**Prune aggressively:**
- Don't load entire files when you need one function
- Use `offset`/`limit` for targeted reads
- Stop searching after 2-3 successful finds

**Just-in-time loading:**
- Don't pre-load all possible context
- Load only what you need for the current step
- Use file paths as references, load on demand

### 3. Task Decomposition

**Break complex tasks into parallel units:**

```
// WRONG: One massive task
task(category="deep", prompt="Implement entire auth system with JWT, roles, and tests")

// CORRECT: Decomposed into parallel units
task(category="deep", prompt="Implement JWT middleware")
task(category="deep", prompt="Implement role-based access control")
task(category="deep", prompt="Write auth tests")
```

**Each task should be:**
- Atomic (one clear goal)
- Independent (no blocking dependencies)
- Small enough for focused execution

### 4. Model Routing

**Match model to task complexity:**

| Task Type | Use |
|-----------|-----|
| Simple fix, typo, config | `quick` category |
| Standard implementation | `deep` category |
| Hard logic, algorithms | `ultrabrain` category |
| UI/visual work | `visual-engineering` category |
| Architecture decisions | `oracle` agent |

### 5. Reduce Over-Exploration

**Stop conditions:**
- Same info appearing across sources
- Enough context to proceed confidently
- 2 search iterations with no new data
- Direct answer found

**Don't:**
- Read entire files for one function
- Search for patterns you already know
- Re-explore what background agents are searching

### 6. Sub-Agent Architecture

**Two tiers of agents — use both:**

*Custom (defined in `opencode.jsonc`, see §1a):* `architect`, `coder`, `sysadmin`, `reviewer`, `tester`, `docs` — for concrete delegated work.

*Built-in (omo/opencode):*
- `explore` - Codebase grep (cheap, fast)
- `librarian` - External docs (cheap, fast)
- `oracle` - Hard problems (expensive, use sparingly)
- `deep` - Autonomous implementation (mid-tier)

**Fire explore/librarian as background, continue with non-overlapping work.**

**Coordination with `parallel-workers`:** that skill owns the *policy* (break down work, delegate simultaneously, combine results). This skill owns the *mechanics* (background flags, wave batching, disjoint surfaces, don't poll). When both trigger, follow parallel-workers' rules and use §1a for execution shape.

## Quick Checklist

Before starting work:
- [ ] Can any steps run in parallel?
- [ ] Which of my 6 custom agents (`architect`/`coder`/`sysadmin`/`reviewer`/`tester`/`docs`) own which track?
- [ ] Is each delegated track on a disjoint surface (no shared files)?
- [ ] Am I loading only what I need?
- [ ] Is this task decomposed properly?
- [ ] Am I using the right model/category?
- [ ] Will I stop searching once I have enough?

## Anti-Patterns

- Reading full files when you need one function
- Sequential execution of independent tasks
- Two agents editing the same file (conflict, not parallelism)
- Delegating without a self-contained prompt (child has no context)
- Polling background tasks (wait for notification)
- Over-exploring before starting work
- Using expensive models for simple tasks