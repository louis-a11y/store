#!/usr/bin/env python3
"""Sync live skills (~/.config/opencode/skills) into the store repo and publish.

- Copies new/changed skills (symlinks dereferenced, .DS_Store skipped)
- Never deletes store skills that vanished locally — public packs are archives;
  orphans are only logged
- Rebuilds skills/index.json
- Commits + pushes only when something actually changed

Run manually or via launchd (com.louis-a11y.skillstore-sync).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path.home() / ".config/opencode/skills"
REPO = Path(__file__).resolve().parent.parent
DEST = REPO / "skills"
INDEX = DEST / "index.json"
BRANCH = "main"


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=REPO, text=True).strip()


def tree_hash(d: Path) -> str:
    h = hashlib.sha1()
    for p in sorted(d.rglob("*")):
        if p.is_file() and p.name != ".DS_Store":
            h.update(str(p.relative_to(d)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def copy_skill(src: Path, dest: Path) -> None:
    if dest.is_symlink() or (dest.exists() and not dest.is_dir()):
        dest.unlink()
    elif dest.is_dir():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, symlinks=False, ignore=shutil.ignore_patterns(".DS_Store"))


def main() -> int:
    changed: list[str] = []
    for src in sorted(SRC.iterdir()):
        if not src.is_dir() or src.name.startswith(".") or not (src / "SKILL.md").is_file():
            continue
        dest = DEST / src.name
        if not dest.is_dir() or tree_hash(src) != tree_hash(dest):
            copy_skill(src, dest)
            changed.append(src.name)

    # rebuild catalog (also refreshes hashes of unchanged files' neighbors)
    run(sys.executable, str(REPO / "scripts/build-index.py"))

    orphans = sorted(
        d.name for d in DEST.iterdir()
        if d.is_dir() and not d.name.startswith(".") and not (SRC / d.name).exists()
    )
    if orphans:
        print(f"orphans kept in store (not on this machine): {', '.join(orphans)}")

    if not run("git", "status", "--porcelain"):
        print("store already in sync" + ("" if not changed else f" (local copies refreshed: {', '.join(changed)})"))
        return 0

    run("git", "add", "-A")
    summary = f"skills updated: {', '.join(changed)}" if changed else "catalog refresh"
    run("git", "commit", "-m", f"sync: {summary}")
    run("git", "push", f"origin", BRANCH)
    print(f"published: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())