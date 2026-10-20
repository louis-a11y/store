---
name: subagent-delegation
description: Use when orchestrating parallel subagents in opencode — when to delegate, writing self-contained prompts, avoiding duplicate work, collecting results, resuming failed agents. The user's setup: explore/librarian/oracle/plan agents + category agents (Sisyphus-Junior).
---

## When to delegate vs do it yourself

| Situation | Move |
|---|---|
| Unfamiliar module, need patterns | explore agent (background) |
| External library / OSS reference | librarian agent (background) |
| Hard architecture/debug after 2+ fails | oracle (read-only consultant) |
| 2+ independent work units | parallel category agents |
| Single-file, known fix | do it directly (delegation overhead > work) |

## Delegation prompt template (all 6 sections mandatory)

```
1. TASK: Atomic, specific goal (ONE action per delegation)
2. EXPECTED OUTCOME: Concrete deliverables + success criteria
3. REQUIRED TOOLS: Explicit whitelist (prevents tool sprawl)
4. MUST DO: Exhaustive requirements — leave NOTHING implicit
5. MUST NOT DO: Forbidden actions — anticipate and block rogue behavior
6. CONTEXT: File paths, existing patterns, constraints
```

**Rule of thumb**: if the prompt is shorter than 5 lines, it's too vague.

## Parallelization rules

- Independent units → fire ALL in parallel (`run_in_background=true` for explore/librarian), never sequentially.
- Each prompt must be self-contained: subagents do NOT inherit your conversation context.
- Anti-duplication: once you delegate a search, do NOT re-run the same search yourself. Continue with non-overlapping work and end your response — the system notifies you when tasks complete.
- ONE goal + ONE deliverable per call. Multiple goals → multiple parallel calls, never bundled.

## Collecting results

- Wait for the completion notification (`<system-reminder>`); never poll a running background task.
- Fetch via `background_output(task_id="bg_...")` — that's the background TASK id, distinct from the continuation SESSION id (`ses_...`).
- Oracle-dependent implementation is BLOCKED until the Oracle result arrives — do unrelated prep only, never "time out and continue anyway".

## Resuming failed agents (continuations)

- Every task returns a continuation session id (`ses_...`). Store it.
- Failed/incomplete → `task(task_id="ses_...", prompt="Fix: {specific error}")`; verification failed → same with "Failed verification: {error}. Fix." Either way the agent keeps FULL context, no re-exploration.
- NEVER start fresh for a follow-up — it re-reads everything and loses what the agent already learned.

## Pitfalls

- **Vague delegation = failed delegation**: missing a MUST NOT DO section invites scope creep ("also refactored my whole module").
- **Wrong category**: UI work → visual-engineering; hard logic → ultrabrain; autonomous research+implement → deep. Mismatched categories produce measurably worse output.
- **Fire-and-forget without verification**: after the agent reports done, VERIFY yourself — does it work, does it match existing patterns, did it respect MUST DO/MUST NOT DO?
- Canceling: cancel disposable tasks individually (`background_cancel(taskId=...)`), never all at once.
- Don't delegate "quick fixes" to keep hands busy — if there's no appropriate category, direct work is correct.
