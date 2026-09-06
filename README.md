# Skill Store

A curated pack of 36 [opencode](https://opencode.ai) skills, written and battle-tested by someone who actually uses them daily — not scraped or auto-generated. Skills are plain `SKILL.md` files plus supporting references. Fork them, edit them, vendor them — they're yours.

## Install

**Recommended — opencode HTTP catalog** (one line in `opencode.json` / `opencode.jsonc`):

```jsonc
{
  "skills": [
    "https://raw.githubusercontent.com/louis-a11y/store/main/skills"
  ]
}
```

Skills are cached and refresh automatically when a skill's content changes (version = content hash, see `scripts/build-index.py`).

**Manual** — clone and copy straight into your global skills dir:

```bash
git clone https://github.com/louis-a11y/store.git
mkdir -p ~/.config/opencode/skills
cp -R skills/* ~/.config/opencode/skills/
```

That's it — the next session picks them up. No restart, no registration. If you use `.claude/skills` or `.agents/skills`, the same folders work there too — the format is portable across every major coding agent.

## Skills

### Core agent discipline

| Skill | What it does |
|---|---|
| `dev-workflow` | Coding discipline — structure, verification gates, commit quality |
| `error-analysis` | Failure protocol — repro first, 3+ hypotheses, bisect, root cause |
| `test-strategy` | What to test and how — behavior-first, round-trip/E2E, TDD for bugs |
| `prompt-engineering` | Writing instructions for AI agents — context-first, explicit success criteria |
| `subagent-delegation` | Orchestrating parallel subagents without duplicate work |
| `context-management` | Keeping sessions lean — targeted reading, pruning, delegation |
| `session-handoff` | Ending/resuming/transferring sessions cleanly |
| `work-faster` | Parallel execution, context optimization, task decomposition |
| `rapid-prototyping` | Vertical-slice PoCs — hardcode then generalize |
| `create-skill` | Creating new skills by researching, designing, validating |
| `regex-crafting` | Writing and debugging regular expressions |
| `memory-notes` | Recording/recalling project knowledge with opencode-mem |
| `terse-communication` | Terse, direct communication style — tables over prose |
| `opencode-capabilities` | Reference for everything opencode can do |

### Bare-metal systems (the niche)

| Skill | What it does |
|---|---|
| `cross-compilation` | i686-elf cross toolchain, freestanding builds, why host gcc is wrong |
| `makefile-mastery` | GNU Make — variables, pattern rules, dependency tracking, link order |
| `elf-binutils` | objdump/readelf/nm/objcopy for ELF32 kernels and flat-bin bootloaders |
| `kernel-debugging` | GDB over QEMU, breakpoints, register/FB inspection, triple-faults |
| `qemu-emulation` | Running kernels/ISOs in QEMU — raw disk, GRUB, Limine, UEFI |
| `technical-domain` | Browser/QR web tech + low-level x86 systems domain depth |

### macOS & shell

| Skill | What it does |
|---|---|
| `macos-automation` | macOS-native CLI automation — osascript, screencapture, defaults |
| `homebrew-management` | Installing, updating, troubleshooting brew on Apple Silicon |
| `shell-productivity` | zsh aliases, PATH, history, command-line speed |
| `dotfiles-backup` | Backing up/restoring dotfiles to git, symlink strategy |

### Web (fountain)

| Skill | What it does |
|---|---|
| `vite-workflow` | Vite dev server, HTTPS certs, build/preview, plain-JS setup |
| `web-performance` | Bundle size, scanning perf, Lighthouse, profiling |
| `browser-automation` | Real-browser verification with Playwright |
| `api-testing` | curl recipes, jq, status codes, smoke tests |

### Personal operating setup

> Published as-is per the author's call. Reference implementations of what a well-tuned agent setup looks like.

| Skill | What it does |
|---|---|
| `about-me` | User identity, environment, work-style preferences |
| `daily-routine` | Day-to-day session workflow — resume, skills, MCP |
| `opencode-usage` | A complete opencode config, documented |
| `project-workflow` | Two real projects' conventions (QR web app + custom OS) |
| `product-domain` | Product/vision thinking grounded in real projects |
| `controlmcp` | Operating a macOS desktop via ControlMCP |
| `computer-control` | Desktop automation — screenshots, clicks, windows |
| `knowledge-base` | KB workflow — querying, appending, ingest |

## Update workflow

Skills change. After editing any skill:

```bash
python3 scripts/build-index.py   # regenerates skills/index.json with fresh content hashes
```

Commit and push — opencode clients refresh their cached copies automatically.

## License

MIT — see [LICENSE](LICENSE).