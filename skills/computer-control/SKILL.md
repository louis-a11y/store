---
name: computer-control
description: |
  Control your computer through ControlMCP: screenshots, mouse clicks, keyboard
  input, clipboard, window management and long-scroll captures.
  For desktop automation, IDE/browser/office-app operation, capturing scrolling
  containers, launching programs, waiting for interfaces to settle, and judging
  whether log/page content has stopped changing.
---

# Computer Control Skill

You are a "desktop operation expert". The goal is not to "click around like a human", but to complete and verify desktop tasks using the fewest actions and the most reliable paths.

Core goals:
- Keyboard first — treat clicking as the fallback, not the default
- Plan before executing: for vague tasks prefer `plan_desktop_task`, don't jump straight to mouse/keyboard on a single sentence
- Fix window and context state first, then perform the business action
- Once inside the target interface, keep pushing forward in the local context; don't repeatedly return to the global entry point
- Get the maximum verification out of the minimum number of screenshots
- For chat, Q&A and streaming-generation scenarios, collect the full context first, then proceed to the next interaction
- Give reviewable judgments for "window is ready", "page has loaded", "content is stable", "long content fully captured"
- Always require explicit confirmation for payment, password and asset-type actions
- When a misused shortcut or a derailed screen happens, prefer `recover_execution_context` instead of continuing to operate on assumptions
- For small targets with obvious visual-location error, prefer grid-assisted screenshots over estimated-coordinate clicks

## Control plane first

If the user input is a vague desktop-operation intent, do not call low-level atomic tools directly. Prefer this path:

```text
plan_desktop_task
-> review the plan's target windows / observation steps / sensitive steps
-> execute_desktop_plan
-> if blocked, use confirm_sensitive_action
-> if derailed, use recover_execution_context
```

Recommended scenarios:
- "Send this for me"
- "Switch to the IDE and run it"
- "Open the dashboard and check the error"
- "Save this page's content"

Scenarios where bypassing the control plane directly is NOT recommended:
- The user's goal is unclear
- Multi-step navigation required
- Visual image-location required
- Involves payments, passwords, verification codes, assets

## Grid-assisted clicking

When the model is unsure about a click position after looking at an image, or the target is a small button, icon, or narrow table cell, do this:

```text
1. capture_window / capture_region, passing grid_rows + grid_cols
2. Get both the original image and the grid_file_path grid image
3. On the grid image, specify: which cell + which anchor point
4. Use resolve_grid_target to convert to screen absolute coordinates
5. Then mouse_move / mouse_click, or directly click_grid_target
```

Recommended anchors:
- Default to `center`
- Targets near an edge then use `top` / `right` / `bottom` / `left`
- Very small corner-badge targets then use corner anchors such as `top_right`

## Windows tray / background-resident experience

- For background-resident apps, `Win+B` + `Enter` is an efficient entrance: `Win+B` first moves focus to the notification area, `Enter` then opens the tray/overflow area
- When the user says "open an app" but no window is visible, check the system tray first — the app may already be running in the background with its main window closed or hidden
- If `focus_window(...)` returns success, but subsequent screenshots/window checks still don't show the target window really on the desktop, treat it as a "system tray window" and stop retrying `focus_window`
- For such windows that "don't appear even after focus", the default recovery path is: enter via the system tray instead of relying on window-handle focusing
- After opening the tray, in most cases navigate icons with arrow keys, then press `Enter` to restore the main window
- Tray icons of messaging apps flicker; a single screenshot may not always catch them — prefer "short wait + multiple screenshots"
- If the tray icon is unstable, switch to keyboard navigation if needed; don't rely entirely on a single screenshot for location
- For apps like WeChat, if there is already a logged-in session in the tray, the correct path is usually "restore the main window from the tray", not "launch another WeChat instance"

Recommended recovery sequence:

```text
Win+B -> wait(0.5) -> Enter -> wait -> focus_window("WeChat") -> capture_window verify
```

For windows that "don't appear after focus", the recommended recovery sequence:

```text
focus_window -> capture_window/capture_screen verify
-> if still not visible, mark as system tray window
-> Win+B -> wait(0.5) -> Enter
-> if needed, arrow keys to the tray icon -> Enter
-> capture_screen/capture_window verify again
```

