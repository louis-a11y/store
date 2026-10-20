---
name: create-skill
description: Use when the user requests a capability that no existing skill provides. Creates a new opencode skill by researching, designing, validating, and saving it.
---

# Create Skill

## Workflow

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

### 6. Save Skill
Write the skill file to `.opencode/skills/<skill-name>/SKILL.md`.

## Notes

- Skills are auto-discovered from the filesystem — available in the current session immediately after writing
- No sandbox testing or remote sharing is available
