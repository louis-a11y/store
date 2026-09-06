---
name: web-performance
description: Use when making the fountain web app faster or auditing performance — bundle size, jsQR scanning performance, rendering, Lighthouse, profiling techniques for plain-JS Vite apps.
---

## Goal
Find and fix real performance problems in fountain (plain-JS Vite QR app): bundle bloat, jsQR scan loop cost, layout thrash, image/canvas handling — measured, not guessed.

## Measure first: Lighthouse

```bash
npx lighthouse http://localhost:3000 --only-categories=performance --output=json --output-path=/tmp/lh.json
# core metrics from the JSON:
jq '.categories.performance.score' /tmp/lh.json
jq '.audits | {fcp: .["first-contentful-paint"].numericValue, lcp: .["largest-contentful-paint"].numericValue, tbt: .["total-blocking-time"].numericValue, cls: .["cumulative-layout-shift"].numericValue}' /tmp/lh.json
```

## Bundle size (Vite)

```bash
npx vite build && ls -lh dist/assets/*.js    # see the raw sizes
# visualize: install rollup-plugin-visualizer (devDep only):
#   plugins: [visualizer({ open: true })]
# or quick: count bytes per import with a build log
```

## fountain-specific hot spots

1. **jsQR is CPU-heavy** — it scans every video frame synchronously:
   - Throttle: scan at most every 2-3 frames (`frameCount % 3 === 0`).
   - Downscale the video frame BEFORE jsQR (256px wide is plenty for QR decode; jsQR returns the data only).
   - Move scanning off the main thread → Web Worker (`new Worker('scanner.js')`, postMessage video frames, receive decoded payload). This is THE fix if the UI janks while scanning.
2. **Canvas readback**: `getImageData` forces a GPU→CPU sync stall. Only read the region you scan, not the whole frame.
3. **QR generation (qrcode lib)**: generating a QR per keystroke re-renders — debounce input; reuse the same canvas and only redraw when payload changes.
4. **RequestAnimationFrame vs interval**: drive the camera loop with rAF, not setInterval — backpressure + battery safe.

## Rendering basics (plain JS)

- Batch DOM writes: read layout once, then write — avoid interleaved read/write (layout thrash).
- Prefer `will-change`/containment on the QR canvas only; don't paint shadows over the video layer.
- If decoding UI updates every frame (status text), only touch the DOM when the value CHANGES.

## Measuring in-page

```js
// in the app: time one scan iteration
const t0 = performance.now();
jsQR(data, w, h);  // or your decode call
console.debug(`scan took ${performance.now() - t0}ms`);
```
- Run with `dev` and DevTools Performance panel once: look for long tasks (>50ms) on main thread and the jsQR frame.

## Pitfalls

- **Don't optimize blind**: a 30ms jsQR scan is only a problem if frames drop — profile first, then throttle/downscale/worker.
- `performance.now()` is per-page; if the app reloads mid-measure, restructure to measure inside the running loop.
- Lighthouse on `http://localhost:3000` — on plain HTTP, some audits change (no h2, service workers ignored). Compare against the https variant (dev:https) for accuracy.
- Vite code-splitting: with a single plain-JS entry, everything lands in one bundle — if it grows, static-import jsQR only where used (dynamic `import()` if the scan side is a separate page).