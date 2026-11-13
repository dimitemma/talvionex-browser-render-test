"""Generate the decode-heavy fixture images (standard library only, deterministic).

    python3 capture/generate.py          # writes capture/img/*.png
    sha256sum -c capture/SHA256SUMS      # the committed bytes are the reference

Each image is a smooth gradient: large when decoded (4096 x 4096 RGB is 48 MiB, about 64 MiB once
Chromium holds it as RGBA) but small on the wire, because the PNG "Up" filter turns every row into
almost nothing. The whole set is bounded: five images, about 256 MiB decoded in total, a few
hundred KB transferred, which is within the capture limits (80 requests, 2 MB per response,
12 MB per page) and well under the worker's 1 GiB memory limit. It is a resource-pressure fixture,
not a denial-of-service fixture: nothing on the page loops, grows or loads more than these files.

zlib output can differ between zlib versions; the committed files and capture/SHA256SUMS are the
reference, and this script documents how they were made.
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

OUT = Path(__file__).resolve().parent / "img"


def _chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def png(width: int, height: int, pixel) -> bytes:
    """An 8-bit RGB PNG. `pixel(x, y)` gives (r, g, b). Rows use filter 2 (Up) after the first."""
    raw = bytearray()
    previous = None
    for y in range(height):
        row = bytes(c for x in range(width) for c in pixel(x, y)) if _row_varies(pixel, y) or previous is None else previous
        if previous is None:
            raw += b"\x00" + row
        else:
            raw += b"\x02" + bytes((a - b) & 0xFF for a, b in zip(row, previous))
        previous = row
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", header) + _chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + _chunk(b"IEND", b"")


def _row_varies(pixel, y: int) -> bool:
    return getattr(pixel, "vertical", False)


class Horizontal:
    """Colour depends on x only: every row is identical."""

    vertical = False

    def __init__(self, width: int, start: tuple[int, int, int], end: tuple[int, int, int]):
        self.cache = [tuple(round(s + (e - s) * x / (width - 1)) for s, e in zip(start, end)) for x in range(width)]

    def __call__(self, x: int, y: int):
        return self.cache[x]


class Vertical:
    """Colour depends on y only: each row is one colour."""

    vertical = True

    def __init__(self, height: int, start: tuple[int, int, int], end: tuple[int, int, int]):
        self.cache = [tuple(round(s + (e - s) * y / (height - 1)) for s, e in zip(start, end)) for y in range(height)]

    def __call__(self, x: int, y: int):
        return self.cache[y]


IMAGES = {
    "heavy-1.png": (4096, 4096, lambda w, h: Horizontal(w, (20, 60, 160), (240, 200, 40))),
    "heavy-2.png": (4096, 4096, lambda w, h: Vertical(h, (160, 20, 60), (40, 220, 200))),
    "heavy-3.png": (4096, 4096, lambda w, h: Horizontal(w, (10, 120, 40), (250, 250, 250))),
    "heavy-4.png": (4096, 4096, lambda w, h: Vertical(h, (250, 140, 0), (30, 30, 90))),
    "heavy-5.png": (8192, 2048, lambda w, h: Horizontal(w, (0, 0, 0), (200, 80, 240))),
}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, (width, height, make) in IMAGES.items():
        (OUT / name).write_bytes(png(width, height, make(width, height)))
        print(name, width, height, (OUT / name).stat().st_size)


if __name__ == "__main__":
    main()
