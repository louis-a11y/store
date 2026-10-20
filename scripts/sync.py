#!/usr/bin/env python3
"""Two-way sync between the live skills folder and the store repo.

Live folder: ~/.config/opencode/skills   (the skills agents actually load)
Store:       ~/tools/skillstore          (published to github.com/louis-a11y/store)

Every run:
1. pull the store from GitHub — edits made on your other device arrive here
2. compare each skill in both directions, using .sync-state.json to know
   what was in sync last time:
   - changed locally         -> copy into the store and push
   - changed on GitHub       -> copy into the live folder
   - changed on BOTH sides   -> CONFLICT: keep local, warn, push nothing
   - deleted locally         -> stays deleted (never resurrected)
   - new on GitHub           -> downloaded into the live folder
3. rebuild skills/index.json, commit + push only if the store changed
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


def skill_dirs(root: Path) -> dict[str, Path]:
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
    # 1. catch up with GitHub first (skill edits from other devices land here)
    if run("git", "status", "--porcelain"):
        print("! store repo has manual edits — skipping pull this run")
    else:
        try:
            run("git", "pull", "--ff-only", "origin", BRANCH)
        except subprocess.CalledProcessError as e:
            print(f"! git pull failed, aborting run: {e}")
            return 1

    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    live = skill_dirs(SRC)
    store = skill_dirs(DEST)
    actions: list[str] = []

    for name in sorted(set(live) | set(store)):
        last = state.get(name)
        lh = hash_tree(live[name]) if name in live else None
        sh = hash_tree(store[name]) if name in store else None

        if lh is not None and lh == sh:                     # both sides identical
            state[name] = lh
        elif lh is not None and sh is None:                 # only here: new local skill
            copy_to(live[name], DEST / name)
            actions.append(f"+{name} (new local)")
            state[name] = lh
        elif sh is not None and lh is None:                 # only in store
            if last == "deleted":
                pass                                        # you deleted it on purpose; leave it gone
            elif last is None:
                copy_to(store[name], SRC / name)            # genuinely new from another device
                actions.append(f"-{name} (downloaded)")
                state[name] = sh
            elif last != sh:
                print(f"! {name}: deleted locally but changed on GitHub — left deleted; check it wasn't an accident")
            else:
                state[name] = "deleted"                     # was in sync, then you deleted it here
        else:                                               # both exist, differ
            local_changed = lh != last
            remote_changed = sh != last
            if local_changed and remote_changed:
                print(f"! CONFLICT {name}: changed both locally and on GitHub — kept local, NOT pushed. "
                      f"Reconcile the two versions, then run again")
                state[name] = lh
            elif local_changed:
                copy_to(live[name], DEST / name)
                actions.append(f"+{name} (edited here)")
                state[name] = lh
            else:                                           # only remote changed
                if live[name].is_symlink():
                    print(f"! {name}: changed on GitHub but local is a symlink -> {live[name].resolve()}. "
                          f"Edit it at its target instead")
                    state[name] = lh
                else:
                    copy_to(store[name], SRC / name)
                    actions.append(f"-{name} (updated from store)")
                    state[name] = sh

    # 3. rebuild catalog, publish only if something changed
    run(sys.executable, str(REPO / "scripts/build-index.py"))
    STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")

    if not run("git", "status", "--porcelain"):
        print("store already in sync")
        return 0
    run("git", "add", "-A")
    summary = ", ".join(actions) if actions else "state refresh"
    run("git", "commit", "-m", f"sync: {summary}")
    run("git", "push", "origin", BRANCH)
    print(f"published: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
