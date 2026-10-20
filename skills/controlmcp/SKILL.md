---
name: controlmcp
description: How to operate the user's macOS desktop via ControlMCP (MCP server `control`). Use when controlling the UI outside the terminal: opening apps/URLs, taking screenshots, clicking, typing, scrolling, window management, reading screens, browser/site interaction, long-screen captures, or any "look at the desktop" request. Triggers: 'screenshot', 'control the screen', 'click on', 'open safari/browser', 'take over the desktop', 'look at the screen', 'desktop automation', 'use the computer', 'macOS control'.
---

# Controlling the Desktop with ControlMCP

Local MCP server (`control`) in `~/.config/opencode/opencode.jsonc`; tools pre-authorized (`permission.control_*: "allow"`). All coordinates = absolute pixels on the primary monitor (1920×1200). **Methodology is in `computer-control`.**

## Tool reference

**Screenshots:** `capture_screen` (full/monitor; `max_width=960`, `quality=70–80` for fast LLM analysis) · `capture_region(x,y,w,h)` · `capture_scroll_region(x,y,w,h,scroll_distance,quality?)` — long content; never `capture_scroll_content` (doesn't exist) · `capture_window(title)` · `read_screenshot_base64(file_path)` · `get_screen_info()` · `get_pixel_color(x,y)`.

**Windows:** `find_windows(title_contains)` (empty ≠ closed — check exact title) · `focus_window(title)` (before any interact) · `list_windows` · `recover_execution_context(strategy="window_rescue", target_window=…)` (replaces nonexistent `recover_window_visibility`; `show_desktop_then_capture` also doesn't exist).

**Mouse:** `mouse_move` · `mouse_click(x,y,button,clicks,modifiers)` · `mouse_drag(x1,y1→x2,y2)` · `mouse_scroll(clicks,x,y)` · `click_grid_target(cell,anchor,…)` / `resolve_grid_target(...)` (after `capture_region` with `grid_rows`/`grid_cols`).

**Keyboard:** `key_press` / `key_hold` / `key_type` (layout-transparent) / `key_sequence` / `hotkey` / `clipboard_get` / `clipboard_set`.

**Launch:** `launch_app(name,args)` · `launch_url(url)`.

**Plan / verify:** `plan_desktop_task` → `execute_desktop_plan` → `get_execution_status`; `record_workflow_experience`; `wait(seconds)`; `confirm_sensitive_action` (only if planner raises it).

## Workflows

- "Look at this" / screenshot read → capture to file (`save_dir`) → `~/bin/vimg` (OCR + colors; if `e5rt` / Core-ML error hits `ocr-bin`/`vimg`, rebuild: `swiftc -O ~/bin/ocr.swift -o ~/bin/ocr-bin`; never "read image directly" — this model can't see pixels).
- Region-first: `capture_region` → `vimg -l` for layout coords.
- Open URL/app: `launch_url` (or `launch_app` → `focus_window` → `key_press cmd+l` → `key_type` → `return`) → `wait(2)` → `capture_screen` → `vimg`.
- Browser verification / Cloudflare turnstile: `capture_window`/`region` (+ grid) → `click_grid_target`/`resolve_grid_target` → click on screen → `wait(1–2)` → `chrome-devtools_take_snapshot`/`wait_for`; do NOT blind-click via DOM only.

## Rules

- macOS only; display 1920×1200; browser Safari; Gmail Italian — don't translate; `control_*` pre-allowed → never ask confirmation; if image shows Chinese → say so and translate to English; `focus_window` ≠ operable → always `focus_window` → `wait` → `capture` → verify.
