---
name: api-testing
description: Use when testing HTTP endpoints or APIs from the terminal — curl recipes, JSON with jq, status codes, headers, cookies, file uploads, quick smoke tests for local dev servers like fountain.
---

## Goal
Test HTTP APIs fast and readably from the shell: proper curl flags, JSON parsing with jq, headers/cookies, and smoke-testing a local server without a framework.

## curl quick reference

| Task | Command |
|---|---|
| GET with status + body | `curl -sS -w '\n%{http_code}\n' http://localhost:3000/api/x` |
| POST JSON | `curl -sS -X POST -H 'Content-Type: application/json' -d '{"msg":"hi"}' URL` |
| Headers only | `curl -sSI URL` (`-I` head) |
| Show headers + body | `curl -sSi URL` |
| Follow redirects | `curl -sSL URL` |
| Timeout (never hang) | `curl -sS --max-time 10 URL` |
| Cookies jar | `curl -sS -c /tmp/cj -b /tmp/cj URL` |
| Upload file | `curl -sS -F 'file=@/path/to.png' URL` |
| URL-encode data | `curl -sS --data-urlencode 'q=hello world' URL` |
| Quiet + error only | `curl -sS -f` (fail on 4xx/5xx, exit non-zero) |

## jq for parsed output

```bash
curl -sS URL | jq .
curl -sS URL | jq '.items[0].name'          # field
curl -sS URL | jq 'length'                  # array length
curl -sS URL | jq 'map(.id)'                # transform
curl -sS URL | jq -r '.token'               # raw string (no quotes) → shell var
curl -sS -x POST -d '{"q":"x"}' URL | jq '.results | length'
```

## Smoke-test pattern (works for fountain)

```bash
# 1. is the server up?
curl -sf --max-time 3 http://localhost:3000 >/dev/null && echo UP || echo DOWN

# 2. endpoint responds with expected shape?
curl -sS http://localhost:3000/api/status | jq -e '.ok == true' >/dev/null \
  && echo "status ok" || echo "status broken"

# 3. full request/response debug when something's odd
curl -sv http://localhost:3000/api/status 2>&1 | sed -n '1,40p'
```

## Polling / retry (WebSocket/async flows)

```bash
# poll until success or timeout
for i in {1..20}; do
  curl -sf --max-time 2 http://localhost:3000/api/job/123 | jq -e '.state=="done"' && break
  sleep 0.5
done
```

## WebSocket quick check

- `brew install websocat` then: `websocat ws://localhost:3000/ws` (interactive)
- Scripted: node one-liner with the `ws` package, or `curl --include --no-buffer -H "Connection: Upgrade" ...` for raw upgrade checks.

## Pitfalls

- `-s` hides errors — ALWAYS pair with `-S` (show errors) or `-f`.
- `-d '{...}'` with single quotes: escape inner quotes properly or use a file (`-d @payload.json`).
- JSON bodies: forget `-H 'Content-Type: application/json'` and the server may parse the body as form-encoded → weird 400s/empty fields.
- `jq -e` exits 1 on false/null — perfect for `&&/||` chains, but wrap in `>/dev/null` to avoid noisy output.
- localhost HTTPS with self-signed certs: add `-k` ONLY for local smoke tests.