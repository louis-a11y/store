---
name: controlmcp
description: How to operate the user's macOS desktop via ControlMCP (MCP server `control`) — screenshots, mouse clicks, keyboard input, clipboard, window management, and long-scroll captures. Use when controlling the UI outside the terminal: opening apps/URLs, taking screenshots, clicking, typing, scrolling, reading screens, browser/site interaction, long-screen captures, IDE/browser/office-app operation, waiting for an interface to settle, judging whether log or page content has stopped changing, or any "look at the desktop" request. Triggers: 'screenshot', 'control the screen', 'click on', 'open safari/browser', 'take over the desktop', 'look at the screen', 'desktop automation', 'use the computer', 'macOS control'.
---

# Controlling the Desktop with ControlMCP

Local MCP server (`control`) in `~/.config/opencode/opencode.jsonc`. Tools pre-authorized (`permission.control_*: "allow"`) — no confirmation needed. Coordinates = absolute pixels on the primary monitor (1920×1200).

This file is both the **tool reference** and the **methodology**. Part 1 lists tools; Part 2 is how to use them reliably.

---

## Part 1 — Tool reference

**Screenshots** (always pass `save_dir`, e.g. `/tmp`): `capture_screen` (full/monitor, `max_width=960`, `quality=70–80` for fast analysis) · `capture_region` (x/y/width/height) · `capture_scroll_region` (x/y/width/height, `scroll_distance` — long content; there is NO `capture_scroll_content`) · `capture_window` (by `title`) · `read_screenshot_base64` (last screenshot → text) · `get_pixel_color` · `get_screen_info` (geometry/scale).

**Windows:** `list_windows` · `find_windows(title_contains)` (empty ≠ app closed — recheck exact title) · `focus_window(title)` (front before interacting) · `recover_execution_context(strategy="window_rescue", target_window=…)` (window exists but screen looks wrong — this replaces the nonexistent `recover_window_visibility`/`show_desktop_then_capture`).

**Mouse:** `mouse_position` · `mouse_move` · `mouse_click(x, y, button, click count, modifiers)` · `mouse_drag(x1,y1 → x2,y2)` · `mouse_scroll(clicks, x, y)` · `click_grid_target(cell, anchor, …)` / `resolve_grid_target(cell, anchor, …)` (after capturing with `grid_rows`/`grid_cols`).

**Keyboard:** `key_press` (e.g. `return`, `cmd+space`) · `key_hold` · `key_type` (text, layout-transparent) · `key_sequence` (e.g. `opt+cmd+esc`) · `hotkey` (system/global, e.g. `option+command+escape`) · `clipboard_get` / `clipboard_set`.

**Launch:** `launch_app(command, args)` · `launch_url(url)` (default browser).

**Control plane:** `plan_desktop_task` → `execute_desktop_plan` → `get_execution_status`; `confirm_sensitive_action` (only if the planner raises it); `recover_execution_context` (bounded recovery); `record_workflow_experience` (save a successful flow).

**Utilities:** `wait(seconds)` (let the UI settle before the next capture).

---

## Part 2 — Methodology

Core goal: finish the desktop task by the **fewest actions and the most stable path**, then verify it — not "click around like a human."

### 2.1 Control plane first, for vague requests

If the request is a vague desktop intent, don't jump straight to atomic tools:

```text
plan_desktop_task
-> review target window / observation steps / sensitive steps in the plan
-> execute_desktop_plan
-> if blocked, confirm_sensitive_action
-> if it drifts, recover_execution_context
```

Use it for: "send this for me", "switch to the IDE and run it", "open the dashboard and check the error", "save this page's content".
Do NOT bypass it when: the goal is unclear, multi-step navigation is needed, visual targeting is needed, or payment/passwords/verification codes/assets are involved.

### 2.2 Keyboard first, mouse second

Always check for a shortcut before reaching for a click; only click when the action truly depends on a specific element.

