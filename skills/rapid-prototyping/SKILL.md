---
name: rapid-prototyping
description: Use when building a demo, PoC, or throwaway experiment fast — vertical slice first, hardcode then generalize, single file, fake data, and knowing when to discard vs productionize.
---

## Goal
Get a working demo in the fewest steps: prove the risky part FIRST, use fake data and hardcoded paths, and make the extend-vs-rewrite decision with evidence.

## Order of operations

1. **The riskiest assumption is the first test.** fountain: "can jsqr decode a real QR from a camera frame?" — verify THAT before building any UI around it.
2. **Vertical slice**: one end-to-end thin path (input → core → output) that visibly works. Everything else is scaffolding.
3. **Hardcode then generalize**: the slice runs on fixed data (one QR with a known payload). Once it works, replace constants with variables.
4. **Fake the I/O**: fake camera (test image / static video), fake network (local JSON file), fake time — isolate the logic being proven.
5. **Single file first**: don't create a module tree until the monolith proves the concept.

## Prototyping tactics

| Need | Move |
|---|---|
| Quick UI | Plain HTML + one JS file, or a tiny Vite app — no framework until it earns one |
| Camera without hardware | `page.goto` + a loop over pre-generated QR images (for the decode path) |
| Server | `python3 -m http.server` or `npx serve` — not a framework |
| Shared state across devices | First: paste the JSON between windows. Then localStorage. Then a server only if needed |
| Visual feedback | Console + alert() + raw DOM, in that order — styling is last |

## The evidence rule

Every prototype milestone ends with something OBSERVABLE: a decoded payload printed, a pixel changed, a file written. If you can't see it work, it doesn't work.

## Productionize or throw away?

| Signal | Decision |
|---|---|
| Concept proven, code is 100 lines, no edge cases | Rewrite properly (keep tests/evidence) |
| Concept proven, code got ugly but works | Refactor IN PLACE only if you'll extend it this week; else rewrite when the requirements solidify |
| Concept NOT proven (decode fails, perf terrible) | Throw away and pivot — the prototype answered the question |
| User says "this is exactly what I want" | Productionize immediately, capture the evidence first |

The prototype's job is to answer a question. Once answered, it's done — keeping it "just in case" creates a second codebase to maintain.

## Pitfalls

- Polishing the prototype before the core works (styling a broken demo wastes the most time).
- Generalizing too early — every unused abstraction is a tax on understanding.
- Perfect commits mid-prototype — commit once at "it works", not every 15 minutes.
- Forgetting the demo is throwaway: if you named things well and it's small, IN-PLACE extension is fine; a full rewrite for clarity is also legitimate — decide with the evidence, not guilt.