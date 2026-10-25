---
name: About Me
description: Creates / edits the user's identity profile interactively. First install asks questions; later edits via @about-me /edit-info command. Keeps personalization out of hardcoded files.
---

## How it works

When first loaded and no profile exists (or the profile is empty / undefined):
ask 5–8 concise questions, record answers to `~/.config/opencode/skills/about-me/profile.md`

Questions (ask one at a time, allow "skip"):
1. Your preferred name / handle?
2. Language (do NOT show raw Chinese)
3. Timezone / locale?
4. Work style: terse/confirm-heavy/fast-iteration/decompose?
5. Confirmations: always / destructive-only / batch-one-per-fork?
6. Projects / repos you maintain (optional, just names)?
7. Any rules that override default behavior (optional)?

If answers already exist, read `profile.md` instead of asking.

## Editing

Trigger by @-mentioning the skill and typing the edit command:

```
@about-me edit-info
```

Then ask which field to change (name / language / timezone / work-style / confirmations / projects / rules), or open `~/.config/opencode/skills/about-me/profile.md` directly.

The skill never hardcodes identity into its SKILL.md — it's always read from profile.md, edited by the user, and rebuilt when needed.

## What is NOT stored here
- Real usernames, emails, paths, or machine details (those go in profile.md only if the user chooses to enter them)
- Anything the user did not explicitly answer
- Project internals — only names/URLs if the user wants them known
