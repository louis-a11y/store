#!/usr/bin/env bash
# Set up two-way skill sync on this machine. Safe to re-run.
#
# Usage on a fresh Mac:
#   brew install gh && gh auth login
#   git clone https://github.com/louis-a11y/store.git ~/tools/skillstore
#   bash ~/tools/skillstore/scripts/setup-machine.sh
set -euo pipefail

REPO_URL="https://github.com/louis-a11y/store.git"
DEST="$HOME/tools/skillstore"
LABEL="com.louis-a11y.skillstore-sync"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

command -v gh >/dev/null || { echo "! gh missing — brew install gh && gh auth login"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "! not logged in — run: gh auth login"; exit 1; }

# clone if this isn't the repo yet (makes the script self-sufficient)
if [ ! -d "$DEST/.git" ]; then
  mkdir -p "$HOME/tools"
  git clone "$REPO_URL" "$DEST"
fi

mkdir -p "$HOME/Library/LaunchAgents"
cp "$DEST/scripts/$LABEL.plist" "$PLIST"

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl kickstart "gui/$(id -u)/$LABEL"
sleep 3

echo "sync installed:"
echo "  log: /tmp/skillstore-sync.log"
tail -1 /tmp/skillstore-sync.log 2>/dev/null || echo "  (log appears after first run)"