#!/usr/bin/env python3
"""Make a tiny, repeatable night sky from a word or phrase. No dependencies."""

import argparse
import hashlib
import math
import random
from pathlib import Path


def sky(seed: str, width: int = 960, height: int = 360) -> str:
    if not (160 <= width <= 4096 and 120 <= height <= 4096):
        raise ValueError("width and height must be between 160/120 and 4096 pixels")
    rng = random.Random(int.from_bytes(hashlib.sha256(seed.encode()).digest(), "big"))
    stars = []
    points = []
    for _ in range(85):
        x = rng.uniform(24, width - 24)
        y = rng.uniform(20, height - 20)
        radius = rng.choice((0.8, 1.1, 1.4, 1.9, 2.5))
        alpha = rng.uniform(0.3, 0.85)
        stars.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="#e4f5ed" opacity="{alpha:.2f}"/>')
        if radius >= 2.5:
            points.append((x, y))
    # Connect a few bright stars in a quiet, angular constellation.
    points = sorted(points[:6], key=lambda p: p[0])
    lines = [
        f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="#9cd7d1" stroke-width="1.2" opacity="0.32"/>'
        for (x1, y1), (x2, y2) in zip(points, points[1:])
        if math.dist((x1, y1), (x2, y2)) < width * 0.33
    ]
    glow_x = rng.uniform(width * 0.28, width * 0.72)
    return "\n".join([
        '<svg xmlns="http://www.w3.org/2000/svg"',
        f'     viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <defs>',
        '    <linearGradient id="night" x2="1" y2="1"><stop stop-color="#0b1531"/><stop offset="1" stop-color="#35446d"/></linearGradient>',
        '    <radialGradient id="glow"><stop stop-color="#79d6c6" stop-opacity="0.22"/><stop offset="1" stop-color="#79d6c6" stop-opacity="0"/></radialGradient>',
        '  </defs>',
        f'  <rect width="{width}" height="{height}" fill="url(#night)"/>',
        f'  <ellipse cx="{glow_x:.1f}" cy="{height * .76:.1f}" rx="{width * .52:.1f}" ry="{height * .52:.1f}" fill="url(#glow)"/>',
        *('  ' + line for line in lines),
        *('  ' + star for star in stars),
        '</svg>',
        '',
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("seed", help="A word or phrase; the same seed makes the same sky")
    parser.add_argument("--width", type=int, default=960)
    parser.add_argument("--height", type=int, default=360)
    parser.add_argument("--out", type=Path, required=True, help="Where to write the SVG")
    args = parser.parse_args()
    args.out.write_text(sky(args.seed, args.width, args.height), encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
