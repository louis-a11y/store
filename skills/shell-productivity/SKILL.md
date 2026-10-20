---
name: shell-productivity
description: Use when working in the shell — zsh aliases, PATH problems, functions, history, command-line speed. Covers the user's zsh on macOS (darwin, Apple Silicon), including the oc/oc-reload workflow.
---

## The user's setup (verify, don't assume)

- `~/.zshrc` currently has:
  - `export PATH="$HOME/bin:$PATH"` — personal scripts dir FIRST
  - `alias oc='opencode -c'` — resume last opencode session
- Scripts live in `~/bin/` (e.g. `oc-reload`: pkill opencode, sleep 1, exec opencode -c)
- After ANY edit to ~/.zshrc: `source ~/.zshrc` or open a new terminal. `zsh -n ~/.zshrc` to syntax-check first.

## Pattern for adding a command

1. Script goes in `~/bin/<name>`, `chmod +x` — automatically on PATH, available in every shell, even non-interactive.
2. Alias only for interactive conveniences (never in scripts — aliases don't expand in non-interactive shells by default).
3. Verify: `command -v <name>` (not `which`, which can lie about aliases).

## Must-know zsh

| Topic | Command |
|---|---|
| History search | `Ctrl+R` (reverse), `Ctrl+S` (forward, if enabled) |
| Edit current line | `Ctrl+X Ctrl+E` (opens $EDITOR) |
| Re-run last command | `!!` |
| Last arg of last command | `!$` |
| Glob: recursive | `**/*.js` |
| Brace expansion | `{1..10}`, `{a,b,c}.txt` |

## PATH debugging

- `echo $PATH | tr ':' '\n'` — see order
- `type -a <cmd>` — where it resolves from + aliases
- `command -v <cmd>` — first hit
- Problem: command exists but wrong version → check PATH order; ~/bin and /opt/homebrew/bin should precede /usr/bin.
- `hash -r` after moving/installing binaries (zsh caches command paths).

## Pitfalls

- Never `cd` + `&&` chains in scripts run from arbitrary dirs — use `workdir` or absolute paths.
- `rm -rf` — always explicit paths, no variables that could be empty (`rm -rf $VAR/` with empty VAR nukes cwd).
- Aliases don't survive `sudo`, non-interactive ssh, or `#!/bin/sh` scripts — use full paths there.
- `set -e` in scripts: check `grep -R PATTERN` exit codes — grep returns 1 when nothing matches, which kills the script.
- macOS ships old bash (3.2); use zsh (default) or install modern bash via homebrew if portability matters.
