---
name: elf-binutils
description: Use when inspecting ELF/i686 binaries with GNU binutils — objdump, readelf, nm, objcopy, ld — for bare-metal x86 (ELF32, i686-elf), bootloaders (flat bin), and cross-compiled systems (vibeos, embedded, custom OS). General i686-elf / objdump / readelf / nm / objcopy / size / xxd workflows, plus vibeos-specific notes preserved below.
---

## Which tool when

| Tool | Job | Example |
|---|---|---|
| `readelf` | ELF structure: headers, sections, segments | `readelf -h kernel.elf`, `readelf -S`, `readelf -l` (segment → where it loads) |
| `objdump` | Disassemble + section dump | `objdump -d kernel.elf` (asm), `objdump -h` (sections) |
| `nm` | Symbol table (names + addresses) | `nm kernel.elf \| grep kmain` |
| `objcopy` | Convert ELF → flat binary / extract sections | `objcopy -O binary kernel.elf kernel.bin` |
| `size` | Section sizes | `size kernel.elf` |
| `xxd` | Hex dump (used for vbe_thunk.h) | `xxd -i vbe_thunk.bin > vbe_thunk.h` |

## vibeos-specific inspections

```bash
# Where does the kernel's .text start? (linker_elf.ld decides load addr)
readelf -l kernel.elf        # check LOAD segments' Virtual Address

# Verify entry point matches linker script
readelf -h kernel.elf | grep Entry

# Disassemble just the entry code (first bytes: jump to kmain)
objdump -d kernel.elf | head -40

# Confirm boot.bin (custom bootloader) is a flat 512/1000-byte blob
ls -l boot.bin kernel.bin && file boot.bin kernel.bin

# vbe_thunk: check the raw real-mode blob made it into the header
head -20 vbe_thunk.h
```

## Common operations

- **Extract a section**: `objcopy --dump-section .text=/tmp/text.bin kernel.elf`
- **Full disasm with source**: `objdump -dS kernel.elf` (needs build with -g)
- **Symbols by size**: `nm -S --size-sort kernel.elf | tail` (find big functions)
- **Undefined symbols** (should be ~none for freestanding): `nm -u kernel.o`
- **Check for .note.GNU-stack / NX issues** (grub multiboot warns): `readelf -S kernel.elf | grep -i stack`

## Why this matters for the build

- `linker.ld` (bin) vs `linker_elf.ld` (ELF): bin layout has no headers — `objdump` can't read `kernel.bin`; disassemble with `objdump -b binary -m i386 -D kernel.bin` (flat binary has no load address — mentally add the link base).
- `vbe_thunk.h` is generated from a binary via `xxd -i` — any change to vbe_thunk.asm requires rebuilding the header (`make` handles it via the vbe_thunk.h rule).

## Pitfalls

- **i686 vs aarch64 tools**: readelf/objdump must match the target. Use `i686-elf-objdump`/`i686-elf-readelf` if plain GNU binutils refuses ("file format not recognized") — mac binutils sometimes lacks ELF32 i386.
- `objdump -d` on ELF with no debug info still shows symbols for global functions (from symtab) — local statics may be missing without -g.
- Don't confuse `vbe_thunk.bin` (16-bit real-mode code, runs before pmode) with kernel code — disassemble with `-m i8086` if inspecting it.