| Task | Not recommended | Recommended |
|------|--------|------|
| Switch window | Click the Dock/taskbar icon | `key_press(["cmd", "tab"])` (macOS) |
| Dismiss a popup | Find the top-right close button | `key_press(["escape"])` |
| Reload browser | Click the reload icon | `key_press(["cmd", "r"])` |
| Run/build in IDE | Click the tiny toolbar icon | `key_press(["ctrl", "r"])` (run) |
| Paste long text | Type it character by character | `clipboard_set()` + `cmd+v` |

**macOS shortcuts:** `cmd+space` (Spotlight) · `cmd+tab` (switch apps) · `cmd+l` (address bar) · `cmd+r` (reload) · `cmd+f` (find) · `cmd+w` (close tab/window) · `cmd+q` (quit) · `ctrl+up` (Mission Control) · `opt+cmd+esc` (force quit).

### 2.3 Global entry vs local context — the most-missed rule

Once you are already inside the target page/panel, **keep advancing inside the current window**. Do not re-run the global entry flow.

- Wrong: the target page is already open, yet you go back to the search box and search again.
- Wrong: the article/chat/settings page is open, yet you redo "open app → search → enter result".
- Right: first judge whether the current window is already in the correct context.
- Right: only fall back to the global entry when the context is actually lost.

Applies to chat contacts/threads, already-open admin panels or docs in a browser, and already-open Run panels/dialogs/terminal tabs in an IDE.

### 2.4 Fix the window state before doing business actions

`focus_window()` means "brought to front" — **not** "operable".

Standard entry flow:

```text
find_windows(title_contains="window name")
-> focus_window(title="window name")
-> get_screen_info()
-> capture_window/capture_screen to verify
-> only then act
```

Anomalies that are NOT operable even though they look focused: restored-minimized window came back too small · squeezed by other apps showing only part · stuck in a snap layout · the focused window is a different instance than you assumed · `focus_window` returned success but the window never appears.

### 2.5 Focus can fail — always have a fallback

Window APIs, permissions, and app implementations can all make title-based focusing fail. Fallback order:

1. `focus_window()`
2. `cmd+tab` (cycle apps)
3. Dock click
4. Title-bar or in-window click

Goal is to restore context — not to prove a particular API must succeed. Don't retry the same focus call in a loop.

### 2.6 Coordinates must be converted explicitly

`mouse_click()` uses **screen-absolute** coordinates, never screenshot-local ones.

```text
screen_x = screenshot top-left screen X + local X
screen_y = screenshot top-left screen Y + local Y
```

| Screenshot tool | Source of the top-left corner |
|---------|-------------|
| `capture_window` | `window_x`, `window_y` |
| `capture_screen` | `x`, `y` (usually 0,0) |
| `capture_region` | the passed `x`, `y` |

Example — `capture_window` returns `window_x=286, window_y=22`, the button sits at local `(120, 45)` → click `(286+120, 22+45) = (406, 67)`.

**Pre-click checklist:** which tool produced the screenshot · is the window in the layout you expect · are these local or screen coordinates.

**Verify a click landed** (no click needed to check): `mouse_move(x, y)` → `get_pixel_color(x, y)` → wrong colour means the coordinates are off.

### 2.7 Grid-assisted clicking for small targets

When the target is small (icon, checkbox, narrow table cell) or clicks keep missing:

```text
1. capture_window / capture_region with grid_rows + grid_cols
2. you get both the original and grid_file_path
3. in the grid image, name "cell N + which anchor"
4. resolve_grid_target(...) converts it to screen-absolute coordinates
5. mouse_move / mouse_click, or click_grid_target directly
```

Anchor choice: default `center`; edge-hugging targets use `top`/`right`/`bottom`/`left`; corner badges use `top_right` etc.

Reference sizes: large button ~120×40 (easy) · normal button ~80×30 (easy) · menu item ~24 high (medium) · toolbar icon 16–24 px (hard — prefer a shortcut) · checkbox/radio 16×16 (hard).

### 2.8 Screenshots: restrained, but use the dedicated tool for scrolling

