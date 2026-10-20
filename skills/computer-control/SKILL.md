---
name: computer-control
description: |
  Control your computer through ControlMCP: screenshots, mouse clicks, keyboard
  input, clipboard, window management and long-scroll captures.
  For desktop automation, IDE/browser/office-app operation, capturing scrolling
  containers, launching programs, waiting for interfaces to settle, and judging
  whether log/page content has stopped changing.
---

# Computer Control

Goal: complete and verify desktop tasks with the fewest actions and most reliable paths.

- Keyboard first — clicking is the fallback
- Vague/multi-step intent → control plane (`plan_desktop_task`), not raw atomics
- Fix window/context state first, then do the business action
- Already in the target context → keep going locally; don't re-enter global flows
- Max verification from minimum screenshots; explicit judgments for "ready/loaded/stable/captured"
- Payment, password, verification-code, asset actions always require explicit confirmation
- Misused shortcut or derailed screen → `recover_execution_context`, don't operate on assumptions
- Small targets / uncertain positions → grid-assisted capture, never estimated-coordinate clicks

## Control plane first

Vague desktop intent → don't call low-level tools directly:

```text
plan_desktop_task → review target windows / observation steps / sensitive steps
→ execute_desktop_plan → (blocked: confirm_sensitive_action | derailed: recover_execution_context)
```

Use when: "Send this for me", "Switch to the IDE and run it", "Open the dashboard and check the error". Skip only for single atomic actions with a clear target. Never skip when the goal is unclear, multi-step, needs visual location, or touches payments/passwords/codes/assets.

## Quick entry & window state

Order: `find_windows(title_contains=…)` → `focus_window(title=…)` → `get_screen_info()` → verify with a capture.

- `focus_window` = foreground, NOT operable. Preferred: `focus_window → wait(0.5) → capture_window/capture_screen verify`.
- Minimized/half-screen/occluded → restore first (macOS: `Option+click` green button = zoom/maximize, `Ctrl+Cmd+F` = full screen, `Ctrl+Up` = Mission Control; or double-click title bar).
- `focus_window` succeeds but window never appears on screen → stop retrying focus; the window is hidden/minimized/closed-but-app-running. Recover via Dock (click/⌘-click Dock icon), Mission Control, or `recover_execution_context(strategy="window_rescue", target_window=…)`.
- Focus API fallback order: `focus_window` → `Cmd+Tab` → Dock click → title-bar click.
- Occluded by other windows: `focus_window` → `Cmd+Tab`; if still messy: `recover_execution_context` or open Mission Control (`Ctrl+Up`) and pick the window.
- Already in the target context (target page/tab/open file visible) → do NOT redo global flows like search-app/open-again. Only fall back to global entry when context is lost.

## Keyboard first

| Task | Not recommended | Recommended |
|------|-----------------|-------------|
| Switch apps | Click Dock icon | `key_press ["cmd","tab"]` |
| Close popup | Find the ✕ | `key_press ["escape"]` |
| Refresh browser | Click refresh icon | `key_press ["f5"]` |
| Large text input | Type char by char | `clipboard_set` + `key_press ["cmd","v"]` |
| Find in page | Scan visually | `key_press ["cmd","f"]` |

Global vs local: before any navigation, judge whether the current window is already in the right context. Applies to chat contacts/article pages, open dashboards/settings, IDE run panels/tabs.

## Coordinates

`mouse_click` uses **screen-absolute** pixels; captures are local:

```text
screen_x = window_x + local_x ; screen_y = window_y + local_y
```

`capture_window` → add window origin; `capture_region` → add region top-left; `capture_screen` → coords ARE screen coords. If pixel math matters (Dock/menu bar): `get_screen_info()` first. Details: [docs/coordinate-system.md](./docs/coordinate-system.md).

## Screenshots & scrolling

