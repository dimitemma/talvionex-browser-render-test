# Talvionex browser rendering test page

A static, self-contained page used to verify browser-assisted URL import in Talvionex.

- The initial HTML holds an empty `<div id="root"></div>` and an inline script; the visible text is rendered by JavaScript.
- No login, cookies, API keys, external services, tracking, analytics or personal information.
- `robots.txt` allows all crawlers. GitHub Pages serves a project's files under its path, so the host-level `https://dimitemma.github.io/robots.txt` (absent, 404) is what crawlers actually read; a missing robots.txt allows crawling.
