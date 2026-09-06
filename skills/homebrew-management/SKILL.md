---
name: homebrew-management
description: Use when managing macOS packages with Homebrew — installing, updating, cleaning up, troubleshooting brew errors, formulae vs casks, services. User's brew lives at /opt/homebrew (Apple Silicon).
---

## Goal
Keep Homebrew healthy, install/remove packages correctly, and fix common brew failures on Apple Silicon.

## Core commands

| Command | Purpose |
|---|---|
| `brew update` | Update Homebrew itself + formulae lists |
| `brew outdated` | List updatable packages |
| `brew upgrade` | Upgrade everything |
| `brew upgrade <pkg>` | Upgrade one |
| `brew install <pkg>` | Install formula (CLI tool, e.g. `brew install node`) |
| `brew install --cask <pkg>` | Install GUI app (e.g. `brew install --cask firefox`) |
| `brew uninstall <pkg>` | Remove |
| `brew list` | Installed formulae |
| `brew list --cask` | Installed casks |
| `brew search <query>` | Search |
| `brew info <pkg>` | Version, deps, caveats, bottle status |
| `brew cleanup` | Remove old versions + cached downloads |
| `brew doctor` | Diagnose problems (run FIRST when things are odd) |
| `brew services list` | Show services (e.g. mysql, postgres) |
| `brew services start/stop <svc>` | Manage a service |

## Tactics

- **Formula vs cask**: `brew install` = CLI/daemons. `--cask` = GUI apps in /Applications. Same name can exist as both (e.g. `docker` vs `docker --cask`).
- **Why run `brew doctor` first**: it catches clobbered dirs, permission issues, duplicate binaries — the cause of most "brew is broken" reports.
- **Cleanup cadence**: `brew cleanup --prune=7` keeps last 7 days of downloads. Old versions pile up silently.
- **Checking what auto-updates**: `brew autoupdate` if installed; otherwise brew auto-updates before every install by default (disable with `HOMEBREW_NO_AUTO_UPDATE=1`).
- **Degrading/edge installs**: `brew install <pkg>@<version>` for versioned formulae (e.g. `node@20`); pin with `<tap>/<pkg>`.

## Troubleshooting (Apple Silicon)

- **"zsh: command not found" but installed** → /opt/homebrew/bin not on PATH. Fix: add `eval "$(/opt/homebrew/bin/brew shellenv)"` to ~/.zshrc (or ensure /opt/homebrew/bin precedes /usr/bin).
- **Permission errors on /opt/homebrew** → `sudo chown -R $(whoami) /opt/homebrew` (own the prefix; avoid running brew with sudo).
- **Bottle "incompatible architecture"** → running arm64 brew on an arm64 Mac is default; this error usually means an x86_64 Homebrew install exists. Check `which brew` → should be /opt/homebrew (arm64), not /usr/local (intel).
- **Stuck "Updating Homebrew..."** → `HOMEBREW_NO_AUTO_UPDATE=1 brew install <pkg>` skips it; or `git -C /opt/homebrew/Library/Taps/homebrew/homebrew-core fetch --prune`.
- **"No available formula"** → tap missing: `brew tap homebrew/core` (rarely needed now) or the package moved — check `brew search`.

## Pitfalls

- Never `sudo brew install` — brew refuses and it breaks ownership.
- `brew upgrade` can break running services — check `brew services list` after big upgrades.
- Casks auto-update their own apps, so `brew outdated --cask` shows drift — it's normal.
- Uninstall with `--zap` on casks to also remove app data (irreversible — confirm first).