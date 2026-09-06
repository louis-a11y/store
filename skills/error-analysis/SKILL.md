---
name: error-analysis
description: Use when anything fails — repro first, capture the full error (logs, stack, exit code), form 3+ hypotheses BEFORE touching code, bisect, check most-recent-change-first, environment vs code.
---

## Goal
Diagnose failures systematically: reproduce, gather evidence, hypothesize (3+), test cheaply, fix the ROOT cause minimally — no shotgun debugging.

## The loop (in order, never skip steps)

1. **Reproduce.** "It fails when X" — make it deterministic. If you can't repro, you can't verify the fix.
2. **Capture FULL evidence.** Not "it crashed" — the exact: error message, stack trace, exit code, log tail, input that triggered it. `-v`/`--debug`/`DEBUG=*` where available.
3. **Form ≥3 hypotheses** before touching anything. Write them down. Rank by likelihood × cheapness-to-test.
4. **Test the cheapest hypothesis that discriminates.** One experiment, observe, update hypotheses.
5. **Most-recent-change-first**: check what changed since it last worked (git diff, recently touched files, new deps).
6. **Environment vs code**: OS version, node version, port in use, PATH, certs, permissions — before blaming your code, rule out the floor beneath it.

## Evidence templates

```bash
# full context capture (run these, paste results)
echo "--- env ---"; node -v; npm -v; uname -a
echo "--- port ---"; lsof -i :3000 || true
echo "--- error tail ---"; <cmd> 2>&1 | tail -40
echo "--- deps ---"; npm ls --depth=0 2>&1 | tail -20   # or brew list for system tools
```

## Hypothesis-driven example (bad)

- Shotgun: "maybe add a fallback, maybe retry, maybe..." → 6 random edits, 0 learnings.

## Hypothesis-driven example (good)

- Symptom: `npm run dev` fails with EADDRINUSE :3000.
- Hypotheses: (a) leftover server process, (b) another app on 3000, (c) wrong port config.
- Cheapest test: `lsof -i :3000` → answers (a)/(b) in one command. Then either kill the squatter or fix config. Done, 1 experiment.

## Bisecting

- **git bisect** for code: `git bisect start && git bisect bad && git bisect good <sha>` then binary-search the breaking commit.
- **Input bisect**: halve the input data until the minimal failing case appears (great for parsers, QR decode, regex).
- **Manual bisect**: disable halves of a feature (config flags / early returns) to localize.

## The 3-failure rule

After 2 failed fix attempts:
1. **STOP editing.** Revert to last known working state.
2. Document attempts + results.
3. Consult Oracle (read-only high-IQ) with the full failure context.
4. If Oracle can't resolve → ask the user.

## Root cause vs symptom

- The root cause is the thing that, if fixed, makes the symptom impossible — not the thing that hides it.
- "Adds retry" handles flakiness (symptom); "the server closes the socket after 30s" is the cause (fix the timeout).
- Fix MINIMALLY: never refactor while fixing. One behavior change per fix; re-verify after EVERY fix attempt.

## Pitfalls

- Shotgun debugging — random changes "hoping" (the loop exists to prevent this).
- Truncating the error to what you expect ("it's probably auth") — read the WHOLE error first.
- "Works on my machine" — that IS a data point: environmental difference is a hypothesis, test it (versions, PATH, locale, timezone).
- Deleting failing tests to make it pass — never. A failing regression test is a gift; keep it, fix the code.
- Stopping at the first explanation that sounds plausible without testing it against the evidence.