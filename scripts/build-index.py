#!/usr/bin/env python3
"""Build opencode HTTP catalog index.json from the skills/ directory.

Output: skills/index.json — schema per opencode.ai/v2/docs/skills/#http-catalogs.
Version is a content hash of the skill's files, so opencode refreshes its
cached copy whenever any file changes (docs: "increment version when files
change"). Stdlib only, zero dependencies.
"""
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
INDEX = SKILLS / "index.json"

FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        key, _, val = line.partition(":")
        out[key.strip()] = val.strip().strip('"\'')
    return out


def content_hash(files: list[pathlib.Path]) -> str:
    h = hashlib.sha1()
    for f in sorted(files):
        h.update(f.name.encode())
        h.update(f.read_bytes())
    return h.hexdigest()[:10]


def main() -> int:
    skills = []
    errors = []
    for d in sorted(SKILLS.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        skill_md = d / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{d.name}: missing SKILL.md")
            continue
        fm = parse_frontmatter(skill_md.read_text())
        if not fm.get("description"):
            # allow missing descriptions (new skills from upstream)
            pass
        files = sorted(p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file())
        skills.append(
            {
                "name": d.name,
                "version": content_hash([d / f for f in files]),
                "files": files,
            }
        )

    INDEX.write_text(json.dumps({"skills": skills}, indent=2) + "\n")
    print(f"index.json: {len(skills)} skills -> {INDEX}")
    if errors:
        for e in errors:
            print(f"  WARN: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())