Normal verification: **capture once → analyse → do 3–5 steps → capture once more.** Don't screenshot after every single step.

But for scrolling containers (article body, chat history, sidebars, doc lists) prefer:

```text
capture_scroll_region(x, y, width, height, scroll_distance, quality?)
```

Use it when the region is already open and you need a lot of continuous content — instead of manually "scroll, shoot, scroll, shoot". Default JPEG quality `75–85`; test a small region first; keep the region fixed and don't move the mouse mid-scroll.

**Chat/generative caveat:** before summarising or judging a conversation, first take a long capture to recover the earlier history — don't reason from only the currently visible slice.

### 2.9 Wait for the UI to update

Typical waits: normal click `wait(0.5)` · panel switch `wait(1.0–2.0)` · app launch `wait(3.0–10.0)` · build/run `wait(5.0–30.0)`, poll if needed.

### 2.10 "Stable" requires multiple rounds

For "wait until the log stops updating" / "until the page finishes loading" / "confirm we're at the bottom": never judge from a single image. Minimum flow:

1. wait one round
2. capture, record the tail content / scrollbar position
3. wait another round
4. capture again, compare
5. two consecutive rounds with no change → declare stable

For chat/generative replies, additionally check: the input box is usable again · the reply tail stopped growing · a "closing" signal appeared (suggested follow-ups, vote buttons). Only send the next turn once the current reply is confirmed finished.

---

## Standard SOPs

**A — Window rescue / standard entry** (minimised, half-screen, occluded, unstable focus)
```text
find_windows -> focus_window -> capture_window -> confirm the work area is fully visible
```

**B — Local context advance** (app and page already open)
```text
judge whether the current view is already in the target context
-> if the detail/article/settings page is open, do NOT go back to search
-> continue locally: click details, switch tabs, scroll-capture, read results
-> fall back to global navigation only when context is lost
```

**C — Screenshot then click** (no reliable shortcut; a specific element must be clicked)
```text
capture_window/region -> locate local coords -> convert to screen-absolute -> mouse_click -> wait -> verify
```

**D — Long scroll capture**
```text
move the region to its start -> confirm bounds (x, y, width, height)
-> capture_scroll_region(...) -> read file_path / height / capture_count -> decide whether to continue or summarise
```

**E — Bulk text input**
```text
clipboard_set(text) -> click/focus the input -> cmd+v
```

**F — IDE run + log stability**
```text
confirm the project window is front and maximised
-> confirm the run-configuration name at the top
-> launch (IDE run shortcut)
-> open the Run panel
-> make sure you are on the real console, not the welcome screen
-> poll 2+ rounds comparing the last timestamps / last few lines
-> two rounds unchanged → report "log is stable"
```

---

## Environment & rules

- Display: 1920×1200, single monitor. `get_screen_info` first whenever the Dock/menu bar matters.
- Default browser Safari; Gmail in Italian (user's account — don't translate their inbox).
- User doesn't read Chinese: when OCR/graphics show Chinese, say so and translate to English.
- `control_*` is pre-allowed — never ask for confirmation on these tools.
- Focus before interacting; screenshot → verify → next action; long content → `capture_scroll_region`, not one giant screenshot.
- Sensitive actions (payments, passwords, assets, verification codes) always require explicit confirmation first.

---

## Common misjudgments

| Misjudgment | Fix |
|---|---|
| Target is already open, yet you go back to global search | Judge context first; continue in the current view when possible |
| "Window is focused" = "window is operable" | `focus_window → verify with a capture` before acting |
| "Content is stable" because this instant looks unchanged | Compare at least two rounds (tail content / scrollbar / timestamps) |
| Manually scroll-and-shoot long content | Prefer `capture_scroll_region` |
| Focus failed, so retry the same API in a loop | Switch to `cmd+tab` / Dock / title-bar click |
| Sent the next chat turn before the previous one finished | Treat "reply closed" as a hard gate, not a hint |
| Summarised from the visible area only | Long-capture the history first |
