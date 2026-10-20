---
name: image-reading
description: Use when the user wants to read or analyze an image, screenshot, photo, UI mockup, diagram, or document — "look at this", "what does this screenshot show", "read this image", "ocr", "see what's on screen". Bridges opencode to images via OCR + optional vision backend.
---

> # CUSTOMIZE-ME (edit from the file manager — Finder: ~/.config/opencode/skills/image-reading/SKILL.md)
>
> | Knob | Default | Change here |
> |---|---|---|
> | Main backend | `~/bin/vimg` — one-shot OCR + color scan (Vision framework) | swap for another OCR if you install one |
> | Description mode | disabled | set `VREAD_DESC_CMD="..."` (e.g. `ollama run llava "$1"` or a vision-API curl) then `vread --desc <img>` gives rich scene descriptions |
> | Capture fallback | ControlMCP `capture_screen` / `capture_region` → then vread the PNG | change tooling |
> | Screenshot archive | `/tmp/vread-*.png` (ephemeral) | switch to ~/Pictures if you want history |

## Goal

The model (big-pickle) is text-only — it cannot see pixels. `vread` is the bridge:
image → **text** → context. From the model's perspective this equals multimodality for
anything containing text: screenshots, UIs, docs, error dialogs, terminal output, QR codes.

## When to invoke

Trigger on: image paths dropped in chat, screenshots, "what does this show", "read/ocr this image",
"analyze this UI/screenshot", "is there an error on screen", "what's the text in this figure".

## Workflow

1. **Resolve the image**, in order of preference:
   - User gave a path → `vimg <path>`
   - User pasted/mentioned a screenshot → find or capture it
   - "What's on screen" → ControlMCP `capture_screen` → `vimg <saved.png>`
   - Region needed → ControlMCP `capture_region` → `vimg <saved.png>`
2. **Run**: `~/bin/vimg [-l] <image>` (absolute path — the bash tool's PATH may omit ~/bin).
   - Plain OCR (text only): `~/bin/vimg <image>`
   - Layout question (where things are): `~/bin/vimg -l <image>` — adds `[x y w h]` coords,
     normalized 0–1, **y=0 is TOP** (already flipped from Vision's bottom-up coords).
     Lines are sorted top-to-bottom, left-to-right, so reading order = output order.
   - BOTH modes also print a color summary (dominant hues % + avg rgb per horizontal band
     top-to-bottom) — enough to answer "what colors / dark or light theme" honestly.
   - Warm runs take ~0.5–1.2s. First run after a reboot can take ~1 min (Vision model
     cold-load) — that's a one-time cost, not a hang.
   - `~/bin/vread` is the older wrapper (still works; adds `-s`/`-r` capture flags and
     `--desc` mode) — prefer `vimg` unless you need those.
3. **Feed the text into reasoning.** Treat OCR output as what the image says, and answer
   from it. Quote interesting fragments back to the user when relevant.
4. **Visual judgment beyond coords+colors** (aesthetics, "does this UI look good",
   semantic layout): options, best first:
   - Try `multimodal-looker` agent if present and responsive (vision-capable model).
   - If `VREAD_DESC_CMD` is configured, `vread --desc <img>` produces scene descriptions.
   - Otherwise say plainly: "OCR + color scan read the text and rough layout; for real
     visual judgment I'd need a vision backend."
   Never claim to have seen pixels you only inferred from OCR coords and color averages.

## UX rules

- Fast path: capture + OCR is ~1-2s with the compiled binary — don't over-narrate, just do it.
- If OCR returns nothing: maybe the image is empty/dark/rotated — report that, suggest re-capture.
- Terminal output, error dialogs, console text: OCR is excellent; use it FIRST before asking the user to retype.
- The user's preference is terse — give the extracted text + the answer, not a transcript of tool calls.

## Backend recipes (set VREAD_DESC_CMD once and description mode comes alive)

- Local (Apple Silicon, no key): `VREAD_DESC_CMD="ollama run llava '$1'"` (or `moondream`, `qwen2.5-vl`)
- API: `VREAD_DESC_CMD="curl -s https://api.openai.com/v1/chat/completions -H 'Authorization: Bearer $OPENAI_KEY' -F 'image=@\"$1\"' ..."` — adapt to your provider
- ControlMCP already ships `read_screenshot_base64` — vread's `localhost-file` flow covers the same ground without it; use whichever is wired.

## Pitfalls

- **Never claim visual understanding from OCR + color averages alone.** Text ≠ layout ≠ aesthetics. When the question is fully visual, say so and use the description backend or multimodal-looker.
- Screenshots with small fonts: OCR degrades — tell the user to zoom/crop the region (`vread -r x,y,w,h`).
- **`e5rt` / Core ML error from `ocr-bin`**: the Vision model cache went stale after a macOS update. Fix = recompile: `swiftc -O ~/bin/ocr.swift -o ~/bin/ocr-bin`. Same for `vimg`: `swiftc -O ~/bin/vimg.swift -o ~/bin/vimg`. If BOTH fail, fall back to a one-off inline swift script using VNRecognizeTextRequest — it usually works when the stale binaries don't.
- Never burn tool calls building an ad-hoc OCR/color script at runtime — `vimg` already covers both. One call, done.