---
name: knowledge-base
description: Use when the knowledge base is involved — querying what we know about a topic, appending facts/decisions/learnings, running kb ingest at session start, promoting a topic to a skill. Also triggers on "KB", "what do we know about X", "do we know anything about X", "kb append", "kb search".
---

> # CUSTOMIZE-ME (edit from the file manager — Finder: ~/.config/opencode/skills/knowledge-base/SKILL.md)
>
> | Knob | Default | Change it here |
> |---|---|---|
> | KB root | `~/knowledge-base/` | `KB_ROOT=` (skill body below) |
> | Ingest at session start | on | set `INGEST_AT_START=false` |
> | Ingest lookback | all | `INGEST_HOURS=all` (all = entire DB history; set `24` to limit) |
> | Promote threshold | 2 sessions | `PROMOTE_AT=2` (topic seen in ≥2 distinct sessions → skill candidate) |
> | Dedupe | exact-match skip | make it fuzzy if wanted |
> | Terse entries | on | `VERBOSE=false` → entries stay one-line in KB |
> | Verbose log | `~/kb-verbose.log` | every `kb append` is ALSO mirrored in long form via `kb log` |
>
> The rest of this file is the learning loop. Edit behavior here, not in app code.

## Goal

The KB is **empty by default** and **learns over hours of use**. The AI's job every session:
READ what's known, USE it to ground answers, APPEND what's new, PROMOTE what's recurring.

## 1. READ — at session start

- Run `kb ingest INGEST_HOURS` (unless INGEST_AT_START=false) to see recent sessions. Default is `kb ingest all` — the whole session history, no time limit.
- Before answering anything project-specific, `kb search <topic-keyword>` (cheap) or read the topic dir.
- If a topic exists, ground the answer in it BEFORE improvising.
- Cost rule: one `kb search` ≈ one grep. Don't fear it; do fear full `kb show` on large topics (cat only the file you need via `kb cat <topic> facts|decisions|learnings`).

## 2. USE — grounding rules

- KB facts are **high-confidence hypotheses, not truth**. Live code/system ALWAYS wins on conflict — then fix the KB note (don't duplicate a wrong note).
- When a KB note conflicts with reality: `kb append <topic> decision "note X was wrong because Y (updated date)"` and rewrite — never stack contradictions.
- Mark uncertainty inline: `(unverified)` if you haven't re-checked.

## 3. APPEND — what counts as durable knowledge

Append ONLY what survives the session and helps a FUTURE session:

| Kind | When | Example |
|---|---|---|
| `fact` | A path, command, flag, version, environment truth | "OVMF.fd lives at /opt/homebrew/share/qemu/ on this machine" |
| `decision` | A choice made with rationale (esp. if user-driven) | "Use flat binary os.img for QEMU; ELF only for GRUB/Limine" |
| `learning` | Something discovered the hard way | "jsqr only decodes ImageData, not video element (fountain)" |

Command: `kb append <topic> <kind> <text>` — dedupes exact matches, creates the topic on first use.

**Terse + verbose pairing**: KB entries stay terse one-liners. After every `kb append`, also write the verbose/prose version (full context, why, what it affects) to the home-folder log with `kb log <verbose text>` → appends timestamped to `~/kb-verbose.log`. KB stays greppable; the verbose log keeps the story.

DO NOT append: transient state, logs, code, "we ran test X it passed" (that's a session fact, not durable).

## 4. PROMOTE — topic -> skill

- Count real-session queries per topic (informally: if the AI reaches for the same topic across ≥ PROMOTE_AT distinct sessions, it's recurring). Threshold default is 2 — one query is curiosity, two is recurring.
- `kb promote <topic>` drafts a candidate to `inbox/promotions/`.
- **NEVER auto-create a skill.** Propose to the user, one line: "topic X queried 2× → want it as a skill?" — approval required (user rule: irreversible/structure-changing things need asking).

## 5. PRUNE — hygiene

- Contradiction → fix in place, don't append a second version.
- Stale (technology changed) → delete note, note the replacement.
- Empty topics (index only, no facts/decisions/learnings after a few weeks) → consider removing; `kb list` shows line counts.
- Every few weeks a cleanup pass: `kb list` then `kb cat` each topic, merge/trim.

## Session-loop recap (the whole behavior)

1. Start: `kb ingest` → skim inbox.
2. During: before answering, `kb search`; after new durable facts, `kb append`.
3. On recurring topic: `kb promote` + ASK user.
4. Terse. Entries are one line each. Tables > prose in topic files.