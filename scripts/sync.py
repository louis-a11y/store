#!/usr/bin/env python3
"""Two-way mirror sync between the live skills folder and the store repo.

Live folder: ~/.config/opencode/skills   (the skills agents actually load)
Store:       ~/tools/skillstore          (published to github.com/louis-a11y/store)

Rules (local copy always wins a conflict):
- edited here            -> copied into the store, pushed
- edited on GitHub       -> downloaded here
- deleted here           -> deleted from the store (and from other devices later)
- deleted on GitHub      -> deleted here
- edited on both sides   -> kept local, warning logged, nothing pushed
- never synced before    -> treated as new, propagated (a fresh machine can never
                            trigger deletions)

.sync-state.json holds the last hash both sides agreed on, plus "deleted"
tombstones that stop deletions from being resurrected on devices that have not
synced yet. Runs hourly + at login via launchd (com.louis-a11y.skillstore-sync).
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
    actions = []

    for name in sorted(set(live) | set(store)):
        last = state.get(name)
        lh = hash_tree(live[name]) if name in live else None
        sh = hash_tree(store[name]) if name in store else None

        if lh is not None and lh == sh:                      # both sides identical
            state[name] = lh
        elif lh is not None and sh is None:                  # only on this machine
            if last == "deleted":                            # re-added after a deletion
                copy_to(live[name], DEST / name)
                actions.append(f"+{name} (re-added)")
                state[name] = lh
            elif last is None:                               # brand-new local skill
                copy_to(live[name], DEST / name)
                actions.append(f"+{name} (new)")
                state[name] = lh
            elif live[name].is_symlink():                    # deleted on GitHub; local is a symlink
                print(f"! {name}: deleted from store but local is a symlink -> {live[name].resolve()}; "
                      f"remove manually if that was intended")
                state[name] = "deleted"
            else:                                            # deleted on another device
                shutil.rmtree(live[name])
                actions.append(f"-{name} (deleted on store side)")
                state[name] = "deleted"
        elif sh is not None and lh is None:                  # only in the store
            if last == "deleted":                            # re-added on another device
                copy_to(store[name], SRC / name)
                actions.append(f"-{name} (re-added, downloaded)")
                state[name] = sh
            elif last is None:                               # new from another device
                copy_to(store[name], SRC / name)
                actions.append(f"-{name} (downloaded)")
                state[name] = sh
            else:                                            # deleted on this machine
                shutil.rmtree(store[name])
                actions.append(f"-{name} (deleted here)")
                state[name] = "deleted"
        else:                                                # both exist, differ
            if lh != last and sh != last:                    # changed on both sides
                print(f"! CONFLICT {name}: changed both locally and on GitHub — kept local, NOT pushed. "
                      f"Reconcile the two versions, then run again")
                state[name] = lh
            elif lh != last:                                 # edited here
                copy_to(live[name], DEST / name)
                actions.append(f"+{name} (edited here)")
                state[name] = lh
            elif live[name].is_symlink():                    # changed on GitHub; symlinked locally
                print(f"! {name}: changed on GitHub but local is a symlink -> {live[name].resolve()}; "
                      f"edit it at its target instead")
                state[name] = lh
            else:                                            # changed on GitHub
                copy_to(store[name], SRC / name)
                actions.append(f"-{name} (updated from store)")
                state[name] = sh

    # 2. rebuild catalog, publish only if something changed
    run(sys.executable, str(REPO / "scripts/build-index.py"))
    STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")

    if not run("git", "status", "--porcelain"):
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
