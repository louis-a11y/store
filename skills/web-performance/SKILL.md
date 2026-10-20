---
name: web-performance
description: Use when making the fountain web app faster or auditing performance — bundle size, jsQR scanning performance, rendering, Lighthouse, profiling techniques for plain-JS Vite apps.
---

## Measure first: Lighthouse

```bash
npx lighthouse http://localhost:3000 --only-categories=performance --output=json --output-path=/tmp/lh.json
# core metrics from the JSON:
jq '.categories.performance.score' /tmp/lh.json
jq '.audits | {fcp: .["first-contentful-paint"].numericValue, lcp: .["largest-contentful-paint"].numericValue, tbt: .["total-blocking-time"].numericValue, cls: .["cumulative-layout-shift"].numericValue}' /tmp/lh.json
```

## Bundle size (Vite)

```bash
npx vite build && ls -lh dist/assets/*.js    # raw sizes
# visualize: rollup-plugin-visualizer (devDep): plugins: [visualizer({ open: true })]
```

## fountain-specific hot spots

1. **jsQR is CPU-heavy** — scans every video frame synchronously:
   - Throttle: scan at most every 2-3 frames (`frameCount % 3 === 0`).
   - Downscale the frame BEFORE jsQR (256px wide is plenty — jsQR returns data only).
   - Move scanning off the main thread → Web Worker (`new Worker('scanner.js')`, postMessage frames, receive decoded payload). THE fix if the UI janks while scanning.
2. **Canvas readback**: `getImageData` forces a GPU→CPU sync stall. Read only the scanned region, not the whole frame.
3. **QR generation (qrcode lib)**: QR per keystroke re-renders — debounce input; reuse the same canvas, redraw only when payload changes.
4. **rAF vs setInterval**: drive the camera loop with requestAnimationFrame — backpressure + battery safe.

## Rendering basics (plain JS)

- Batch DOM writes: read layout once, then write — avoid interleaved read/write (layout thrash).
- `will-change`/containment on the QR canvas only; don't paint shadows over the video layer.
- If decoding UI updates every frame (status text), only touch the DOM when the value CHANGES.

## Measuring in-page

```js
const t0 = performance.now();
jsQR(data, w, h);  // or your decode call
console.debug(`scan took ${performance.now() - t0}ms`);
```
- Run with `dev` + DevTools Performance panel once: look for long tasks (>50ms) on main thread and the jsQR frame.

## Pitfalls

- **Don't optimize blind**: a 30ms jsQR scan is only a problem if frames drop — profile first, then throttle/downscale/worker.
- `performance.now()` is per-page; if the app reloads mid-measure, measure inside the running loop.
- Lighthouse on plain `http://localhost:3000` changes some audits (no h2, service workers ignored) — compare against the https variant (dev:https).
- Vite code-splitting: a single plain-JS entry lands everything in one bundle — if it grows, static-import jsQR only where used (dynamic `import()` if scan side is a separate page).