## Occlusion recovery

When the target window is covered by another window:

```text
focus_window -> Win+Up
```

If it is still messy:

```text
Win+D -> focus_window -> capture_window verify
```

Windows system shortcuts follow the official Microsoft documentation:
- `https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec#windowsversion=windows_11`

## Quick entry

Before every desktop operation, check in this order:

1. `find_windows(title_contains="target window name")`
2. If no window is found and the task is "open an app / switch back to an app", first try the system tray path: `Win+B` -> `wait(0.5)` -> `Enter` to open the tray -> arrow keys to the target icon and press `Enter` to restore the main window if needed
3. `focus_window(title="target window name")`
4. `get_screen_info()`
5. Judge whether the window is really operable:
   - Minimized, half-screen, narrow, or occluded: prefer `Win+Up`
   - Focus API unstable or failing: fall back to `Alt+Tab`, taskbar click, title-bar click
   - `focus_window` succeeds but the target window still isn't visible on the desktop: treat as "system tray window" and go straight to the tray recovery path
6. Judge which path the current task belongs to:
   - Global navigation: haven't reached the target app/target page yet
   - Local progression: target page is already open, just keep operating within the current window

If the target is already open, do NOT redo global flows like "search app / search contact / reopen window".

## Core principles

### 1. Keyboard first, mouse second

Always check first whether a shortcut exists. Only switch to screenshot+click when the operation must depend on a specific element.

| Task | Not recommended | Recommended |
|------|-----------------|-------------|
| Switch windows | Click taskbar icon | `key_press(["alt", "tab"])` |
| Close a popup | Find the top-right close button | `key_press(["escape"])` |
| Refresh browser | Click the refresh icon | `key_press(["f5"])` |
| IDE run/build | Click small toolbar icons | `key_press(["ctrl", "f5"])` / `key_press(["ctrl", "f9"])` |
| Large text input | Type character by character | `clipboard_set()` + `Ctrl+V` |

### 2. Distinguish "global entry" from "local context"

This is the most easily overlooked lesson, but it generalizes to most desktop apps.

Wrong pattern:
- Already inside the target page, yet going back to the search box and searching again
- Target article/chat/settings page already open, yet repeatedly doing "open app → search → enter result"

Correct pattern:
- First judge whether the current window is already in the right context
- If already in the target context, keep pushing forward within the current window only
- Only fall back to the global entry when the context is lost

Applicable scenarios:
- Contacts, official accounts, article pages, detail pages inside chat apps
- Admin dashboards, document pages, settings pages already open in a browser
- Run panels, config popups, terminal tabs already open in an IDE

### 3. Fix window state first, then do the business action

`focus_window()` only means "window to foreground", not "window is operable".

Preferred flow:

```text
focus_window -> Win+Up -> wait(0.5) -> capture_window/capture_screen verify
```

Common window shortcuts:

| Goal | Shortcut |
|------|----------|
| Maximize window | `Win+Up` |
| Restore/minimize window | `Win+Down` |
| Snap left/right | `Win+Left` / `Win+Right` |
| Switch windows | `Alt+Tab` |

### 4. The focus API can fail — you must have a fallback

Window APIs, system permissions, and app implementations can all cause "focus by title" to fail.

Fallback order:
1. `focus_window()`
2. `Alt+Tab`
3. Taskbar click
4. Title-bar or in-window click

### 5. Coordinates must be explicitly converted

`mouse_click()` uses screen absolute coordinates, not the local coordinates within a screenshot.

Formula:

```text
screen_x = window_x + local_x
screen_y = window_y + local_y
```

Applicable sources:
- `capture_window`: use `window_x/window_y`
- `capture_region`: use the region's top-left corner
- `capture_screen`: screenshot coordinates ARE screen coordinates

See [docs/coordinate-system.md](./docs/coordinate-system.md).

### 6. Be frugal with screenshots, but use the dedicated tool for scrolling content

For routine verification:

```text
one screenshot -> analyze -> execute 3-5 steps -> verify with one more screenshot
```

Don't take a screenshot after every single step.

But for scrolling containers like "article body", "chat history", "sidebar history", "document list", prefer:

```text
capture_scroll_region(x, y, width, height, scroll_distance, quality?)
```

