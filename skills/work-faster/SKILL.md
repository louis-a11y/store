---
name: work-faster
description: Use when you want to work faster and more efficiently. Provides techniques for parallel execution, context optimization, and task decomposition. Triggers: 'work faster', 'speed up', 'be more efficient', 'optimize performance'.
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

**Use specialized agents:**
- `explore` - Codebase grep (cheap, fast)
- `librarian` - External docs (cheap, fast)
- `oracle` - Hard problems (expensive, use sparingly)
- `deep` - Autonomous implementation (mid-tier)

**Fire explore/librarian as background, continue with non-overlapping work.**

## Quick Checklist

Before starting work:
- [ ] Can any steps run in parallel?
- [ ] Am I loading only what I need?
- [ ] Is this task decomposed properly?
- [ ] Am I using the right model/category?
- [ ] Will I stop searching once I have enough?

## Anti-Patterns

- Reading full files when you need one function
- Sequential execution of independent tasks
- Over-exploring before starting work
- Using expensive models for simple tasks
- Polling background tasks (wait for notification)