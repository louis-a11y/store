---
name: dev-workflow
description: How this user wants development work done — general discipline for writing, refactoring, and shipping code in their projects. Use for any coding task that isn't project-specific: how to structure work, verification gates, commit discipline, quality bars. Triggers: 'how should i code this', 'best practices for this task', 'implement X', code review, refactoring, testing, commits.
---

# Dev Workflow (general discipline)

## Operating principles
1. **Act, don't ask** — routine coding actions need no confirmation. Only irreversible things (deletes, force-push, mass renames) get a question, batched into one at most.
2. **Senior-engineer output** — code indistinguishable from a senior dev's: match existing patterns, no AI slop, no excessive ceremony.
3. **Terse communication** — no status updates, no post-task summaries unless asked. Todos ARE the progress tracker.

## Execution discipline
1. **Plan first for non-trivial work**: 2+ steps → atomic todos (WHERE + HOW + WHY + expected RESULT per item; one item = 1-3 tool calls).
2. **Parallelize**: independent reads/searches/tasks run simultaneously; independent implementation units → delegate in parallel.
3. **Match the codebase**: disciplined project → follow conventions strictly. Chaotic → propose a convention, ask once, then apply.
4. **Verify as you go**: after edits run `lsp_diagnostics` on changed files; at completion run the project's build/test commands. Exit 0 + clean diagnostics = done. No evidence = not complete.
5. **Fail fast, recover clean**: 3 consecutive failed fix attempts → STOP, revert to last known-good, document, and consult (oracle/debugging route) instead of shotgun-debugging.

## Code quality bars (non-negotiable)
- No type-error suppression (`as any`, `@ts-ignore`, `@ts-expect-error`).
- No empty catch blocks; handle errors explicitly (typed errors, propagate meaningfully).
- Prefer existing libraries over new deps; small focused changes over big refactors.
- **Bugfix rule**: fix minimally, never refactor while fixing.
- Never commit unless the user explicitly asked. No force-push. Match the repo's commit style when committing.

## Delegation rules (subagents)
- Delegate to the category matching the domain (visual → visual-engineering, logic-heavy → ultrabrain, research-heavy → deep, trivial → quick).
- Prompt must include: TASK (atomic goal) + EXPECTED OUTCOME + MUST DO + MUST NOT DO + CONTEXT (file paths, patterns to follow). Vague prompts are failures.
- After delegation: verify the result actually works and follows codebase patterns.

## When in doubt
- Ambiguous request with 2x+ effort between interpretations → ask ONE question with a recommended default.
- User's design is flawed → state the concern concisely, propose an alternative, ask to proceed either way.
- A specialist exists (explore/librarian/oracle/debugging skills) → use it instead of grinding alone.

## Definition of done
- [ ] Todos complete, each marked as it finished
- [ ] Diagnostics clean on touched files
- [ ] Build/test passes (or pre-existing failures explicitly noted)
- [ ] Original request fully addressed; no scope creep
