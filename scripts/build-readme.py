#!/usr/bin/env python3
"""Regenerate README header counts from skills/ + plugins/ so they never rot."""
from pathlib import Path
repo = Path(__file__).resolve().parent.parent
skills = sum(1 for d in (repo/"skills").iterdir() if d.is_dir() and not d.name.startswith(".") and (d/"SKILL.md").is_file())
plugins = sum(1 for p in (repo/"plugins").iterdir() if p.is_file() and not p.name.startswith(".") and p.name.endswith(".json"))
readme = repo / "README.md"
t = readme.read_text()
t = t.split("\n", 1)[1] if "\n" in t else t
header = f"# Skill Store  ({skills} skills / {plugins} plugin catalogs)\n\nA curated pack of skills + plugin catalogs [opencode]"
# inject header and replace the old hardcoded 36 mention in paragraph 1
lines = t.splitlines()
# replace first paragraph's number if still hardcoded
new_first = f"A curated pack of {skills} skills + {plugins} plugin catalogs [opencode]"
for i, ln in enumerate(lines):
    if ln.startswith("A curated pack of"):
        lines[i] = new_first
        break
t = "\n".join(lines)
readme.write_text("# Skill Store  (" + f"{skills} skills / {plugins} plugin catalogs)\n" + ("\n".join(lines[1:] if lines[0].startswith("# ") else lines)) + "\n")
print(f"README updated: {skills} skills / {plugins} plugin catalogs")
