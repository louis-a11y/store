---
name: opencode-capabilities
description: Reference guide for everything opencode can do. Use when the user asks what opencode is capable of, how to use a specific feature, wants to configure opencode deliberately (not vibe-coding), or needs help choosing the right workflow, agent, command, or tool for the job. Triggers: 'what can opencode do', 'opencode features', 'how do i use opencode', 'set up opencode', 'power user', 'capabilities'.
---

# OpenCode Capabilities

## Interfaces

| Interface | When to use |
|-----------|-------------|
| Terminal TUI | Default. Full-featured: themes, keybinds, sessions, agents |
| Web (opencode.ai) | Remote/cloud IDE |
| IDE extension | In-editor workflows |
| CLI (`opencode ...`) | Scripting, batch, non-interactive |

## Core Modes

- **Build mode** (default, Tab): Full tool access, makes changes
- **Plan mode** (Tab to switch): Analysis + planning only, no edits. Perfect for designing before implementing
- **Auto-detect**: Use plan first for big features, then build

## Built-in Agents

**Primary** (cycle with Tab):
- `build` - Default, all tools. Standard dev work
- `plan` - Restricted to analysis. Plan mode agent. Use to review code or design before changes

**Subagents** (invoke with `@mention` or auto):
- `general` - Research + multi-step tasks, full tools
- `explore` - Fast read-only codebase search
- `scout` - External docs & dependency research (read-only)

**Hidden** (run automatically): `compaction`, `title`, `summary`

## Agent Configuration

Create custom agents via:
- `opencode agent create` (interactive)
- `.opencode/agents/<name>.md` (global: `~/.config/opencode/agents/`)
- `agent: {}` in opencode.json

Key options: `description` (required), `mode` (primary/subagent/all), `model`, `permission`, `temperature`, `top_p`, `steps`, `hidden`, `color`, `disable`.

## Skills

- Reusable instruction playbooks in `SKILL.md` format; frontmatter `name` (required) + `description` (effectively required, drives triggering)
- Locations: project `.opencode/skills/`, global `~/.config/opencode/skills/`, external `~/.claude/skills/`, `~/.agents/skills/` — register extra paths via `skills.paths` in opencode.json
- Skill inventory: `opencode skill` family of commands

## Commands (Slash Commands)

Built-in: `/init` (AGENTS.md), `/connect` (auth), `/undo`, `/redo`, `/share`, `/help`, `/models`, more.

Custom commands: `.opencode/command/<name>.md` or global `~/.config/opencode/command/<name>.md`. Frontmatter: `description`, `agent`, `model`. Body = prompt template with `$ARGUMENTS`.

## Configuration (opencode.json)

| Section | Purpose |
|---------|---------|
| `model` / `small_model` | Default models |
| `agent` | Agent definitions/overrides |
| `command` | Custom commands |
| `skills` | Extra skill locations |
| `mcp` | MCP server connections |
| `plugin` | Plugin loading |
| `permission` | Tool access control |
| `provider` / `disabled_providers` | LLM providers |
| `references` | External docs/Git repos as context |
| `instructions` | AGENTS.md loading |
| `formatter` / `lsp` | Formatting & language servers |
| `theme` / `keybind` | UI customization |

Project config: `./opencode.json` or `.opencode/opencode.json`. Global: `~/.config/opencode/opencode.json`. Validate with `$schema: https://opencode.ai/config.json`.

## Agent Tool Surface

- **File ops**: `read`, `write`, `edit`, `apply_patch`, `glob`, `grep`, `list`
- **Exec**: `bash` (arbitrary shell)
- **Delegation**: `task` (spawn subagents)
- **Research**: `webfetch`, `websearch`, `scout`
- **Code intelligence**: LSP tools (`lsp_diagnostics`, `lsp_symbols`, goto/rename/references)
- **Structure**: `todowrite`/`todoread` (task tracking)
- **Memory**: project memory system (store/retrieve knowledge)
- **Sessions**: session list/read/search/resume, `/handoff` for context transfer
- **MCP tools**: anything a connected server exposes (e.g. Playwright browser automation, Context7 docs)
- **Skill**: load skills on demand

## Permissions Model

Each tool permission: `allow` | `ask` | `deny`.
Keys: `read`, `edit`, `glob`, `grep`, `list`, `bash`, `task`, `external_directory`, `todowrite`, `webfetch`, `websearch`, `lsp`, `skill`, `question`.
Pattern matching: last matching rule wins, put `*` first, specifics after.
Per-agent `permission` overrides top-level.

## Planned Workflows (Not Vibe-Coding)

1. **Init** → `/init` creates AGENTS.md so opencode knows the project
2. **Question** → `@file` mentions + Plan mode analysis
3. **Big task** → decompose into parallel subagents (`general`/`deep`), review each
4. **Mistake** → `/undo` / `/redo`
5. **Share** → `/share` for conversation links
6. **Handoff** → `/handoff` to continue work in a fresh session

## SDK & Extensibility

- **SDK**: TypeScript SDK for building on opencode
- **Server**: headless server mode
- **Plugins**: `.opencode/plugin/*.ts` + npm packages; hook into events, config, tool execution
- **Custom tools**: define your own tools
- **MCP/ACP**: connect external tool servers
- **References**: link external Git repos/docs as always-available context

## Model Management

- Any provider: Anthropic, OpenAI, Google, opencode Zen, local models, etc.; `model` = `provider/model-id` format
- Route models per agent (`agent.<name>.model`); `opencode models` lists available; Zen = curated, tested model list

## Diagnosing Problems

- Broken config → `OPENCODE_DISABLE_PROJECT_CONFIG=1` to start anyway
- `OPENCODE_CONFIG=/path/to/config.json` extra config
- `OPENCODE_CONFIG_CONTENT='...'` inline config injection
- LSP issues → `lsp` permission keys, per-language servers
- Troubleshooting docs: opencode.ai/docs/troubleshooting
