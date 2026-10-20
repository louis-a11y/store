#!/usr/bin/env bash
# Install skills from github.com/louis-a11y/store — one command, curl + tar only.
#
# Usage:
#   install.sh                      install every skill
#   install.sh skill-a skill-b      install selected skills
#   install.sh --list               list available skills (names only)
#   install.sh --to DIR [...]       install into DIR (default: ~/.config/opencode/skills)
#
# Works for any agent's skills dir: ~/.config/opencode/skills, ~/.claude/skills,
# ~/.agents/skills, a project's .opencode/skills — same skill format everywhere.
set -euo pipefail

REPO="louis-a11y/store"
BRANCH="main"
BASE_URL="https://raw.githubusercontent.com/$REPO/$BRANCH/skills"
DEST="$HOME/.config/opencode/skills"

NAMES=()
while [ $# -gt 0 ]; do
  case "$1" in
    --to)   DEST="$2"; shift 2 ;;
    --list) LIST_ONLY=1; shift ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    -*)     echo "unknown flag: $1" >&2; exit 2 ;;
    *)      NAMES+=("$1"); shift ;;
  esac
done

fetch_index() {
  if command -v curl >/dev/null; then
    curl -fsSL "$BASE_URL/index.json"
  else
    wget -qO- "$BASE_URL/index.json"
  fi
}

available() {
  fetch_index | python3 -c 'import json,sys; [print(s["name"]) for s in json.load(sys.stdin)["skills"]]'
}

if [ "${LIST_ONLY:-}" = "1" ]; then
  available
  exit 0
fi

if [ ${#NAMES[@]} -eq 0 ]; then
  while IFS= read -r n; do NAMES+=("$n"); done < <(available)
fi

echo "installing ${#NAMES[@]} skills -> $DEST" >&2

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# one archive download covers every skill, including multi-file ones
curl -fsSL "https://codeload.github.com/$REPO/tar.gz/refs/heads/$BRANCH" -o "$TMP/pack.tgz"

mkdir -p "$DEST"
INSTALLED=0
for name in "${NAMES[@]}"; do
  if ! tar -tzf "$TMP/pack.tgz" | grep -q "^$REPO-$BRANCH/skills/$name/"; then
    echo "  ! $name: not in store, skipping" >&2
    continue
  fi
  rm -rf "$DEST/$name"
  tar -xzf "$TMP/pack.tgz" -C "$DEST" --strip-components=2 "$REPO-$BRANCH/skills/$name"
  INSTALLED=$((INSTALLED + 1))
done

echo "installed $INSTALLED skill(s). restart your agent session to pick them up." >&2