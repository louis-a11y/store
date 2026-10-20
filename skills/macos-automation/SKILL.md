---
name: macos-automation
description: Use when automating the Mac from the shell — osascript/AppleScript, screencapture, pbcopy/pbpaste, launchctl, defaults, open, window management, notifications. Covers macOS-native CLI automation without third-party tools.
---

## Core commands

| Command | Purpose |
|---|---|
| `screencapture -x /tmp/s.png` | Screenshot full screen silently (no shutter sound) |
| `screencapture -x -R x,y,w,h /tmp/s.png` | Screenshot a region (0,0 is top-left, primary display coords) |
| `screencapture -x -w /tmp/s.png` | Interactive window capture |
| `screencapture -x -t jpg /tmp/s.jpg` | Force JPEG (smaller) |
| `pbcopy` / `pbpaste` | Pipe text to/from clipboard: `echo hi | pbcopy`, `pbpaste` |
| `pbpaste | jq .` | Inspect clipboard JSON |
| `open -a Safari https://x.com` | Open URL in a specific app |
| `open .` | Reveal cwd in Finder |
| `defaults read com.apple.finder` | Read an app's preferences |
| `defaults write com.apple.finder AppleShowAllFiles -bool true` | Write a preference (then `killall Finder`) |
| `launchctl list` | List loaded launchd jobs |
| `launchctl load/unload ~/Library/LaunchAgents/foo.plist` | Manage user launch agents (legacy but common) |

## osascript (AppleScript from shell)

```bash
# Tell an app to do something
osascript -e 'tell application "Safari" to activate'

# Get info / open URL
osascript -e 'tell application "Safari" to open location "https://example.com"'

# Window list (useful for targeting)
osascript -e 'tell application "System Events" to get name of every window of every process'

# Keystrokes (requires Accessibility permission for the terminal)
osascript -e 'tell application "System Events" to keystroke "c" using command down'

# Run a full script from a file
osascript /path/to/script.applescript
```

## Screenshot + OCR pipeline (this machine has NO image input)

1. `screencapture -x /tmp/s.png`
2. Run Swift Vision OCR: `swift /tmp/ocr.swift /tmp/s.png` (script exists, compiled ad-hoc)
3. Grep/read the text output.

## launchctl / launch agents

- User agents: `~/Library/LaunchAgents/*.plist` (run when user logs in)
- `launchctl list | grep <label>` — check if a job is loaded/running
- `launchctl kickstart gui/$(id -u)/<label>` — restart a running agent
- Plist keys: `ProgramArguments`, `RunAtLoad`, `StartInterval` (seconds), `StandardOutPath`/`StandardErrorPath`

## Pitfalls

- **TCC permissions**: screencapture (Screen Recording), osascript keystrokes/System Events (Accessibility), clipboard read (some contexts) all require granting the host terminal app permission in System Settings > Privacy & Security. First call silently fails or returns garbage — check permissions first.
- `defaults` changes often need the app restarted (`killall <app>`) to take effect.
- Apple Silicon: some old keystroke-based automation is flaky in apps that use custom hotkey handlers; prefer native `open` URLs or IPC when available.
- `osascript -e` with System Events is SLOW (~0.5-1s per call). Batch into one script instead of looping.
- Screenshot coords on this machine are primary-display pixels (1920x1200). Retina scaling: `screencapture` returns pixels, not points.