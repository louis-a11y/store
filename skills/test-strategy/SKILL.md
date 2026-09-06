---
name: test-strategy
description: Use when deciding what to test and how — behavior-first testing, round-trip/E2E tests (fountain has test-roundtrip.mjs), TDD for bugfixes, keeping tests fast, mocks vs reality.
---

## Goal
Write tests that catch real regressions without becoming a burden: test behavior, not implementation; test the risky paths; keep them fast enough to run constantly.

## What to test (priority order)

1. **The core deliverable end-to-end** — fountain: a QR round-trip (encode → decode → payload matches). This is the single most valuable test in the project.
2. **Edge/error paths** — decode garbage, empty input, malformed payload, network failure. Errors are where untested code fails.
3. **Untangled pure logic** — if you can extract a pure function (encode/decode/payload parsing), unit-test the invariants: `decode(encode(x)) == x`.
4. **Regressions** — for EVERY bugfix: a failing test first, then the fix (test-first regression). If the bug can't be tested, the fix is untrusted.

## Test levels (for fountain-style plain-JS)

| Level | What | Cost | When |
|---|---|---|---|
| Unit | Pure functions (payload gen, encode/decode helpers) | Instant | Always |
| Integration | Modules wired together in node (no browser) | Fast | Core logic changes |
| E2E round-trip | Real encode→decode (test-roundtrip.mjs) | Seconds | Before every release / after big changes |
| Manual/visual | Camera + real phone scan | Manual | Camera-specific behavior (can't be automated cheaply) |

## The round-trip pattern (test-roundtrip.mjs)

```js
// skeleton spirit: encode a payload with qrcode, decode the image with jsqr, compare
const qr = qrcode.create(payload);
const img = qrToImageData(qr);          // render QR to pixels
const decoded = jsqr(img.data, img.w, img.h);
assert.equal(decoded?.data, payload);
```
- Run with `npm run test-roundtrip` (per package.json) — must be a single command, exit 0 on pass.
- Extend for URL payloads, binary payloads, and long payloads (QR has capacity limits — test the boundary).

## TDD discipline (bugfix edition)

1. Write the failing test that reproduces the bug (it should FAIL on the current code — verify it does).
2. Make the minimal fix.
3. Test passes → done. Never delete a failing test to "pass" — that's admitting the bug is unfixable, which is almost never true.

## Keeping tests fast

- Prefer node-based tests over browser automation for pure logic (browser boot = seconds per test).
- One E2E test that covers the happy path beats 5 brittle browser tests.
- CI-less projects (this one): give tests a single npm script so "run the tests" is one command — makes it actually happen.

## Pitfalls

- Testing implementation (function call counts, internal state) → refactors break tests for no behavior change. Test inputs/outputs.
- Over-mocking: mocking `qrcode`/`jsqr` makes the round-trip test test nothing. Mock only external I/O (camera, network), never the lib under test.
- Skipping the boundary tests: QR payload capacity, frame rate, and canvas size are where production breaks. Test the limits, not just the happy path.
- Tests that never run in CI or a script are decoration — wire them to a command.