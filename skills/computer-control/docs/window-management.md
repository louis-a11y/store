# Window Management Reference

## Core judgment

"Window in the foreground" does NOT equal "window is in an operable state".

Common anomalies:
- A minimized window comes back with a small size when restored
- The window is squeezed by other apps and only shows a partial area
- The window is stuck in a snap layout, leaving the work area incomplete
- The target window is focused, but it's not the project/app instance you think it is
- `focus_window()` returns success, but the target window doesn't actually appear on the desktop

## Tray-window determination

If you observe this pattern:

```text
focus_window("target window") -> returns success
but the target window still doesn't appear on the desktop in screenshot/visual verification
```

Treat it as a "system tray window" by default instead of repeatedly calling `focus_window()`.

Recommended handling order:

```text
1. Win+B
2. wait(0.5)
3. Enter opens the tray/overflow area
4. If needed, arrow keys to locate the target icon
5. Enter restores the main window
6. capture_screen / capture_window verify
```

Principles:
- `focus_window()` solves window-handle focusing; it does not guarantee restoring tray business-state
- "Still not visible after focus" means the entrance is not in the normal window layer, but in the system tray layer
- For such apps, tray click/keyboard entry is more stable than continuing to retry focusing

## Common shortcuts

### Windows

| Goal | Shortcut | Description |
|------|--------|------|
| Maximize window | `Win + Up` | Use after focusing the target window |
| Restore/minimize window | `Win + Down` | Restores normal size once; usually minimizes on a second press |
| Snap left | `Win + Left` | Use for side-by-side comparison |
| Snap right | `Win + Right` | Use for side-by-side comparison |
| Switch windows | `Alt + Tab` | Find the correct app instance |
| Show desktop | `Win + D` | Quick cleanup |

## Standard flows

### Scenario 1: Window may be minimized

```text
1. find_windows(title_contains="target title")
2. focus_window(title="target title")
3. key_press(["win", "up"])
4. wait(0.5)
5. capture_window(title="target title")
```

### Scenario 2: Need to view two windows side by side

```text
1. focus_window("window A")
2. Win+Left
3. focus_window("window B")
4. Win+Right
5. Screenshot each to confirm
```

### Scenario 3: Similar window titles — risk of switching to the wrong instance

```text
1. find_windows(title_contains="keyword")
2. Compare the returned titles and pick a more precise focus_window parameter
3. Screenshot after focusing to confirm
```

## Field experience

### Tip 1: Do a window correction right after `focus_window()`

Especially for complex windows like IDEs, browsers, and design software.

Recommended default action:

```text
focus_window → Win+Up → wait(0.5)
```

Reason:
- A restored minimized window is often not maximized
- Partial screenshots easily lead to misjudgments

### Tip 2: If the screenshot shows only "half a window", don't continue business operations

Fix the window first, then talk about clicking, running, and reading logs.

### Tip 3: Only use snap layouts when you need to preserve a layout

Maximize by default normally. Snapping is a task-driven exception, not the default layout.