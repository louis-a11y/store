---
name: opencode-usage
description: This user's exact opencode setup — config file, plugins, MCP servers, skills, restart/reload mechanics, and known quirks. Use when configuring or troubleshooting opencode on this machine, explaining how their setup works, or applying changes that need a restart. Triggers: 'opencode config', 'change my opencode', 'hot reload', 'restart opencode', 'oc-reload', 'plugins', 'MCP', 'skills on this machine', 'why is opencode doing X'.
---

## Config layout (authoritative)
- **Global config**: `~/.config/opencode/opencode.jsonc` (NOT `~/.opencode/`, NOT `opencode.json`).
- Config is loaded ONCE at startup. **It is NOT hot-reloaded.** Any change (opencode.jsonc, skills, agents, commands, plugins) requires a restart.

## Current global config
- **Plugins**: oh-my-openagent (LSP daemons spawn as node processes), opencode-mem.
- **MCP**: `control` → local, command `/Users/superlouisyt/tools/ControlMCP/.venv/bin/control-mcp`. Other servers enabled at runtime: context7, grep_app, websearch, playwright, codegraph (disabled). Check with the TUI `/status`.
- **Permission**: every `control_*` tool is pre-allowed → NEVER ask the user before control actions.

## Restart mechanics (use these, don't fight the process)
- `oc` (alias in ~/.zshrc) = `opencode -c` → resume last session in a NEW terminal.
- `~/bin/oc-reload` = kill running opencode TUI, sleep 1, relaunch with `-c` → poor man's hot reload. **Run it from a NEW terminal, not from inside the TUI.**
- After changing any config, skill, or plugin: tell the user to run `oc-reload` from another terminal. Do NOT try to force a reload from inside the session.

## Skills on this machine
- Global skills directory: `~/.config/opencode/skills/<name>/SKILL.md`.
- Existing skills: about-me, controlmcp, opencode-usage, dev-workflow, project-workflow, daily-routine, product-domain, technical-domain, + user-supplied ones (computer-control, create-skill, opencode-capabilities, work-faster).
- Every skill needs `name` (lowercase-hyphen) + `description` (what + when to trigger). Skills without a description are filtered out.
- New skill = new folder `~/.config/opencode/skills/<name>/SKILL.md`. Available after opencode restart.

## Session persistence
- Sessions live in the `session` table of `~/.local/share/opencode/opencode.db` (SQLite: `opencode.db`, `.db-wal`, `.db-shm`).
- `opencode -c` resumes the MOST RECENT session (global "continue" pointer).
- `opencode -s <session-id>` resumes a specific session.
- The DB is the source of truth: use `session_list`/`session_info`/`session_read`/`session_search` tools to inspect history before assuming anything about past work.

## Known quirks & pitfalls
- **PID 35833-class issue**: `pkill -x opencode` matches the process name exactly; `opencode serve` (headless) is also named `opencode` and would be killed too. oc-reload documents this.
- **Two instances, one live session = "Unexpected server error"**. Never start a second TUI with `-c` while the same session is already open. Kill first, then resume.
- **MCP client eviction**: opencode bug #17099 can permanently evict an MCP client (e.g. `control`) on a transient `listTools()` failure. Symptom: a control tool errors out and stays dead. Fix: restart opencode.
- opencode is installed via Homebrew (`/opt/homebrew/Cellar/opencode/<version>/bin/opencode`) — `brew upgrade` overwrites it. The upstream binary has NO config reload: `/reload`, `/restart`, `config/reload` do not exist. Don't pattern-match them from other tools.

## Best practices on this box
1. Before editing or assuming a capability: check the active config (`cat opencode.jsonc` — it's tiny) + `/status` — don't guess.
2. For desktop/browser work: use the controlmcp skill (this user's `control` MCP).
3. For "what can opencode do" questions: point to the opencode-capabilities + customize-opencode skills rather than improvising.
