#!/usr/bin/env bash
# Permanently delete a skill (it is the only way — accidental deletions bounce back).
#
#   bash scripts/trash.sh SKILL-NAME
#
# Restore later (from anywhere, on any machine):
#   git mv trash/SKILL-NAME skills/SKILL-NAME && python3 scripts/sync.py
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
NAME="${1:?usage: trash.sh SKILL-NAME}"
[ -d "$REPO/skills/$NAME" ] || { echo "! not in the store: $NAME"; exit 1; }

mkdir -p "$REPO/trash"
if git -C "$REPO" mv "skills/$NAME" "trash/$NAME" 2>/dev/null; then
  :
else
  mv "$REPO/skills/$NAME" "$REPO/trash/$NAME"
fi

python3 "$REPO/scripts/sync.py"
echo "trashed: $NAME (restore: git mv trash/$NAME skills/$NAME)"