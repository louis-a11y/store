---
name: technical-domain
description: Technical expertise for the domains this user actually works in — browser/QR web tech (fountain) and low-level systems programming (vibeos: x86, boot, kernel, drivers, VBE graphics). Use when the work needs domain depth and correctness in these areas, or when scoping what's possible. Triggers: 'Web APIs', 'camera', 'QR', 'barcode', 'x86', 'assembly', 'bootloader', 'kernel', 'VBE', 'graphics mode', 'cross-compiler', 'limine', 'GRUB', low-level, systems programming.
---

# Technical Domain Depth

## Domain 1 — Browser + QR web tech (fountain)

### Camera & QR reality (get this right)
- **Secure context mandatory**: `getUserMedia` (camera) and QR scanning over `http://` are blocked — that's why fountain ships `.certs/` + a `dev:https` script. Local camera testing MUST use the https variant.
- **Camera APIs**: `navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })` for rear camera (phones). Handle: permission denial, no camera, `overconstrained`, `torch`, and track lifecycle (stop tracks on scanner unmount — else the camera LED stays on).
- **QR decoding**: jsqr (pure JS, no WASM) — feed `ImageData` (grayscale RGBA). Perf: downscale before decoding (~640x480 max; full-HD too slow).
- **QR generation**: qrcode npm lib → canvas/dataURL. Keep quiet zone ≥ 4 modules or real-world scanners fail.
- **Testing**: `test-roundtrip.mjs` covers encode→decode; true camera paths need a real/emulated device. Playwright can fake `getUserMedia` via `--use-fake-ui-for-media-stream --use-fake-device-for-media-stream` launch args; otherwise controlmcp on a real browser.

### fountain-specific pitfalls
- ES modules, no framework — event wiring lives in app.js/main.js; match that orchestration style.
- No casual npm deps: stack is deliberately thin (vite + jsqr + qrcode only). Prefer a ~50-line utility over a package.

## Domain 2 — Systems programming / OS dev (vibeos)

### The boot chain
- `boot.asm` — first code (MBR/BIOS stage; real mode, 16-bit). `entry.asm` — 32/64-bit entry handing off to kernel. `boot.bin`/`entry.o` = intermediates; `kernel.bin`/`kernel.elf` = deliverables.
- Two boot paths: **GRUB** (`grub.cfg`, legacy multiboot) and **limine** (`limine.conf`, modern protocol; handles long mode / higher-half mapping — if kernel.c expects virtual addresses, that's the limine path). A change must not break the other (test both ISOs).
- Yellow flags when low-level editing: segment registers in real mode, GDT/IDT, paging (PML4...) on 64-bit, transition order. `build-toolchain.sh` = custom cross-compiler; always `make` with it, never host gcc for kernel code.

### Graphics / VBE (vibeos)
- VBE (VESA BIOS Extensions): `vbe_thunk.asm` + `vbe_thunk.h` = real-mode thunk to switch video modes from protected mode (realmode call via v86 or bounce buffer).
- Framebuffer math: pixels at `fb + (y * pitch) + (x * bpp/8)`; pitch ≠ width×bpp/8 (alignment!). Clamp all drawing to mode dimensions — overdraw corrupts memory with no visible crash.
- Higher mode (e.g. 1024x768@32): verify the thunk returns the new pitch and update every draw routine; stale pitch = stretched/garbled screen.

### The SDK contract (vibeos user-space)
- `sdk.h` + `SDK_GUIDE.md` = the ONLY supported way user apps touch the OS. Events: `on_paint(id, x, y, w, h)`, `on_click(id, mx, my, btn)`, `on_key(id, ch)`, `on_close(id)`; drawing via `SDK_FILL/SDK_TEXT/SDK_PIXEL`; windows via `focus_window`/visibility flags.
- Kernel changes MUST keep the SDK ABI stable or bump it explicitly + update SDK_GUIDE.md — app_calc_example.c is the canary.

## General rules
1. Give correct, current API details (Web APIs drift; verify with the controlmcp browser or docs when unsure).
2. When scoping, state what's hard vs risky honestly (e.g. "real-mode bootstrap is the fragile part, userspace is safe").
3. Mixed-domain requests (e.g. "scan a QR in vibeos") — flag the complexity early: two very different toolchains, real time required.
