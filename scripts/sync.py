#!/usr/bin/env python3
"""Two-way recovery sync between the live skills folder and the store repo.

Live folder: ~/.config/opencode/skills   (the skills agents actually load)
Store:       ~/tools/skillstore          (published to github.com/louis-a11y/store)

Accidental deletions bounce back:
- deleted from the live folder    -> restored from the store
- deleted from the store          -> restored from the live folder
- deleted on another device       -> restored here (and re-pushed by that device)

The ONLY permanent deletion is the trash:
    bash scripts/trash.sh SKILL-NAME        (deletes it everywhere)
    git mv trash/NAME skills/NAME           (restores it everywhere)

Rules:
- edited here          -> copied into the store, pushed
- edited on GitHub     -> downloaded here
- edited on both sides -> kept local, warning logged, nothing pushed
- skill sitting in trash/ -> removed from the live folder too

.sync-state.json holds the hash both sides last agreed on (needed to tell
"edited here" apart from "edited there"). Runs hourly + at login via launchd
(com.louis-a11y.skillstore-sync).
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path.home() / ".config/opencode/skills"
REPO = Path(__file__).resolve().parent.parent
DEST = REPO / "skills"
TRASH = REPO / "trash"
STATE = REPO / ".sync-state.json"
BRANCH = "main"


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=REPO, text=True).strip()


def hash_tree(d: Path) -> str:
    h = hashlib.sha1()
    for p in sorted(d.rglob("*")):
        if p.is_file() and p.name != ".DS_Store":
            h.update(str(p.relative_to(d)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def skill_dirs(root: Path) -> dict:
    return {
        d.name: d
        for d in root.iterdir()
        if d.is_dir() and not d.name.startswith(".") and (d / "SKILL.md").is_file()
    }


def copy_to(src: Path, dest: Path) -> None:
    if dest.is_symlink() or (dest.exists() and not dest.is_dir()):
        dest.unlink()
    elif dest.is_dir():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, symlinks=False, ignore=shutil.ignore_patterns(".DS_Store"))


def main() -> int:
    # 1. catch up with GitHub first (other devices' changes arrive here)
    if run("git", "status", "--porcelain"):
        run("git", "add", "-A")
        run("git", "commit", "-m", "sync: manual changes")
    try:
        run("git", "pull", "--rebase", "origin", BRANCH)
    except subprocess.CalledProcessError:
        run("git", "rebase", "--abort")
        print("! remote and local histories conflicted — aborting this run, nothing touched")
        return 1

    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    live = skill_dirs(SRC)
    store = skill_dirs(DEST)
    trashed = skill_dirs(TRASH) if TRASH.is_dir() else {}
    actions = []

    # NOTE: trashed skills are only removed from the store (trash.sh does the move).
    # Live folders are never touched by a deletion — a local rm is what removes it,
    # and it sticks because the store copy is already gone.

    for name in sorted(set(live) | set(store)):
        if name in trashed:
            continue
        last = state.get(name)
        lh = hash_tree(live[name]) if name in live else None
        sh = hash_tree(store[name]) if name in store else None

        if lh is not None and lh == sh:                 # both sides identical
            state[name] = lh
        elif lh is not None and sh is None:             # store copy gone: restore (or brand-new local)
            copy_to(live[name], DEST / name)
            actions.append(f"+{name} ({'new' if last is None else 'restored to store'})")
            state[name] = lh
        elif sh is not None and lh is None:             # live copy gone: restore from store
            copy_to(store[name], SRC / name)
            actions.append(f"* {name} (restored to live)")
            state[name] = sh
        else:                                           # both exist, differ
            if lh != last and sh != last:               # changed on both sides
                print(f"! CONFLICT {name}: changed both locally and on GitHub — kept local, NOT pushed. "
                      f"Reconcile the two versions, then run again")
                state[name] = lh
            elif lh != last:                            # edited here
                copy_to(live[name], DEST / name)
                actions.append(f"+{name} (edited here)")
                state[name] = lh
            elif live[name].is_symlink():               # changed on GitHub; symlinked locally
                print(f"! {name}: changed on GitHub but local is a symlink -> {live[name].resolve()}; "
                      f"edit it at its target instead")
                state[name] = lh
            else:                                       # changed on GitHub
                copy_to(store[name], SRC / name)
                actions.append(f"* {name} (updated from store)")
                state[name] = sh

    # 2. drop state for skills gone from everywhere, rebuild catalog
    for stale in [n for n in state if n not in live and n not in store and n not in trashed]:
        del state[stale]
    run(sys.executable, str(REPO / "scripts/build-index.py"))
    try:
        run(sys.executable, str(REPO / "scripts/build-readme.py"))
    except Exception as e:
        print(f"! README refresh skipped: {e}")
    STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")

    # 3. publish only if something changed
    if not run("git", "status", "--porcelain"):
        ahead = run("git", "rev-list", f"origin/{BRANCH}..HEAD", "--count")
        if ahead != "0":
            try:  # pending commits exist (e.g. manual edits committed at start)
                run("git", "push", "origin", BRANCH)
                print("published: pending commits")
            except subprocess.CalledProcessError:
                print("! push failed (did another device push in the meantime?) — will retry next run")
            return 0
        print("store already in sync")
        return 0
    run("git", "add", "-A")
    summary = ", ".join(actions) if actions else "state refresh"
    run("git", "commit", "-m", f"sync: {summary}")
    try:
        run("git", "push", "origin", BRANCH)
    except subprocess.CalledProcessError:
        print("! push failed (did another device push in the meantime?) — will retry next run")
        return 1
    print(f"published: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