- Routine rhythm: **1 screenshot → execute 3–5 steps → 1 verification screenshot**. Never screenshot after every step.
- Long/scrolling content (article, chat history, lists) → `capture_scroll_region(x, y, width, height, scroll_distance, quality?)`: quality 75–85, one small trial first to confirm the region, keep the region fixed (don't move the mouse during capture), then read the returned `file_path/height/capture_count`. This replaces manual "scroll → shot → scroll → shot" loops.
- Small/legible region beats full screen: `capture_region`/`capture_window` with `max_width=960`, `quality=70–80` for fast analysis.
- Tiny target: capture with `grid_rows`+`grid_cols` → specify cell + anchor (default `center`; edge targets use edge anchors; corner badges use e.g. `top_right`) → `click_grid_target`, or `resolve_grid_target` → `mouse_move`/`mouse_click`.

## Waits & stability

Waits: normal click `0.5s` · panel switch `1–2s` · app launch `3–10s` · build/run `5–30s` (poll).

"Content has stopped updating / page loaded / reached bottom" → never trust one image:
1. Wait a round → capture (note tail content / scrollbar / timestamps)
2. Wait another round → capture → compare
3. **Two consecutive rounds with no change → declare stable** (compare tail, scrollbar position, timestamps — not the instant view)

Chat/LLM-streaming flow:
- Summarize/judge a conversation → capture the history ABOVE first (`capture_scroll_region` on the chat body, not the input box/list); never conclude from the visible fragment.
- "Reply finished" is a **hard gate** before the next round: input box back to ready · tail stopped growing · closing signals present (follow-up suggestions, 👍/👎) · after sending, ≥1 wait + 1 recheck (2 for long replies) · no blind follow-ups on a fixed timer.
- Mid-derailed reply → locate the derailment point in history first, then decide whether to send a corrective nudge.

## Standard procedures

**A. Window rescue:** `find_windows` → `focus_window` → restore/zoom → `wait(0.5)` → `capture_window(quality=75, max_width=960)` → confirm workspace fully visible.

**B. Click after screenshot:** capture → locate element → convert coords → `mouse_click` → `wait(0.5–2.0)` → verify only if needed.

**C. Large text:** `clipboard_set` → focus input box → `key_press ["cmd","v"]`.

**D. Chat round:** long-capture body history → confirm previous round complete → click input → paste → send → `wait(1–3s)` → recheck generation started → wait+recheck tail/input-box/closing signals → only then next round → final history re-capture before summarizing.

**E. IDE run & log stability (JetBrains):** window foreground + correct run config (`Alt+Shift+F10` to re-select) → run → open Run panel (`Alt+4`) → confirm it's the actual console, not the welcome page → poll ≥2 rounds comparing last timestamps/lines → no change in consecutive rounds → "logs stable". macOS keymap differs from Windows defaults — `Ctrl+Shift+A` (Find Action) is the universal escape hatch.

## Quick reference

| JetBrains (Windows keymap) | Shortcut | macOS window mgmt | Shortcut |
|---|---|---|---|
| Run current configuration | `Shift+F10` | Switch apps | `Cmd+Tab` |
| Restart config | `Ctrl+F5` | Minimize / close / quit | `Cmd+M` / `Cmd+W` / `Cmd+Q` |
| Stop | `Ctrl+F2` | Mission Control | `Ctrl+Up` |
| Build project | `Ctrl+F9` | Hide app | `Cmd+H` |
| Run panel | `Alt+4` | Next window (same app) | `` Cmd+` `` |
| Terminal | `Alt+F12` | Full screen | `Ctrl+Cmd+F` |
| Find Action | `Ctrl+Shift+A` | Snap left/right equivalent | drag to screen edge |

| Browser | Shortcut |
|---|---|
| Refresh / hard refresh | `F5` / `Ctrl+F5` |
| Address bar / find | `Ctrl+L` / `Ctrl+F` (macOS: `Cmd+L` / `Cmd+F`) |

## Chrome human-verification (Cloudflare) prompts

When chrome-devtools shows "confirm you are human" / Turnstile, don't blind-click via DOM:

1. Keep the browser foreground; don't refresh
2. `capture_window`/`capture_region` (+ grid if small) to locate the checkbox
3. `click_grid_target` / converted `mouse_click` on screen
4. `wait(1–2s)` → back to `chrome-devtools_take_snapshot`/`wait_for` to confirm pass

Division: chrome-devtools = page structure/navigation; ControlMCP = real-screen clicks (also for iframe checkboxes visible in DOM but not accepting DOM clicks).

## Documentation index

- Coordinate conversion: [docs/coordinate-system.md](./docs/coordinate-system.md)
- Window management & rescue: [docs/window-management.md](./docs/window-management.md)
- JetBrains run & log observation: [docs/idea-run-workflow.md](./docs/idea-run-workflow.md)
