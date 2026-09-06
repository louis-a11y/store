# IDEA Launch and Log Observation

## Applicable scenarios

Applies to requests like:
- Launch a certain IDEA / PyCharm run configuration
- Wait until the console log stops updating, then report
- Check whether the currently running item is correct

## Workflow

### 1. Get into the correct window

```text
1. find_windows(title_contains="project name")
2. focus_window(title="project name")
3. Win+Up
4. wait(0.5)
5. capture_window verify
```

## 2. Confirm the run configuration

First look at the run configuration name at the top.

If you are unsure whether the current configuration is correct:

```text
1. Alt+Shift+F10
2. Type the target configuration name
3. Enter to select
```

Don't just assume the abbreviated name at the top matches the target configuration.

## 3. Launch the app

Common actions:
- Run current configuration (no run sub-window, or the run sub-window configuration is not the one you want to launch): `Shift+F10`
- Run current configuration (run sub-window exists and its configuration IS the one you want to launch) / restart current configuration: `Ctrl+F5`
- Run in debug mode: `Shift+F9`
- Stop the current run: `Ctrl+F2`
- Open the Run panel: `Alt+4`

## 3.1 Fallback material when shortcuts don't behave as expected

JetBrains-family IDE shortcut knowledge carries a premise:
- Different IDE products may differ
- Different versions may differ
- Install paths on different machines may differ
- If the user has modified the keymap, actual behavior may also differ

Therefore, when shortcuts don't behave as expected, handle it in this order:

1. First check the local IDE's shortcut PDF reference card
2. Then check the JetBrains official online documentation
3. Correct the action based on the current IDE, current version, and current keymap

Example local IntelliJ IDEA PDF:

```text
C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.2\help\ReferenceCard.pdf
```

Note:
- This path is only an example; don't hardcode it as the sole location
- Products like PyCharm, WebStorm, GoLand have different product names and install directories
- For the same product, directory names change between versions

Example official IDEA online resource:

```text
https://www.jetbrains.com/idea/resources/ (use the localized portal matching your region)
```

Applicable principles:
- Shortcut pressed with no response
- Shortcut triggered a different action
- Click position doesn't match expectations — go back to official material to confirm the entry name and UI location

## 4. Confirm the console panel

After launch, the Run panel may show two states:

### State A: Welcome screen

Characteristics:
- The panel says "To run code, do the following"
- No actual console output visible

This doesn't mean the program didn't launch; it only means you haven't switched to the actual running item.

### State B: Console page

Characteristics:
- You can see the `java.exe` command line, Spring logs, timestamps, or stdout output

## 5. If still on the welcome screen

How to handle:
- Check the Run tab bar at the bottom for a running-app tab
- Switch to the corresponding tab
- If needed, click on an entry like "Running applications"

Principle:
- Don't mistake the "welcome screen" for "no logs"

## 6. Determining whether the log has stopped updating

Don't observe only once.

Recommended polling:

```text
1. wait(5-10s)
2. capture_window
3. Record the last timestamp or the last 2-3 lines
4. wait(5-10s) again
5. capture_window
6. Compare again
7. If two rounds match, do a third round to confirm
```

Suggested standard for reporting "log has stopped updating":
- Two or more consecutive rounds with no new output
- The last batch of log timestamps no longer advances

## 7. Common misjudgments

### Misjudgment 1: Seeing the Run panel means you're already looking at the console

It may actually just be the welcome screen.

### Misjudgment 2: Judging "log stopped" from a single screenshot

The log may just be intermittent output.

### Misjudgment 3: Top configuration is correct, so the bottom run tab must be correct too

The bottom may actually be switched to another running item, or may not have switched to the console at all.

### Misjudgment 4: Assuming JetBrains-family IDE shortcuts are identical on all machines

They are actually affected by product, version, install directory, and the user's keymap.

Fix:
- First check the local PDF reference card
- Then check the official online documentation