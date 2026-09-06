---
name: browser-automation
description: Use when driving a real browser for verification/testing of the fountain app — Playwright page steps, screenshots, console-error capture, two-tab QR flow, mobile emulation for the scan side.
---

## Goal
Verify the fountain QR-transfer web app in a real browser: load it, click through the sender→receiver flow, capture console errors, screenshot evidence, and simulate the phone (scanning) side.

## Playwright quick reference (fountain is on localhost:3000)

```js
// minimal round-trip check (matches test-roundtrip.mjs spirit)
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false }); // headed = visible, currently favored here
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } }); // phone-ish for receiver
  const sender = await browser.newPage();
  await sender.goto('http://localhost:3000', { waitUntil: 'networkidle' });

  // capture console errors (silent failures are the enemy)
  const errors = [];
  sender.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  sender.on('pageerror', e => errors.push(String(e)));

  // screenshot evidence
  await sender.screenshot({ path: '/tmp/sender.png' });

  // ... perform the QR flow steps here ...
  console.log('console errors:', errors);
  await browser.close();
})();
```

## The fountain two-tab / two-device flow

1. Sender page: generate QR (`qrcode` lib) → QR appears on screen.
2. Receiver side: use a new page (or a phone) with camera → `jsqr` decodes from getUserMedia stream.
3. In automation: you can't easily fake a camera — but you CAN read the QR payload from the sender page (`page.evaluate(() => window.__qrPayload)`) if the app exposes it, or decode the on-screen QR from the screenshot.
4. HTTPS caveat: camera (getUserMedia) requires a secure context — dev uses `dev:https` with `.certs/`. Playwright's `http://localhost` also overrides insecure-origin quirks, but test against the https variant to be safe.

## Common actions

| Action | Snippet |
|---|---|
| Click | `await page.click('#send-btn')` |
| Fill input | `await page.fill('#url-input', 'https://x.com')` |
| Wait for element | `await page.waitForSelector('#qr-canvas', { timeout: 5000 })` |
| Wait for text | `await page.waitForSelector('text=Connected')` |
| Get attribute | `await page.getAttribute('#qr-canvas', 'data-payload')` |
| Evaluate | `await page.evaluate(() => navigator.userAgent)` |
| Network response | `await page.waitForResponse(r => r.url().includes('/api'))` |

## Mobile (phone) emulation for the scan side

```js
const iPhone = devices['iPhone 13'];
const ctx = await browser.newContext({ ...iPhone });
```
Camera in headless emulation won't work without a fake stream — for camera testing use headed mode + a real webcam, or inject a fake MediaStream via `launchOptions.args` / CDP (complex; only if camera is the thing under test).

## Pitfalls

- `waitUntil: 'networkidle'` can hang if the app keeps a websocket open — prefer `'load'` then explicit waitForSelector.
- Screenshots of QR codes: save the QR canvas region, not the whole page, for reliable OCR/redecode.
- Playwright browsers must match the app's https cert — if `.certs/` is self-signed, Playwright may need `ignoreHTTPSErrors: true` in context.
- Headless Chromium + getUserMedia is a known pain: if camera fails on page, the error is usually a PermissionsPolicy/media error, catch it in `pageerror`.