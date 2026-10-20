---
name: test-strategy
description: Use when deciding what to test and how — behavior-first testing, round-trip/E2E tests (fountain has test-roundtrip.mjs), TDD for bugfixes, keeping tests fast, mocks vs reality.
---

## What to test (priority order)
1. **The core deliverable end-to-end** — fountain: a QR round-trip (encode → decode → payload matches). The single most valuable test in the project.
2. **Edge/error paths** — decode garbage, empty input, malformed payload, network failure. Errors are where untested code fails.
3. **Untangled pure logic** — extract pure functions (encode/decode/payload parsing), unit-test the invariants: `decode(encode(x)) == x`.
4. **Regressions** — for EVERY bugfix: a failing test first, then the fix. If the bug can't be tested, the fix is untrusted.

## Test levels (fountain-style plain-JS)

| Level | What | Cost | When |
|---|---|---|---|
| Unit | Pure functions (payload gen, encode/decode helpers) | Instant | Always |
| Integration | Modules wired together in node (no browser) | Fast | Core logic changes |
| E2E round-trip | Real encode→decode (test-roundtrip.mjs) | Seconds | Before every release / after big changes |
| Manual/visual | Camera + real phone scan | Manual | Camera-specific behavior (can't be automated cheaply) |

## The round-trip pattern (test-roundtrip.mjs)

```js
// encode a payload with qrcode, decode the image with jsqr, compare
const qr = qrcode.create(payload);
const img = qrToImageData(qr);          // render QR to pixels
const decoded = jsqr(img.data, img.w, img.h);
assert.equal(decoded?.data, payload);
```
- Run with `npm run test-roundtrip` (per package.json) — must be a single command, exit 0 on pass.
- Extend for URL payloads, binary payloads, and long payloads (QR has capacity limits — test the boundary).

## TDD discipline (bugfix edition)
1. Write the failing test that reproduces the bug — verify it FAILS on the current code.
2. Make the minimal fix.
3. Test passes → done. Never delete a failing test to "pass" — that's admitting the bug is unfixable, which is almost never true.

## Keeping tests fast
- Prefer node-based tests over browser automation for pure logic (browser boot = seconds per test).
- One E2E test covering the happy path beats 5 brittle browser tests.
- CI-less project: give tests a single npm script so "run the tests" is one command, or they never run.

## Pitfalls
- Testing implementation (function call counts, internal state) → refactors break tests for no behavior change. Test inputs/outputs.
- Over-mocking: mocking `qrcode`/`jsqr` makes the round-trip test test nothing. Mock only external I/O (camera, network), never the lib under test.
- Skipping boundary tests: QR payload capacity, frame rate, and canvas size are where production breaks. Test the limits, not just the happy path.
