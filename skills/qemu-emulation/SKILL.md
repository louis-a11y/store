---
name: qemu-emulation
description: Use when emulating or running the vibeos kernel / ISOs in QEMU on macOS — raw disk, GRUB ISO, Limine ISO, UEFI, networking. Grounded in the vibeos Makefile targets (run, run-grub, run-grub-uefi, run-limine, debug).
---

## The canonical commands (from vibeos/Makefile)

| Target | Command | What it boots |
|---|---|---|
| `make run` | `qemu-system-i386 -drive file=os.img,format=raw,index=0,media=disk -m 256 -vga std -device e1000,netdev=net0 -netdev user,id=net0` | Custom bootloader raw disk, 32M, e1000 NIC |
| `make debug` | same drive but `-s -S` | Same + GDB stub (see kernel-debugging) |
| `make run-grub` | `qemu-system-i386 -cdrom vibeos.iso -m 128 -boot d` | GRUB BIOS ISO |
| `make run-grub-uefi` | `qemu-system-x86_64 -cdrom vibeos.iso -m 128 -bios /opt/homebrew/share/qemu/OVMF.fd -boot d` | GRUB UEFI ISO (x86_64 emu) |
| `make run-limine` | `qemu-system-i386 -cdrom vibeos-limine.iso -m 256 -boot d` | Limine BIOS ISO |

## Key flags explained

- `-drive file=os.img,format=raw,index=0,media=disk` — raw disks need `format=raw` or QEMU guesses wrong
- `-m 256` — RAM in MB
- `-vga std` — standard VGA (needed for VBE)
- `-s -S` — `-s` = GDB server on tcp::1234, `-S` = freeze CPU on start (wait for `continue`)
- `-cdrom X.iso -boot d` — boot from CD
- `-bios <OVMF.fd>` — UEFI firmware (OVMF); brew installs under `/opt/homebrew/share/qemu/`
- `-netdev user,id=net0 -device e1000,netdev=net0` — user-mode network (no root needed)

## UEFI on this machine

- OVMF.fd locations checked (in order): `/opt/homebrew/share/qemu/OVMF.fd`, then `/usr/share/qemu/OVMF.fd`, else "brew install qemu".
- `make run-grub-uefi` uses `qemu-system-x86_64` because OVMF is x86_64 firmware.

## Useful extras

| Need | Add |
|---|---|
| Serial console | `-serial stdio` (then kernel writes to COM1 appear in terminal) |
| Silent-reset / triple-fault log | `-d int,cpu_reset -no-reboot -D /tmp/qemu.log` — log's last entries show the faulting vector; most common: #GP (13) / #PF (14) / triple fault (vector 8 double-fault loop) |
| More RAM/cores | `-m 512 -smp 2` |
| Snapshot (don't persist disk) | `-snapshot` |

## Pitfalls

- Mixing `-kernel` (multiboot raw kernel.bin) with the custom bootloader build does NOT work — the boot.bin path needs `-drive`, not `-kernel`.
- If the screen stays black with `-vga std`, the kernel may be in VBE mode before the driver initializes — check serial output first.
- Mouse grab: `Ctrl+Alt+G` releases the pointer; `Ctrl+Alt+1/2/3` switches monitor/serial/network views.
- Apple Silicon: `qemu-system-i386` is TCG-only (no KVM) — slow is normal. A 32-bit x86 emu boots in ~1-3s, not instant.
