---
name: project-workflow
description: Specifics of the user's main projects — fountain (QR web app) and vibeos (custom OS). Use when working inside those codebases: what they are, how to run/build/test them, their conventions. Triggers: 'work on fountain', 'work on vibeos', 'fountain app', 'vibeos', 'kernel', 'QR app', 'run fountain', 'build vibeos'.
---

# Project Workflows

## fountain — QR code web app
**Path**: `~/Desktop/progetti/fountain`

### What it is
A Vite 6 project. Frontend web app doing QR code work (qr-utils.js, jsqr + qrcode npm deps). There are "sender" and "receiver" flows (sender.js, receiver.js) routed through main.js/app.js, plus history.js, settings.js, db.js (local persistence), and a standalone static site in `web app/` (photo gallery + audio pages — separate from the Vite app).

### How to run it
```bash
cd ~/Desktop/progetti/fountain
npm run dev             # vite dev server (default port 5173)
npm run dev:https       # vite --host with the project's .certs/ (used for camera/QR over https)
./run.sh                # npm run dev in bg, then opens http://localhost:3000
```
- `npm run build` → `dist/`.
- The project ships its own TLS certs under `.certs/` — camera/QR APIs need a secure context, so HTTPS flows are a first-class concern here.

### Conventions & quirks
- Plain JS (ES modules, `"type": "module"`), no framework — app.js/main.js style orchestration.
- `test-roundtrip.mjs` at root exercises a QR send→receive round trip; update it when the QR protocol changes.
- `.omo/` at root holds plan artifacts; don't delete casually without asking (they record past decisions).
- `.playwright-mcp/` exists → browser testing of the app is expected to happen via Playwright.

### Acceptance gate for fountain changes
- `npm run build` exits 0.
- If the change touches the QR protocol or sender/receiver flow: `node test-roundtrip.mjs` passes.
- Manual visual check via the running dev server (this user owns a browser: use controlmcp/Playwright to verify).

---

## vibeos — custom operating system
**Path**: `~/Desktop/vibeos`

### What it is
A from-scratch hobby OS for x86. Own kernel (`kernel.c`, `kernel.h`), boot chain (`boot.asm`, `entry.asm`), GRUB + limine dual boot flow (`grub.cfg`, `limine.conf`), linker scripts (`linker.ld`, `linker_elf.ld`), built to `kernel.bin`/`kernel.elf`, packed into `os.img` and bootable ISOs (`limine-iso.sh`).
Has a **SDK for user apps** (`sdk.h`, `SDK_GUIDE.md`): callbacks (on_paint/on_click/on_key/on_close), window/focus API, drawing primitives (SDK_FILL, SDK_TEXT, SDK_PIXEL), example app `app_calc_example.c`. The SDK guide is in Italian — do not translate code comments gratuitously; keep the existing style.

### How to build & run
```bash
cd ~/Desktop/vibeos
make                        # builds kernel.bin/elf, entry.o, etc.
./build-toolchain.sh        # (only when toolchain is missing) prepares the cross-compiler
./limine-iso.sh             # produce bootable ISO
./create-usb.sh             # write os.img / ISO to a USB stick
```
- Guest test images / vbe thunks present (`guest_2m.bin`, `vbe_thunk.asm`) — VBE graphics and guest-mode experiments are part of the repo.

### Conventions & quirks
- C + GNU as (AT&T vs Intel syntax: check each .asm — boot.asm and entry.asm differ in comments).
- Very low-level: edit VBE/graphics code with care (no screen = debug via serial/log or os.img inspection).
- `SDK_GUIDE.md` is the contract for user-space apps — any breaking change must update it too.
- `.omo/` exists here as well.

### Acceptance gate for vibeos changes
- `make` exits 0 with no new warnings for touched files.
- Boot artifacts regenerate (kernel.bin/os.img are produced, not hand-edited).
- If SDK changed: app_calc_example.c (or at least the SDK guide's examples) still compile.

---

## Cross-project rules
- Never confuse the two stacks: fountain is web (JS/Vite), vibeos is systems (C/asm/boot).
- Both have `.omo/` plan dirs — treat as decision records unless the user says otherwise.
- Both are personal/hobby projects: the user values forward motion and working demos over grand architecture documents.