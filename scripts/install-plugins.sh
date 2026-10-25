#!/usr/bin/env bash
# Install this store's plugins (MCP server configs, commands, agents).
#
# Usage:
#   bash scripts/install-plugins.sh          # all plugins
#   bash scripts/install-plugins.sh NAME     # specific plugin
#   bash scripts/install-plugins.sh --list    # available
set -euo pipefail
REPO="https://github.com/louis-a11y/store"
BRANCH="main"
DEST="${HOME}/.config/opencode"

NAME="${1:-}"
[ "$NAME" = "--list" ] && { curl -fsSL "$REPO/raw/$BRANCH/plugins/index.json" | python3 -c 'import json,sys; [print(p["name"]) for p in json.load(sys.stdin)["plugins"]]'; exit 0; }

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
curl -fsSL "$REPO/archive/$BRANCH.tar.gz" -o "$TMP/pack.tgz"
PREFIX=$(tar -tzf "$TMP/pack.tgz" | head -1 | cut -d/ -f1)

mkdir -p "$DEST/plugins" "$DEST/commands" "$DEST/agents"

if [ -n "$NAME" ]; then
  tar -xzf "$TMP/pack.tgz" -C "$TMP" --strip-components=2 "$PREFIX/plugins/$NAME"
  cp -R "$TMP/$NAME" "$DEST/plugins/"
  echo "plugin installed: $NAME -> $DEST/plugins/$NAME"
else
  tar -xzf "$TMP/pack.tgz" -C "$TMP" --strip-components=2 "$PREFIX/plugins"
  cp -R "$TMP/plugins"* "$DEST/plugins/" 2>/dev/null || true
  echo "all plugins -> $DEST/plugins/"
fi