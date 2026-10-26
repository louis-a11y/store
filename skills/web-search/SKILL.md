name: web-search
description: Multi-browser search skill that cascades across available APIs, CLI tools, and installed desktop browsers.
license: MIT
compatibility: opencode
metadata:
opencode/slash: "true"
opencode/autoinvoke: "true"

Search Execution Cascade

When searching the web or fetching page context, execute the following cascade in order until one succeeds:

Level 1: Native MCP API (Fastest & Primary)

If the brave-search MCP server is active and BRAVE_API_KEY is configured:

⚬ Query via Model Context Protocol brave-search tool calls.

Level 2: Command-Line Web Scrapers (No Browser Required)

If MCP is unavailable, attempt CLI execution using lightweight system binaries (curl / python3):

[bash]
# Try fetching formatted search results via Brave Search endpoint
curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
  "https://search.brave.com/search?q=YOUR_QUERY_HERE" | grep -oP '(?<=<a class="result-header" href=")[^"]*' || \

# Fallback: DuckDuckGo HTML endpoint via curl
curl -sL "https://html.duckduckgo.com/html/?q=YOUR_QUERY_HERE" | grep -oP '(?<=<a class="result__url" href=")[^"]*'


Level 3: Multi-Browser & Text-Mode Cascade

If raw curl fails to parse JavaScript-rendered pages, detect and run whichever installed browser binary exists on the system:

[bash]
# 1. Try Lynx (if installed)
command -v lynx >/dev/null && lynx -dump "https://search.brave.com/search?q=YOUR_QUERY_HERE" || \

# 2. Try w3m (if installed)
command -v w3m >/dev/null && w3m -dump "https://search.brave.com/search?q=YOUR_QUERY_HERE" || \

# 3. Try Headless Desktop Browsers (Brave -> Chrome -> Chromium -> Firefox)
if command -v brave >/dev/null; then
  brave --headless --dump-dom "https://search.brave.com/search?q=YOUR_QUERY_HERE"
elif command -v google-chrome >/dev/null; then
  google-chrome --headless --dump-dom "https://search.brave.com/search?q=YOUR_QUERY_HERE"
elif command -v chromium >/dev/null; then
  chromium --headless --dump-dom "https://search.brave.com/search?q=YOUR_QUERY_HERE"
elif command -v firefox >/dev/null; then
  firefox --headless --screenshot "https://search.brave.com/search?q=YOUR_QUERY_HERE"
fi


Rules for Agents

1. Never fail a search simply because one specific browser binary is missing from PATH.

2. Use the command -v <tool> check to silently fall through to the next available tool.

3. Once URLs are retrieved, fetch specific page contents using curl -sL <url>.

4. If some needed API keys aren't configured stop, tell the user, and tell them how to configure it