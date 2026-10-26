---
name: vibeos-review
description: Review vibeos kernel / boot / OS code for correctness, cross-compilation, and bare-metal errors. Triggers: review vibeos, kernel review, bootloader check, elf check.
---
# Vibeos Review (Domain-Specific)

Scope: `vibeos/` source — kernel, bootloader, drivers, VBE graphics, cross-compiler (i686-elf). Use `elf-binutils` skill + `cross-compilation` skill + `kernel-debugging`.

Checklist: ELF32 correct (`readelf`), linker order (Makefile), cross-compile flags (`-ffreestanding -nostdlib`), QEMU emulation passes (`qemu-emulation`), no triple-fault.

Source check: free (repo-local); no paid tools.
