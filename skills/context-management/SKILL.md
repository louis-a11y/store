---
name: context-management
description: Use when an opencode session feels heavy or slow — context bloat, long tool outputs, repeated reads — to keep the window lean and the agent sharp. Includes targeted-reading, delegation, and pruning tactics that match the user's setup.
---

## Goal
Keep the context window lean so the agent reasons well: avoid bloat at the source, read only what's needed, delegate bulk, and prune before continuing.

## What bloats context (in order of damage)

1. Full-file reads of big files (grep/read targeted ranges instead)
2. Long command outputs (logs, ls -la of huge dirs, npm install walls)
3. Repeated greps for the same thing (search once, or delegate to explore)
4. Re-reading files already in context (leverage subagent continuations instead)
5. Giant frontmatter/skill dumps injected into unrelated tasks
6. Pasting entire error logs instead of the tail + summary

## Tactics

| Bloat source | Fix |
|---|---|
| Need one function | Read the range (offset/limit), not the file |
| Need a symbol across files | grep with include filter, output 'content' mode, head_limit |
| Huge build output | Run with output to file; grep the file for errors only |
| Repo-wide search | Explore agent in background — keeps parent context clean |
| Multi-step follow-up | Resume the SAME subagent (task_id) — it keeps its own context |
| Old irrelevant logs | Delete/purge mentally — don't re-read to "confirm" |
| Long sessions | /handoff the tail and start fresh for the next objective |

## The read-then-forget rule

- Read with a purpose: "I need these 3 facts from this file" — extract, use, don't paste back.
- Prefer `grep` for locating, `read offset` for the slice, `lsp_find_references` for symbol graph — each cheaper than a full read.
- Delegation is context-management: explore/librarian agents (background) return SUMMARIES, not full dumps.

## Quantified guardrails

- Keep the active file set under ~5 files you truly need; the rest is on disk.
- If a single tool output would exceed ~50KB of useful text, filter it first (head_limit, include, -q).
- If the conversation is >50% old tool dumps and <50% reasoning/results, it's time to compact or handoff.

## Pitfalls

- **The "just in case" read**: reading a file to be safe often lands ~1000 lines of dead weight. Decide the question first.
- **Inline dupe-checking**: after firing explore for a search, DON'T re-grep the same thing (Anti-Duplication) — it doubles the cost and can contradict the agent.
- **Background-task roulette**: waiting on background_output while the parent does nothing = idle context; end your response and let the notification come.
- **Bad habits from chat tools**: pasting a 200-line "here's the error" when `head -5` of the log + the stack line suffices.