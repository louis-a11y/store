---
name: about-me
description: The user's identity, environment, preferences, and projects. Use when you need to know who the user is, how they like to work, their machine setup, or what projects they maintain. Triggers: 'who am i', 'about me', 'my preferences', 'my setup', personalization, tailoring responses to the user, deciding how much confirmation to ask for.
---

# About the User

## Identity
- **Username**: superlouisyt
- **Language**: English (does NOT read Chinese — translate anything Chinese, never show raw Chinese text)
- **Timezone**: Europe/Rome (device locale en-US)
- **Machine**: macOS (darwin), Apple Silicon, shell /bin/zsh

## Work Style Preferences (IMPORTANT — these override generic behavior)
- **Do NOT ask for confirmation on routine actions.** Ask only before **irreversible or destructive** actions (deleting data, force pushes, mass renames, irreversible config changes) or genuinely ambiguous choices — batch into at most ONE question per real fork, with a recommended default. Otherwise: proceed, note the assumption, keep going.
- They are terse; match their brevity. No fluff, no status updates, no "great question" openers, no summaries unless asked.
- They sweet-talk the AI ("i'd do only ask if its irreversible stuff / the other stuff allow") — interpret leniently toward action.
- Prefers quick iteration over exhaustive planning for small tasks. For big tasks, decompose and parallelize.

## Environment
- **Shell**: /bin/zsh, config at ~/.zshrc
- **Homebrew** for system packages
- **Custom bins**: ~/bin on PATH (e.g. ~/bin/oc-reload)
- **Editor/agent**: opencode (TUI). Sessions resume with `oc` (alias for `opencode -c`) or `oc-reload` (kill + relaunch resumed).
- **Projects root**: ~/Desktop/progetti/ (most) and ~/Desktop/ (some, e.g. vibeos)

## Projects
| Project | Path | What it is |
|---|---|---|
| fountain | ~/Desktop/progetti/fountain | Vite app (QR + WebCamera front-ends; jsqr + qrcode deps), has a static "web app" folder with HTML gallery/audio, .certs/ for https dev, run.sh, test-roundtrip.mjs |
| vibeos | ~/Desktop/vibeos | Homebrew-baked OS project: own kernel (kernel.c/h), boot.asm + entry.asm, GRUB & limine boot flows, Makefile, os.img, SDK_GUIDE.md, sdk.h, example apps (app_calc_example.c), usb/iso build scripts |

## AI setup preferences
- Wants their opencode install to be a capable assistant, not a random vibe coder: skills, MCP, orchestration all encouraged.
- Desktop control via ControlMCP is installed and allowed (permission.control_*: allow).
- Keep global AI config in ~/.config/opencode/opencode.jsonc; custom skills in ~/.config/opencode/skills/.

## How to behave with them
Act first (ask only when irreversible/ambiguous), be concise, and use the right project context: fountain for web/QR work, vibeos for OS/kernel/systems work. Don't confuse the two.
