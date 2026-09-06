---
name: controlmcp
description: How to operate the user's macOS desktop via ControlMCP (MCP server `control`). Use when controlling the UI outside the terminal: opening apps/URLs, taking screenshots, clicking, typing, scrolling, window management, reading screens, browser/site interaction, long-screen captures, or any "look at the desktop" request. Triggers: 'screenshot', 'control the screen', 'click on', 'open safari/browser', 'take over the desktop', 'look at the screen', 'desktop automation', 'use the computer', 'macOS control'.
---

# Controlling the Desktop with ControlMCP

ControlMCP is a local MCP server (`control`) configured in `~/.config/opencode/opencode.jsonc`. Its tools are pre-authorized (`permission.control_*: "allow"`), so NO confirmation is needed. All coordinates are absolute screen pixels on the primary monitor (1920x1200).

## Capabilities (tool reference)

### Screenshots & vision
- `capture_screen` — full-screen PNG (params: save_dir, monitor, quality, max_width, grid_rows/cols, sharpen). **Always capture to a file** (save_dir) so you can read it back.
- `capture_region` — crop x/y/width/height to a region (smaller = faster + more OCR-able).
- `capture_scroll_region` — scroll-capture a container (x/y/width/height, scroll_distance) for long content.
- `capture_window` — capture a specific window by title (params title, save_dir, quality).
- `get_screen_info` — display geometry (monitor bounds, scale).
- `read_screenshot_base64` — returns the last screenshot as base64/data-url.
- `get_pixel_color` — sample a pixel's color at x/y.

### Windows
- `list_windows` — all open windows (no params).
- `find_windows` — filter by `title_contains` (returns matches; **empty result ≠ app closed — check exact title**).
- `focus_window` — bring window with `title` to front (required before clicking).
- `recover_window_visibility` — if a window exists but the screen looks wrong, force-restore it.
- `show_desktop_then_capture` — clear the clutter, then screenshot.

### Mouse
- `mouse_position` — current cursor location.
- `mouse_move` — move to x/y.
- `mouse_click` — click at x/y (params: button, click count, modifiers).
- `mouse_drag` — drag from (x1,y1) to (x2,y2).
- `mouse_scroll` — scroll at position (x/y, scroll_amount, direction).
- `click_grid_target` / `resolve_grid_target` — for grid-based clicking (capture with grid_rows/cols then click cells).

### Keyboard
- `key_press` — single key (e.g. `key_press: return`, `cmd+space`).
- `key_hold` — hold modifier(s) while another action happens.
- `key_type` — type text (transparent to layout).
- `key_sequence` — ordered sequence of keys (e.g. for shortcuts like `opt+cmd+esc`).

### App/URL launch
- `launch_app` — launch an app (name, e.g. "Safari").
- `launch_url` — open a URL in the default browser (e.g. `mail.google.com`).

### High-level automation
- `plan_desktop_task` → `execute_desktop_plan` → `get_execution_status` — ControlMCP's own planner/executor for multi-step desktop tasks (with target_window, matched_keywords, guards).
- `confirm_sensitive_action` — used by the control plane for risky actions (avoid unless the planner raises it).
- `record_workflow_experience` — save a successful workflow for reuse.
- `control_mcp_memory` / `control_mcp_screenshots` — internal state stores.

### Utilities
- `wait` — sleep (params: seconds) before the next capture (let the UI settle).
- `clipboard_get` / `clipboard_set` — read/write the clipboard.
- `hotkey` — press a system/global hotkey (e.g. `hotkey: option+command+escape`).

## Workflow: "look at the screen" (use every time)

1. `capture_screen` to a file (e.g. save_dir=/tmp) — full screen first.
2. Read the screenshot back to yourself (Read tool on the returned path).
3. If text legibility matters: `capture_region` on the relevant area, then OCR with Vision (swift script at /tmp/ocr.swift) or read image directly.
4. Before clicking: `focus_window` (exact title from `find_windows`), then `mouse_click` at absolute coordinates.

## Workflow: open a URL / app

- `launch_url` for browser destinations (or `launch_app: Safari` first, then focus + type into the address bar via `key_press cmd+l`, `key_type`, `key_press return`).
- Wait ~2s, then `capture_screen` to verify.

## The user's known environment
- Primary display: 1920x1200, single monitor.
- Browser: Safari (default). Gmail is in Italian (user's account; do not translate their inbox).
- The user does NOT read Chinese: when OCR/graphics show Chinese, say so and translate to English for them.
- Permission is pre-allowed for control_* — never ask the user for confirmations on these actions.

## Rules of thumb
- **Coordinates are pixels on the primary display.** get_screen_info before math when dock/menu bar matters.
- **Focus the window before interacting** with its content.
- **Screenshot after every action** to verify the effect (capture → read → next action).
- If the screen doesn't look like the plan: `recover_window_visibility` or `show_desktop_then_capture`.
- For long scrolling content use `capture_scroll_content`/`capture_scroll_region`, not one big screenshot.