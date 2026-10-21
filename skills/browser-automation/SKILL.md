---
name: browser-automation
description: Use when driving a real browser for verification/testing — Playwright page steps, screenshots, console-error capture, mobile/desktop emulation, network interception. Works for any web app (fountain, generic sites, SPAs).
---

## Playwright quick reference (fountain is on localhost:3000)

```js
const { chromium, devices } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false }); // headed = visible, currently favored
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } }); // phone-ish receiver
  const sender = await browser.newPage();
  await sender.goto('http://localhost:3000', { waitUntil: 'networkidle' });

  // capture console errors (silent failures are the enemy)
  const errors = [];
  sender.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  sender.on('pageerror', e => errors.push(String(e)));

  await sender.screenshot({ path: '/tmp/sender.png' });
  // ... perform the QR flow steps here ...
  console.log('console errors:', errors);
  await browser.close();
})();
```

## The fountain two-tab / two-device flow

1. Sender page: generate QR (`qrcode` lib) → QR appears on screen.
2. Receiver side: new page (or phone) with camera → `jsqr` decodes from getUserMedia stream.
3. Automation: you can't easily fake a camera — read the QR payload from the sender page (`page.evaluate(() => window.__qrPayload)`) if the app exposes it, or decode the on-screen QR from a screenshot.
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
const ctx = await browser.newContext({ ...devices['iPhone 13'] });
```
Camera in headless emulation won't work without a fake stream — for camera testing use headed mode + a real webcam, or inject a fake MediaStream via `launchOptions.args` / CDP (complex; only if camera is the thing under test).

## Pitfalls

- `waitUntil: 'networkidle'` can hang if the app keeps a websocket open — prefer `'load'` then explicit waitForSelector.
- QR screenshots: save the QR canvas region, not the whole page, for reliable redecode.
- Self-signed `.certs/` may require `ignoreHTTPSErrors: true` in the Playwright context.
- Headless Chromium + getUserMedia is a known pain: camera failures are usually PermissionsPolicy/media errors — catch them in `pageerror`.
