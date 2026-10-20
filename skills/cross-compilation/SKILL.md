---
name: cross-compilation
description: Use when building a cross compiler or compiling freestanding code — i686-elf-gcc/gcc/ld toolchain, why host clang/gcc is wrong for kernels, sysroot-less freestanding builds. Grounded in vibeos (i686-elf-gcc, build-toolchain.sh, -nostdlib -ffreestanding).
---

## Why a cross compiler

- macOS's clang/ld target Mach-O for x86_64 darwin — it cannot emit raw i386 ELF binaries that GRUB/Limine/nasm boots.
- Host compiler injects: crt0/crti startup, stack protector, PIE, dynamic linking, libc headers — all poison for a kernel.
- vibeos solves it with: `CC = i686-elf-gcc`, `ASM = nasm`, `LD = i686-elf-ld` + the freestanding CFLAGS below.

## Toolchain state on this machine

- The project has `build-toolchain.sh` — read the script before assuming tools exist.
- Verify installed: `command -v i686-elf-gcc i686-elf-ld i686-elf-objdump` — if missing, run/confer with build-toolchain.sh.

## Baseline freestanding flags (match vibeos CFLAGS)

```
-m32 -ffreestanding -fno-builtin -fno-stack-protector -nostdlib -nostdinc -c -O2 -Wall
```

| Flag | Why |
|---|---|
| `-m32` | Emit i386 code |
| `-ffreestanding` | No hosted libc assumptions (no main(), no heap) |
| `-fno-builtin` | Don't replace calls with builtin memcpy etc. |
| `-fno-stack-protector` | Kernel has no __stack_chk_fail |
| `-nostdlib` | No crt0/crti/libc at link |
| `-nostdinc` | No host headers; use own (sdk.h, kernel.h) |
| `-O2` / `-g` | Tune: -O0 -g for debugging sessions |

## Linking: two scripts, one rule

- `LDFLAGS_BIN = -m elf_i386 -T linker.ld -nostdlib` → flat binary (boot.bin+kernel.bin → os.img)
- `LDFLAGS_ELF = -m elf_i386 -T linker_elf.ld -nostdlib` → ELF with symbols (GRUB/Limine)
- Same objects, different scripts: keep both rules (`kernel.bin` and `kernel.elf`) so `make` doesn't fight over one output.

## Assembly side

- `nasm -f elf32 entry.asm -o entry.o` → ELF object for linking
- `nasm -f bin boot.asm -o boot.bin` → raw bootloader (no ELF, direct 0x7C00 / custom load)
- `nasm -f bin vbe_thunk.asm` → 16-bit real-mode BIOS thunk blob (embedded via xxd → vbe_thunk.h)

## Building a fresh toolchain (if build-toolchain.sh is stale)

Hand-rolled (binutils + gcc, ~10-20 min):
```
brew install gmp mpfr libmpc       # gcc deps (binutils doesn't need them)
binutils:  ../binutils-2.4x/configure --target=i686-elf --prefix=/opt/i686-elf --disable-nls --disable-werror
gcc:       ../gcc-1x.x/configure --target=i686-elf --prefix=/opt/i686-elf --disable-nls --enable-languages=c --without-headers
make -j$(sysctl -n hw.ncpu) && make install
```
Or simpler: `brew install i686-elf-gcc` (formula exists for macOS) — prefer this unless a specific version is needed.

## Pitfalls

- **Never mix**: `gcc -m32` on macOS produces Mach-O/LLVM weirdness — even `-m32` doesn't give you ELF. Use the i686-elf-* family end to end.
- **`-nostdinc` means NO headers**: kernel.c includes kernel.h/sdk.h from the project — include paths must be explicit (`-I.` etc.).
- **Link order** (see makefile-mastery): entry.o first, else entry point unresolved or wrong.
- **as/ld naming**: on Sony macOS hosts, plain `as`/`ld` are the HOST ones — always use `i686-elf-as`/`i686-elf-ld` explicitly, or set CC/AS/LD vars (vibeos Makefile does exactly this).
- If `make` fails with "unrecognized option -m elf_i386", the host `ld` was used instead of `i686-elf-ld` (PATH shadowing or var clobbered).
