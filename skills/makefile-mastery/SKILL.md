---
name: makefile-mastery
description: Use when writing, editing, or debugging GNU Makefiles — variables, automatic vars, pattern rules, phony targets, dependency tracking, link order. Grounded in vibeos/Makefile conventions.
---

## Goal
Write and debug GNU Makefiles confidently: correct variable/function syntax, automatic variables, dependency generation, parallel builds, and the linking traps specific to kernel builds.

## vibeos/Makefile conventions (match these)

- Variables uppercase: `CC = i686-elf-gcc`, `ASM = nasm`, `LD = i686-elf-ld`
- Flags: `CFLAGS`, `LDFLAGS_BIN`, `LDFLAGS_ELF`
- Target files: `os.img` ← `boot.bin kernel.bin` (binary concat via `cat` + `truncate -s 32M`)
- ELF variant: `kernel.elf` ← `entry.o kernel.o` with a DIFFERENT linker script
- `.PHONY` at the end listing all non-file targets (`all run debug iso ... clean`)

## Core syntax (quick reference)

```makefile
# Simple rule: target: prerequisites
kernel.o: kernel.c vbe_thunk.h
	$(CC) $(CFLAGS) kernel.c -o kernel.o

# Automatic variables
kernel.elf: entry.o kernel.o
	$(LD) $^ -o $@          # $@ = target, $^ = ALL prereqs, $< = FIRST prereq
	@echo "built $@"        # @ = silent
```

| Variable | Meaning |
|---|---|
| `$@` | Target name |
| `$<` | First prerequisite |
| `$^` | All prerequisites (deduped) |
| `$*` | Stem (matched part) |

## Common constructs

```makefile
# Wildcard + pattern rule for many sources
SRCS := $(wildcard src/*.c)
OBJS := $(SRCS:.c=.o)

%.o: %.c
	$(CC) $(CFLAGS) $< -o $@

# Phony (always run) targets
.PHONY: all clean run

# Conditionals
ifndef TOOLCHAIN
TOOLCHAIN := $(shell which i686-elf-gcc 2>/dev/null)
endif
```

## Makefile debugging

| Need | Command |
|---|---|
| Dry run (print, don't run) | `make -n` |
| See variables | `make -p \| grep -A1 <VAR>` or `$(info VAR=$(VAR))` |
| Force rebuild one target | `make -B kernel.o` |
| Parallel build | `make -j$(sysctl -n hw.ncpu)` (macOS!) |
| Don't delete intermediate files | `make -o file` or mark `.SECONDARY:` |
| Explain why target remade | `make -d` (verbose debug) |

## Kernel-build-specific traps

- **Link order matters**: `entry.o` FIRST (contains entry point / `_start`). `$(LD) kernel.o entry.o` breaks boot. Order = entry, then deps.
- **`-nostdlib` + no libc**: the final link must be `-nostdlib` or the ld will complain about missing `_start`/crt0.
- **Missing headers** = stale objects: add header deps (`kernel.o: kernel.c vbe_thunk.h`), or generate auto-deps (`-MMD -MP` in CFLAGS, include `*.d`).
- **vbe_thunk.h generated file**: its rule (`xxd -i vbe_thunk.bin > vbe_thunk.h`) must run BEFORE kernel.o compiles — declare it as a prerequisite (already in Makefile).
- **Parallel builds + generated headers**: `-j` can race rule order unless the dependency is declared. Always list the generated header as a prereq of the .o that includes it.
- **`truncate -s 32M`** for os.img: only works on files, not pipes; sequence `cat > os.img && truncate` is correct.

## Pitfalls

- Tab vs spaces: recipe lines MUST start with an actual TAB character. Copy-paste from chat often produces spaces → "missing separator" error.
- `make` treats `run`/`debug`/`iso` as file targets unless listed in `.PHONY` — if a file named `run` exists, the target never executes.
- On macOS multi-core: `-j$(sysctl -n hw.ncpu)` (not `nproc` — doesn't exist without coreutils).
- `.NOTPARALLEL:` if two rules write the same output — rare here, but the os.img cat+truncate pair is a sequence, don't parallelize it.