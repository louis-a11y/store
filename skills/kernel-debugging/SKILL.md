---
name: kernel-debugging
description: Use when debugging the vibeos kernel or other bare-metal x86 code — GDB over QEMU, breakpoints on symbols, register/FB inspection, triple-fault reading, printk-style tracing.
---

## Debug session (vibeos Makefile)

1. Terminal 1: `make debug` (runs `qemu-system-i386 ... -s -S`)
2. Terminal 2: `gdb kernel.bin` (or `gdb kernel.elf` for symbols from linker_elf.ld)
3. Inside GDB:
   ```
   target remote localhost:1234
   file kernel.bin          # already loaded via argv, but confirm
   break kmain              # C symbol
   break entry              # asm label from entry.asm
   continue
   ```
4. QEMU freezes at first instruction (`-S`); `continue` runs until breakpoint.

## GDB commands that matter for kernels

| Command | Use |
|---|---|
| `info registers` | All regs (EFLAGS, CR0/CR2/CR3 via `p $cr0` etc.) |
| `p/x *(int*)0xB8000` | Read VGA text memory directly |
| `x/40bx 0x100000` | Dump kernel memory after load (often loaded at 1M) |
| `x/8i $eip` | Disassemble around current instruction |
| `bt` | Backtrace (works if frame pointers / DWARF present) |
| `layout asm` / `layout src` | TUI split view |
| `break *0xFFFFFFE0` | Break on raw address (when no symbols) |
| `c` / `si` / `ni` | Continue / step instruction / next instruction |
| `monitor info registers` | QEMU monitor via GDB (if `-monitor` configured) |

## Symbols troubleshooting

- `symbol-file kernel.elf` — the ELF with debug info is the RIGHT file for symbols. `kernel.bin` (flat binary, `linker.ld`) has no DWARF — symbols come from `entry.o`/`kernel.o` only via the .elf build (`linker_elf.ld`).
- If `break kmain` says "function not defined", ensure you loaded `kernel.elf`, and that CFLAGS include `-g` (add it temporarily if missing: `CFLAGS += -g` in Makefile).
- `add-symbol-file kernel.o` works too if you have separate-section layout.

## Crash diagnosis without GDB

- **Triple fault / reset loop**: run `qemu-system-i386 ... -d int,cpu_reset -no-reboot -D /tmp/qemu.log`. The log's last entries show the faulting vector (e.g. `check_exception old=0x0e new 0x08` = page fault escalating to double fault → triple).
- **#PF (14)**: check CR2 (`p $cr2`) = faulting address; it's usually a bad pointer, wrong segment base, or unmapped page.
- **#GP (13)**: bad segment selector, non-canonical address, or privileged instruction in ring 0 misuse (e.g. `cli` before interrupts set up).
- **printk-style tracing**: simplest fix — write to VGA 0xB8000 (text mode) or toggle a pixel in VBE FB, plus `-serial stdio` and write to COM1 (port 0x3F8). Serial survives panics that kill the screen.

## Pitfalls

- Kernel runs at ring 0 — `stepi` into instructions like `sti`/`cli` changes global state; re-establish assumptions after stepping.
- Optimized code (`-O2` in CFLAGS): variables may be optimized out; use `-O0 -g` for a debug build (add a `debug` variant with `CFLAGS_DEBUG`).
- GDB on macOS Apple Silicon is aarch64-hosted but debugs i386-remote fine — i386 target support is built in.
- VBE framebuffer is linear memory; inspect with `p/x` on the FB address from the VBE mode info (per vibeos vbe_thunk). Content changes only after a repaint — single-step won't show intermediate states.
