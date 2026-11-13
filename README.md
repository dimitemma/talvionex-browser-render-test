# Talvionex browser rendering test page

A static, self-contained page used to verify browser-assisted URL import in Talvionex.

- The initial HTML holds an empty `<div id="root"></div>` and an inline script; the visible text is rendered by JavaScript.
- No login, cookies, API keys, external services, tracking, analytics or personal information.
- `robots.txt` allows all crawlers. GitHub Pages serves a project's files under its path, so the host-level `https://dimitemma.github.io/robots.txt` (absent, 404) is what crawlers actually read; a missing robots.txt allows crawling.

## Screenshot capture fixtures (`capture/`, Talvionex B3 M12 E1)

Deterministic pages for the Talvionex screenshot-capture rehearsal. Nothing here sets cookies, loads third-party resources, tracks visitors or contains personal data.

| Page | Purpose | Expected capture |
|---|---|---|
| `capture/basic.html` | A plain static page | `ok`, 1280 px wide, about 1,450 px tall; a blue block (`#1f6feb`) centred at (140, 220) |
| `capture/decode-heavy.html` | Five large, highly compressible PNG gradients (about 256 MiB decoded, about 300 KB transferred), one with a CSS filter; about 5,000 px tall | `ok` and cut at the requested maximum height, or a correctly mapped limit error (`timeout`, `render_failed`, `image_too_large`, `oversized_output`); the worker must stay healthy and not restart |
| `capture/ssrf.html` | Image requests to `http://172.17.0.1:8400/`, `https://10.0.0.1/` and, if given at run time as `#host=<IPv4>`, `https://<host>/` | Every request fails: boxes 1–3 green (`#00b000`), box 0 blue (`#0050ff`). Red means an image was received (an isolation failure) |

- The host address for `ssrf.html` is never stored in this repository; it is passed in the URL fragment, which browsers do not send to servers.
- `capture/generate.py` (standard library only) documents how the images were made. The committed files and `capture/SHA256SUMS` are the reference.
- Verify with `sha256sum -c capture/SHA256SUMS`.
