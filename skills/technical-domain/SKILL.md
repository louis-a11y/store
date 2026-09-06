---
name: technical-domain
description: Technical expertise for the domains this user actually works in — browser/QR web tech (fountain) and low-level systems programming (vibeos: x86, boot, kernel, drivers, VBE graphics). Use when the work needs domain depth and correctness in these areas, or when scoping what's possible. Triggers: 'Web APIs', 'camera', 'QR', 'barcode', 'x86', 'assembly', 'bootloader', 'kernel', 'VBE', 'graphics mode', 'cross-compiler', 'limine', 'GRUB', low-level, systems programming.
---

# Technical Domain Depth

## Domain 1 — Browser + QR web tech (fountain)

### Camera & QR reality (get this right)
- **Secure context is mandatory**: `getUserMedia` (camera) and QR scanning over `http://` are blocked. That's WHY fountain ships `.certs/` and a `dev:https` script. Any local testing of camera features must use the https variant.
- **Camera APIs**: `navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })` for the rear camera (phones). Must handle: permission denial, no camera, `overconstrained` errors, and `torch`/tracks lifecycle (stop tracks when the scanner unmounts — otherwise the camera LED stays on).
- **QR decoding in JS**: jsqr (pure JS, no WASM) — feed it `ImageData` (grayscale RWTA). Performance: downscale the video stream before decoding (scan at ~640x480 max); full-HD frames are too slow.
- **QR generation**: qrcode npm lib renders to canvas/dataURL — keep quiet margins (quiet zone ≥ 4 modules) or real-world scanners fail.
- **Testing reality**: automated round trips (`test-roundtrip.mjs`) cover encode→decode logic; true camera paths need a real device or emulated camera. Playwright can fake `getUserMedia` via `--use-fake-ui-for-media-stream --use-fake-device-for-media-stream` or launch args; otherwise use controlmcp on a real browser.

### fountain-specific pitfalls
- ES modules, no framework — event wiring lives in app.js/main.js; add behavior by matching that orchestration style.
- Do not add npm deps casually: the user's stack is deliberately thin (vite + jsqr + qrcode only). Prefer a ~50-line utility over a new package.

## Domain 2 — Systems programming / OS dev (vibeos)

### The boot chain (how vibeos boots)
- `boot.asm` — the very first code (MBR/BIOS stage; real mode, 16-bit). `entry.asm` — 32-bit (or 64-bit) entry that hands off to the kernel. `boot.bin`/`entry.o` are intermediates; `kernel.bin`/`kernel.elf` are the deliverables.
- Two boot paths configured: **GRUB** (`grub.cfg`, legacy multiboot) and **limine** (`limine.conf`, modern boot protocol). limine handles long mode / higher-half mapping — if kernel.c expects virtual addresses, that's the limine path. Changes to one path must not break the other (test both ISOs).
- Yellow flags when low-level editing: segment registers in real mode, GDT/IDT setup, paging (PML4...) on 64-bit, and the transition order. `build-toolchain.sh` implies a custom cross-compiler; always `make` with it, never the host gcc for kernel code.

### Graphics / VBE (vibeos)
- VBE (VESA BIOS Extensions): `vbe_thunk.asm` + `vbe_thunk.h` = the real-mode thunk used to switch video modes from protected mode (classic pattern: realmode call via v86 or a bounce buffer).
- Framebuffer math: pixels at `fb + (y * pitch) + (x * bpp/8)`; pitch ≠ width×bpp/8 (alignment!). Clamp all drawing to the mode's dimensions — overdraw corrupts memory with no visible crash.
- If the user enables a higher mode (e.g. 1024x768@32): verify the thunk returns the new pitch and update every draw routine; stale pitch = stretched/garbled screen.

### The SDK contract (vibeos user-space)
- `sdk.h` + `SDK_GUIDE.md` = the ONLY supported way user apps touch the OS. Events are `on_paint(id, x, y, w, h)`, `on_click(id, mx, my, btn)`, `on_key(id, ch)`, `on_close(id)`; drawing via `SDK_FILL/SDK_TEXT/SDK_PIXEL`; windows via `focus_window`/visibility flags.
- Kernel changes MUST keep the SDK ABI stable or bump it explicitly and update SDK_GUIDE.md — app_calc_example.c is the canary.

## General rules
1. Give correct, current API details (Web APIs drift; verify with the controlmcp browser or docs when unsure).
2. When scoping: state what's hard vs risky honestly (e.g. "real-mode bootstrap is the fragile part, userspace is safe").
3. If a request mixes both domains (e.g. "scan a QR in vibeos"), flag the complexity early — that's two very different toolchains and will take real time.