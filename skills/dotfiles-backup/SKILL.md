---
name: dotfiles-backup
description: Use when backing up, versioning, or restoring dotfiles — ~/.zshrc, ~/.config/opencode/, ~/bin/ — to git, restoring on a new machine, symlink strategy.
---

## Goal
Keep the user's machine config (shell, opencode, scripts, skills) versioned in git so a new machine can be configured in minutes — and keep ~/bin + skills synced.

## What matters on this machine

| Path | Why |
|---|---|
| `~/.zshrc` | PATH + oc alias |
| `~/bin/` | oc-reload + any personal scripts |
| `~/.config/opencode/` | opencode.jsonc config, skills/ (ALL skills live here) |
| `~/tools/ControlMCP/` | ControlMCP MCP server source + venv (bigger; maybe separate repo) |

## Recommended layout

```
~/dotfiles/
  .zshrc          # symlink -> ~/.zshrc
  .config/opencode/  # symlink -> ~/.config/opencode
  bin/            # symlink each script or the dir
  README.md
```

## Setup on this machine

```bash
mkdir -p ~/dotfiles && cd ~/dotfiles
git init
# Move (don't copy) the files into place:
mv ~/.zshrc ~/dotfiles/.zshrc
ln -s ~/dotfiles/.zshrc ~/.zshrc
mv ~/.config/opencode ~/dotfiles/.config/opencode
ln -s ~/dotfiles/.config/opencode ~/.config/opencode
mv ~/bin ~/dotfiles/bin
ln -s ~/dotfiles/bin ~/bin
# Verify everything still resolves:
zsh -n ~/.zshrc && alias oc && command -v oc-reload
git add -A && git commit -m "Initial dotfiles"
# Private repo (contains no secrets if config holds none — CHECK opencode.jsonc for tokens)
```

## Restore on a new machine

```bash
git clone <url> ~/dotfiles
ln -s ~/dotfiles/.zshrc ~/.zshrc
ln -s ~/dotfiles/.config/opencode ~/.config/opencode
ln -s ~/dotfiles/bin ~/bin
```

## Skill sync

- Skills live in `~/.config/opencode/skills/` — they're plain folders with SKILL.md; they version in git like everything else.
- New skills are picked up on opencode restart (`/exit` + `oc` in the same terminal).

## Pitfalls

- **Secrets**: grep for tokens/keys before committing. opencode.jsonc may hold MCP auth/API keys — if so, use `opencode.jsonc` in the repo but put secrets in an ignored file or env vars.
- Symlink the DIR or the FILE, not both — `ln -s ~/dotfiles/bin ~/bin` (whole dir) is simplest and keeps PATH stable.
- `.gitignore` the ControlMCP venv (hundreds of MB) — track only the source (tools/ControlMCP/src).
- After moving config: re-run `brew doctor`/`opencode` once to confirm nothing referenced absolute old paths.
- If dotfiles already exist on the new machine, back them up first: `mv ~/.zshrc ~/.zshrc.bak`.