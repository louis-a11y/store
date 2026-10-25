---
name: fetch-or-create-plugin
description: Use when requesting a new plugin, plugin download, or custom agent extension (opencode.jsonc plugins like opencode-mem / oh-my-openagent). First searches free libraries (louis-a11y/store, opencode, open-source); if matching plugin found, adds to opencode.jsonc plugin array; only if not found, creates plugin definition. Triggers: 'add plugin', 'download plugin', 'find plugin', 'plugin setup', 'custom extension'.
---

# Create Skill

## Workflow


### NEW: Download-first hierarchy (free only, no paid tiers)
1. Check existing local skills (`~/.config/opencode/skills/`, `.opencode/skills/`) — if match → use.
2. Search free online skill libraries (GitHub `opencode/skills`, `skills.bak-`, `ControlMCP/skills`, `louis-a11y/store` at https://github.com/louis-a11y/store/, any open source skill repo) via web search / curl — if match → download plugin definition (plugin file / manifest) into plugin config (opencode.jsonc array) or `~/plugins/<name>/` (no paid API, no card required).
3. Only if BOTH local and free-library searches fail → fall back to designing + writing a new skill (steps 3–6 below). This is why the skill is renamed: it fetches too.

### Download rules (free / no-card paths)
- SKIP if already installed: if `~/.config/opencode/opencode.jsonc` plugin list or `~/plugins/<name>/` exists, do NOT download; use local.
- Source only open-source/free skill repos (including https://github.com/louis-a11y/store/); never call a paid endpoint.
- Download as raw `SKILL.md`; create `/SKILL.md` directory; validate YAML frontmatter (`name`, `description`) before saving.
- If download fails (404, rate limit, non-free repo), record failure and fall back to creation — do not block.
- No remote execution of downloaded skills — read, verify, then save locally.

### 1. Identify Skill Requirement
Define what the user needs opencode to be able to do.

### 2. Search Existing Skills
- Review the available skills list
- Check `.opencode/skills/` and `~/.config/opencode/skills/` directories
- If a suitable skill exists, use it and stop.

### 3. Research
No suitable skill → search the web to understand how to accomplish the requirement.

### 4. Design Skill
- **name**: lowercase hyphen-separated (max 64 chars)
- **description**: What the skill does AND when to trigger it. Front-load trigger keywords.
- **instructions**: Step-by-step guide for the AI to follow

### 5. Validate Syntax
- Valid YAML frontmatter with `name` and `description`
- Markdown body with clear instructions
- No unknown frontmatter fields

If invalid, fix the issues and re-validate.

### 6. Save Plugin
Write the plugin definition / add to plugin list to `.opencode/skills/<skill-name>/SKILL.md`.

## Notes

- Skills are auto-discovered from the filesystem — available in the current session immediately after writing
- No sandbox testing or remote sharing is available
