---
name: fountain-qr-debug
description: Debug fountain QR web app — camera, jsQR scanning, roundtrip. Triggers: fountain debug, QR broken, scan fail, test-roundtrip.
---
# Fountain QR Debug (Project-Specific)

Scope: `fountain/` — `test-roundtrip.mjs`, `jsQR`, camera access, Vite dev server (`vite-workflow`), HTTPS local certs.

Actions: run `node test-roundtrip.mjs`, check camera permissions, verify `jsQR` decode, test HTTPS (`vite-workflow`), check `fountain-a346bfb39549` senpi task results for scan errors.

Free-only: local test server, no paid QR APIs.