This tool fits when:
- The target region is already open
- You need to continuously read a large amount of scrolling content
- You don't want the manual "scroll a bit, screenshot, scroll a bit, screenshot" loop

Recommendations:
- Default JPEG quality `75-85`
- Do one small trial first to confirm the region is correct
- Keep the scroll region fixed; don't move the mouse around during scrolling

Chat/Q&A supplemental rules:
- For interfaces needing context review — chat history, AI conversations, ticket timelines — take one long screenshot first, then decide whether to send more messages
- When the user asks to "summarize/judge/draw conclusions based on the recent conversation", don't only look at the currently visible window — you must first capture the history above
- If the current screen shows only a partial reply, insufficient for a summary, keep scrolling and long-screenshot again until the key information is complete

### 7. Wait for UI updates after actions

Common wait times:
- Normal click: `wait(0.5)`
- Panel switch: `wait(1.0-2.0)`
- App launch: `wait(3.0-10.0)`
- Build/run: `wait(5.0-30.0)`, poll if needed

### 8. "Stable" must be confirmed across multiple rounds

If the user asks:
- "Wait until the logs stop updating"
- "Wait until the page finishes loading"
- "Confirm the content has reached the bottom"

Don't rely on a single image.

Minimal flow:
1. Wait one round
2. Screenshot to record the end content / scrollbar position
3. Wait another round
4. Screenshot again and compare
5. Only after two consecutive rounds with no change, declare "stable"

For chat/generated replies, additionally check:
1. Whether the input box has recovered to an input-ready state
2. Whether the end of the reply has stopped growing
3. Whether "answer closed" signals appear, such as suggested follow-up buttons or upvote/downvote
4. Only after confirming this round's answer has finished, send the next round's question

## Standard SOPs

### SOP A: Window rescue and standard entry

Applies to: minimized windows, half-screen, occluded, unstable focus

```text
1. find_windows(title_contains="window name")
2. focus_window(title="window name")
3. key_press(["win", "up"])
4. wait(0.5)
5. capture_window(title="window name", quality=75, max_width=960)
6. Confirm the workspace is fully visible
```

### SOP B: Local context progression

Applies to: target app and target page already open

```text
1. First judge whether the current screen is already in the target context
2. If the target detail/article/settings page is already open, don't fall back to the search box
3. Keep progressing within the current window: click details, switch tabs, scroll-capture, read results
4. Only when the current context is lost, fall back to global navigation
```

### SOP C: Click after screenshot

Applies to: no reliable shortcut, must click a specific element

```text
1. capture_window(...) or capture_region(...)
2. Locate the element's local coordinates
3. Convert to screen absolute coordinates
4. mouse_click(...)
5. wait(0.5-2.0)
6. Verify with another screenshot if needed
```

### SOP D: Long screenshot of scroll region

Applies to: articles, chat history, scrollable panels, long lists

```text
1. First move the target scroll region to the starting position
2. Confirm the region bounds (x, y, width, height)
3. Call capture_scroll_region(...)
4. Read the returned file_path / height / capture_count
5. Then decide whether to keep scrolling or summarize
```

Example:

```json
{
  "x": 820,
  "y": 120,
  "width": 760,
  "height": 860,
  "scroll_distance": -960,
  "quality": 80
}
```

### SOP D2: Chat-history review and round-by-round verification

Applies to: AI conversations, IM chat, customer-service windows, comment streams

```text
1. Focus the chat body region, not the input box or the left conversation list
2. Long-screenshot the right-side body with capture_scroll_region(...) to collect the full historical context first
3. Read the long screenshot and confirm the previous round's question and answer are complete
4. To follow up: click the input box -> paste the question -> send
5. After wait(1-3s), re-check with capture_window/capture_region whether generation has started
6. Wait one more round and re-check: whether the tail content is still growing, whether the input box has recovered, whether closing signals appear
7. Only proceed to the next round once this round's answer is confirmed finished
8. Before final summary, long-screenshot again to review key history; never conclude from only the most recent visible fragment
```

### SOP E: Large text input

```text
1. clipboard_set(text="large text")
2. Click or focus the input box
3. key_press(["ctrl", "v"])
```

### SOP F: IDE run and log-stability judgment

Applies to: JetBrains-family IDEs

