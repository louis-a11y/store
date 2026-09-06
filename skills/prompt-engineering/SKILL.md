---
name: prompt-engineering
description: Use when writing instructions for AI agents — user requests, delegation prompts, skill descriptions, slash commands. Covers context-first prompting, explicit success criteria, constraints, and avoiding ambiguity that causes rework.
---

## Goal
Write prompts that get the agent to the right result on the first try: context, goal, constraints, and done-criteria, with no ambiguity left for guessing.

## The user's prompting style (encode it)

- Explicit implementation verbs when you want work: "implement/add/create/fix" — never rely on implication.
- Say research when you want research: "explain", "find", "investigate" → answer only, no edits.
- Provide file paths when you know them; file+reason when you don't: "X is broken" < "X is broken, seems related to Y in src/z.js".
- One compound ask = multiple prompts. Split: "do A and B and C" → 3 separate asks, or explicitly allow delegation.

## Prompt anatomy (the 6 sections that matter)

1. **CONTEXT**: what the agent is working on, which files/modules, current approach. "I'm adding auth to the API in src/routes/"
2. **GOAL**: the single outcome with a success criterion. "A POST /login endpoint returning a JWT; smoke test returns 200"
3. **CONSTRAINTS**: what NOT to touch, what style to match (reference a real file).
4. **MUST DO list**: exhaustive requirements — never leave anything implicit that matters.
5. **MUST NOT DO list**: anticipate and block rogue behavior ("don't refactor while fixing", "no new deps").
6. **DONE criteria**: how you'll verify (diagnostics clean, build passes, test run).

## Rules for each element

| Element | Do | Don't |
|---|---|---|
| Context | Reference real paths/patterns | Assume the agent knows your repo |
| Goal | Measurable outcome ("returns boolean", "exit 0") | "Make it better" |
| Constraints | Explicit prohibitions | Rely on the agent's judgment for scope |
| Verification | Name the command you'll run | Leave success undefined |

## Ambiguity handling

- Multiple interpretations, similar effort → pick a reasonable default and STATE the assumption.
- Multiple interpretations, 2x+ effort difference → ask ONE question first.
- Missing critical info → ask before burning tokens.
- If the requested design looks wrong, say so BEFORE implementing: "I notice X → this will cause Y because Z. Alternative: W. Proceed or switch?"

## Pitfalls

- **Vague verbs** ("handle", "deal with", "check") produce vague work — translate to concrete actions.
- **Buried constraints**: put "DO NOT refactor" at the TOP, not paragraph 7 — agents weight early instructions higher.
- **Implied scope** ("clean up this function") invites scope creep — bound it ("change only the error branch").
- **Compound requests** in one message dilute the priority — the agent executes linearly, so order matters; put the critical item first.
- For parallel work, write each sub-prompt as a SELF-CONTAINED spec: subagents don't share the conversation context of the parent.