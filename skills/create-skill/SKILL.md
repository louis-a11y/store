---
name: create-skill
description: Use when the user requests a capability that no existing skill provides. Creates a new opencode skill by researching, designing, validating, and saving it.
---

# Create Skill

## Purpose

Create a new skill when no existing skill can perform the requested task.

## Workflow

### 1. Identify Skill Requirement

Define what the user needs opencode to be able to do.

### 2. Search Existing Skills

Check if a suitable skill already exists by:
- Reviewing the available skills list
- Checking `.opencode/skills/` and `~/.config/opencode/skills/` directories
- If a suitable skill exists, use it and stop.

### 3. Research

When no existing skill is suitable, search the web to understand how to accomplish the skill's requirement.

### 4. Design Skill

Create the skill with these components:
- **name**: lowercase hyphen-separated (max 64 chars)
- **description**: What the skill does AND when to trigger it. Front-load trigger keywords.
- **instructions**: Step-by-step guide for the AI to follow

### 5. Validate Syntax

Ensure the skill follows the correct format:
- Valid YAML frontmatter with `name` and `description`
- Markdown body with clear instructions
- No unknown frontmatter fields

If invalid, fix the issues and re-validate.

### 6. Save Skill

Write the skill file to:
```
.opencode/skills/<skill-name>/SKILL.md
```

The skill is available immediately after writing.

## Notes

- Skills are auto-discovered from the filesystem
- No sandbox testing or remote sharing is available
- The skill can be used in the current session after creation