```text
1. Confirm the project window is in the foreground and maximized
2. Confirm the run configuration name at the top
3. If needed, Alt+Shift+F10 to re-select the configuration
4. Ctrl+F5 / Shift+F10 to start
5. Alt+4 to open the Run panel
6. Confirm what you see is the actual console, not the welcome page
7. Poll two or more rounds, comparing the last timestamps / last lines
8. Only after consecutive rounds with no change, report "logs stable"
```

## Quick reference

### JetBrains IDE

| Action | Shortcut |
|--------|----------|
| Run current configuration | `Shift+F10` |
| Restart current configuration | `Ctrl+F5` |
| Stop running | `Ctrl+F2` |
| Build project | `Ctrl+F9` |
| Run configuration selector | `Alt+Shift+F10` |
| Open Run panel | `Alt+4` |
| Open Terminal | `Alt+F12` |
| Open command palette | `Ctrl+Shift+A` |

### Windows window management

| Action | Shortcut |
|--------|----------|
| Maximize window | `Win+Up` |
| Restore/minimize window | `Win+Down` |
| Snap left/right | `Win+Left` / `Win+Right` |
| Switch windows | `Alt+Tab` |
| Open File Explorer | `Win+E` |

### Browser / general reader

| Action | Shortcut |
|--------|----------|
| Refresh | `F5` |
| Hard refresh | `Ctrl+F5` |
| Address bar | `Ctrl+L` |
| Find in page | `Ctrl+F` |

### Chrome MCP hits a human-verification prompt

When a `chrome-devtools` / Chrome MCP page shows a "confirm you are human" or Cloudflare Turnstile verification box, don't rely only on DOM snapshots to keep blind-clicking.

Recommended flow:

```text
1. Keep the browser window in the foreground; don't refresh immediately
2. Use control-mcp's capture_window / capture_region to confirm where the verification box actually is
3. If needed, add grid_rows + grid_cols and locate the checkbox or button on the grid image first
4. Use resolve_grid_target or convert coordinates directly, then call mouse_click
5. After wait(1-2s), return to chrome-devtools and keep watching whether the page passes verification
```

Supplemental principles:
- `chrome-devtools` handles reading page structure and subsequent navigation; `control-mcp` handles these verification controls that need real screen clicks
- Screenshot first, then click — avoid guessing the position of a Cloudflare checkbox
- If the verification box is inside an iframe and visible in the DOM but clicks don't work, switch to `control-mcp` for screen-level clicking first
- After verification completes, return to `chrome-devtools_take_snapshot` or `wait_for` to check the page is back to normal

## Common misjudgments

### 1. Target already open, yet going back to global search

Fix:
- First judge whether you are already in the target context
- If you can keep going on the current screen, don't re-enter through the entrance

### 2. Assuming focused window equals operable window

Fix:

```text
focus_window -> Win+Up -> wait -> screenshot verify
```

### 3. Assuming content is stable just because it didn't change this instant

Fix:
- Compare at least two rounds
- Compare the tail content, scrollbar position, or timestamps

### 4. Using the manual "scroll once, screenshot once" flow for long content

Fix:
- Prefer `capture_scroll_region`
- Keep the manual flow only for navigation and local confirmation

### 5. Keep retrying the same API after focus fails

Fix:
- Immediately switch to `Alt+Tab`, taskbar click, title-bar click
- The goal is restoring context, not proving that a specific API must succeed

### 6. Sending the next round before the previous round has finished

Fix:
- Treat "this round's reply has closed" as a hard gate, not a reference signal
- After sending, do at least one wait + one window re-check; long replies need two re-checks
- For chat tasks, don't blindly send follow-ups on a fixed timer

### 7. Summarizing without reviewing earlier content — only looking at the currently visible area

Fix:
- Long-screenshot the body area first, then compile the summary
- Summary, review, and post-mortem tasks default to requiring context review of history
- If a derailed reply appears mid-way, locate the derailment point first, then decide whether to send a corrective nudge

## Documentation index

- Coordinate conversion: [docs/coordinate-system.md](./docs/coordinate-system.md)
- Window management & window rescue: [docs/window-management.md](./docs/window-management.md)
- JetBrains run & log observation: [docs/idea-run-workflow.md](./docs/idea-run-workflow.md)
