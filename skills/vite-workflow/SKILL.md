---
name: vite-workflow
description: Use when working with Vite in the fountain project — dev server, HTTPS with local certs, build/preview, config options, env vars, dependency quirks, plain-JS (no framework) setup.
---

## The fountain scripts (from package.json)

| Script | Command | Use |
|---|---|---|
| dev | `vite` | HTTP dev server (default port 5173, or per config) |
| dev:https | `vite --https --cert .certs/... --key .certs/...` | HTTPS for camera (getUserMedia requires secure context!) |
| build | `vite build` | Production bundle → dist/ |
| preview | `vite preview` | Serve the built dist/ locally |
| test-roundtrip | `node test-roundtrip.mjs` | E2E QR round-trip test |

## Secure context rule (why dev:https exists)

- **getUserMedia (camera) only works on secure origins** — `https://` or `http://localhost`.
- Phone scanning from the PC's screen needs HTTPS on the LAN address + cert trust on the phone — that's what `.certs/` is for. Add `server.host: true` in vite.config.js to expose on LAN.

## vite.config.js quick reference (plain JS)

```js
import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 3000,            // match run.sh expectations (localhost:3000)
    host: true,            // expose on LAN for phone testing
    https: { cert: '.certs/cert.pem', key: '.certs/key.pem' }, // or via CLI flags
    proxy: { '/api': 'http://localhost:8080' } // backend proxy if any
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    target: 'es2020'       // jsQR/qrcode compatibility
  },
  base: './'               // relative paths if serving from file:// or subdir
});
```

## Env vars

- `.env` / `.env.local` → `import.meta.env.VITE_*` (only VITE_ prefixed are exposed)
- `import.meta.env.DEV`, `.PROD`, `.MODE` — built-in
- Changing `.env` requires a dev-server restart.

## Common fountain pitfalls

- **HTTPS + camera on phone**: both cert AND HTTPS origin must be trusted on the scanning device; on iOS the cert must be installed as a profile. Test with a real phone camera first if this is a goal.
- **jsqr only decodes from ImageData**: pass `ctx.getImageData(...)` from the capture canvas — NOT a video element. (See web-performance for downscaling.)
- **Vite HMR**: plain-JS module changes hot-reload; vite.config.js or .env changes restart the server automatically.
- **Vite 6**: Node >= 18 required — check `node -v` if `vite` errors on startup.
- **Port conflicts**: if 3000 is taken, run.sh may fail silently — `lsof -i :3000` before assuming Vite broke.

## Troubleshooting order

1. `npm install` up to date? (`npm ci` if package-lock.json exists)
2. `node -v` ≥ 18?
3. `lsof -i :3000` — port free?
4. `npx vite --debug` — verbose startup logs.
5. Cert expired/self-signed refused by browser? Recreate certs in .certs/ and re-trust.
