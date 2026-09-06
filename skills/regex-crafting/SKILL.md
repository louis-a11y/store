---
name: regex-crafting
description: Use when writing or debugging regular expressions — greedy/lazy, anchors, character classes, lookarounds, multiline/dotall traps, JS vs PCRE vs POSIX differences, and when regex is the wrong tool.
---

## Goal
Write correct regexes fast and debug them without guessing: build from anchors, avoid the classic traps, and know when to reach for a parser instead.

## Build order (never write the whole thing at once)

1. **Anchors first**: `^`/`$` or `\b` — define where the match lives.
2. **Literal spine**: match the fixed text around the variable part.
3. **The variable part LAST**: `[0-9]+`, `.+?` — smallest possible capture.
4. Test immediately with a one-liner, then extend.

## Quick reference

| Pattern | Meaning |
|---|---|
| `.*` (greedy) | As much as possible — matches to the LAST occurrence |
| `.*?` (lazy) | As little as possible — matches to the FIRST occurrence |
| `[a-z]{2,4}` | Quantified character class |
| `\d` `\w` `\s` `\b` | Digit, word char, whitespace, word boundary |
| `x(?=y)` / `x(?!y)` | Lookahead: match x only if followed/not followed by y |
| `(?<=y)x` / `(?<!y)x` | Lookbehind (supported in JS, Python, PCRE2 — NOT in old POSIX) |
| `^`/`$` with `m` flag | Line anchors (each line) |
| `.` with `s` flag | Dot matches newline too (dotall) |

## Testing fast (node one-liner)

```bash
node -e "const r=/^https:\/\/([^/]+)/; console.log('https://x.com/a'.match(r)?.[1])"
# loop over cases:
node -e "
const cases=['a@b.com','nope','a@b'];
const r=/^[\w.+-]+@[\w-]+\.[\w.]+$/;
for (const c of cases) console.log(c, r.test(c));
"
```

## Debugging a failing regex (in order)

1. Test the parts separately (anchors, then class, then quantifier).
2. Check greedy vs lazy — `.*` with two matches always grabs the last.
3. Check which flags are missing (`g` for multiple, `m` for multiline, `s` for dotall, `i` for case).
4. `$`/`^` with `m` vs without — classic "matches once but not per line" bug.
5. Backtracking explosion with nested quantifiers `(a+)+` — catastrophic on long strings.

## JS regex differences (critical for node/fountain)

- No free-spacing mode, no named captures in older engines — `(?<name>...)` works in modern V8.
- `\d` is ASCII-only (unlike Python which is Unicode by default).
- Lookbehind IS supported in modern V8/Node ≥ 8.3.
- `String.match` with `g` returns matches WITHOUT captures — use `matchAll` for capture groups.

## When regex is the WRONG tool

| Task | Use instead |
|---|---|
| Parsing JSON/HTML/XML | Real parser (`JSON.parse`, cheerio, DOMParser) |
| Nested structures (brackets, quotes) | Parser or recursion, never regex |
| Email validation for UX | Just check `@` and a dot — full RFC regexes are wrong in 80% of real addresses |
| URL validation | `new URL(str)` try/catch — robust and standard |
| Log extraction at scale | awk/cut for fixed columns; regex only for the free-form tail |

## Pitfalls

- `\b` inside `[`...`]` is a backspace — `[\b]` never matches a word boundary. Use `\b` OUTSIDE classes.
- `-` in classes: `[a-z-]` fine, but `[a-z-_]` places it where it can be misread — put `-` first or last ALWAYS.
- Escaping in shells: single-quote the whole regex in bash to stop `$`/`\d` interpolation; in double quotes, `$` dies.
- In node `-e`, escape backslashes (`\\d`) because the shell eats one layer.