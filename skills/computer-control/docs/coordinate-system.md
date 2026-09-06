# Coordinate System Reference

> This document answers one question only: how to reliably convert "a position seen in a screenshot" into a ControlMCP-clickable screen coordinate.

## Core concept

ControlMCP uses the **screen absolute coordinate system**. All `mouse_click`, `mouse_move` and `mouse_drag` parameters are screen coordinates.

Prerequisites:
- First make sure the target window is really in an operable state
- If the window is minimized, half-screen, or has abnormal dimensions, fix the window first per [window-management.md](./window-management.md)

## Coordinate system diagram

```
Single monitor:
(0,0)┌─────────────────────────┐
     │  Primary monitor        │
     │  1920 × 1080            │
     │                         │
     │  (960, 540) = screen center
     │                         │
     │                    (1919, 1079)
     └─────────────────────────┘

Dual monitor (left + right):
(0,0)┌──────────────┐(1920,0)┌──────────────────┐
     │  Monitor 1   │        │  Monitor 2       │
     │  1920×1080   │        │  2560×1440       │
     │              │        │                  │
     └──────────────┘        │            (4479, 1439)
                             └──────────────────┘

Dual monitor (top+bottom or left+right with offset):
Depends on system settings; confirm with get_screen_info().
```

## Full flow from screenshot to click

### Case 1: Using capture_window

```
capture_window returns:
{
  "window_x": 286,        ← screen X of the window's top-left corner
  "window_y": 22,         ← screen Y of the window's top-left corner
  "window_width": 1404,   ← window width
  "window_height": 990,   ← window height
  "screenshot_width": 1404,
  "screenshot_height": 990
}

You see a button in the screenshot at pixel position (120, 45)

screen coordinates = (286 + 120, 22 + 45) = (406, 67)
```

### Case 2: Using capture_screen (full-screen screenshot)

```
capture_screen returns:
{
  "width": 1920,
  "height": 1080,
  "x": 0,
  "y": 0
}

The button position in the screenshot, (960, 540), IS the screen coordinate — no conversion needed.
```

### Case 3: Using capture_region (region screenshot)

```
capture_region(x=100, y=200, width=400, height=300) returns:
{
  "x": 100,   ← screen X of the region's top-left corner
  "y": 200,   ← screen Y of the region's top-left corner
}

The button in the screenshot is at (50, 30)

screen coordinates = (100 + 50, 200 + 30) = (150, 230)
```

## Generic conversion formula

```
screen_x = screenshot top-left screen X + button X within screenshot
screen_y = screenshot top-left screen Y + button Y within screenshot
```

| Screenshot tool | Source of top-left corner |
|---------|-------------|
| `capture_window` | `window_x`, `window_y` |
| `capture_screen` | `x`, `y` (usually 0,0) |
| `capture_region` | the passed `x`, `y` parameters |

## Grid-assisted clicking (recommended for small targets)

If the target is small, or the model's clicks keep landing off-target, prefer grid-assisted screenshots.

### Step 1: Generate the grid image

```text
capture_window(title="target window", grid_rows=3, grid_cols=4)
```

The return value will include both:
- `file_path`: the original image
- `grid_file_path`: the grid overlay image
- `grid_rows` / `grid_cols`

### Step 2: Have the model describe only "cell + anchor"

For example:

```text
center of cell 6
right edge of cell 8
top-right corner of cell 3
```

### Step 3: Convert to screen coordinates

```text
resolve_grid_target(
  base_x=window_x,
  base_y=window_y,
  image_width=screenshot_width,
  image_height=screenshot_height,
  grid_rows=3,
  grid_cols=4,
  cell=6,
  anchor="center"
)
```

### Supported anchors

| Anchor | Description |
|------|------|
| `center` | Cell center |
| `top_left` | Inset point at top-left corner |
| `top` | Inset point at top edge midpoint |
| `top_right` | Inset point at top-right corner |
| `right` | Inset point at right edge midpoint |
| `bottom_right` | Inset point at bottom-right corner |
| `bottom` | Inset point at bottom edge midpoint |
| `bottom_left` | Inset point at bottom-left corner |
| `left` | Inset point at left edge midpoint |

## Pre-click checks

Before actually clicking, confirm at least these three things:

1. What is the screenshot source: `capture_window`, `capture_screen`, or `capture_region`
2. Whether the window is maximized or in the layout you expect
3. That the identified coordinates are in-screenshot coordinates, not screen coordinates

Recommended order:

```text
fix window → screenshot → identify local coordinates → compute screen coordinates → click
```

## Common UI element size reference

For estimating click precision requirements:

| Element type | Typical size | Click difficulty |
|---------|---------|---------|
| Large button (e.g., "Submit") | 120×40 px | Easy |
| Normal button | 80×30 px | Fairly easy |
| Toolbar icon | 16-24×16-24 px | Hard (prefer a shortcut) |
| Menu item | variable width×24 px | Medium |
| Tab | 150×28 px | Fairly easy |
| Dropdown option | variable width×20 px | Medium |
| Checkbox | 16×16 px | Hard |
| Radio button | 16×16 px | Hard |
| Input field | variable×28-36 px | Easy (click center) |

## DPI scaling handling

Windows high-DPI scaling affects coordinates.

```
Monitor physical resolution: 3840 × 2160 (4K)
Windows scaling: 150%
Logical resolution: 3840/1.5 × 2160/1.5 = 2560 × 1440

get_screen_info() returns the logical resolution (2560×1440)
capture_window's window_x/y use logical coordinates
mouse_click's x/y use logical coordinates

So: all tools already handle DPI automatically — just use the returned values.
```

**Note:** If you notice clicks landing off-target, first confirm the returned resolution with `get_screen_info()`.
If the actual screenshot pixels and the returned values disagree, it may be a DPI issue.

## Verifying click accuracy

```
Step 1: mouse_move(x=target_x, y=target_y)
Step 2: color = get_pixel_color(x=target_x, y=target_y)
Step 3: inspect the color
  - If the target is a green button, expect RGB ≈ (76, 175, 80)
  - If on a white background, expect RGB ≈ (255, 255, 255)
  - If the color is completely wrong, the coordinates are off — fine-tune them
```