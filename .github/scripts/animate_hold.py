#!/usr/bin/env python3
"""Post-process the 3D-contrib SVG so the rise animation loops with a pause at the top.

For every <animate>/<animateTransform>: keep the original motion over the first
6s of an 8s cycle, then HOLD the final value for the remaining 2s, and loop
forever. Works whatever the number of `values` an animation has (bars use 2,
the fade-ins use 11). Idempotent: tags already carrying keyTimes are skipped.
"""
import re
import sys

RISE = 0.75  # fraction of the cycle spent moving (6s of 8s); the rest holds


def fmt(x):
    s = f"{x:.4f}".rstrip("0").rstrip(".")
    return s or "0"


def fix(match):
    tag = match.group(0)
    if "keyTimes=" in tag:  # already processed
        return tag
    vm = re.search(r'values="([^"]*)"', tag)
    if not vm:
        return tag
    segs = vm.group(1).split(";")
    n = len(segs)
    if n < 2:
        return tag

    # append the last value once more -> holds it until the end of the cycle
    new_values = ";".join(segs + [segs[-1]])
    # original values spread over 0..RISE, then a final stop at 1.0 (the hold)
    key_times = [fmt((i / (n - 1)) * RISE) for i in range(n)] + ["1"]
    new_key_times = ";".join(key_times)

    tag = re.sub(r'values="[^"]*"', lambda m: f'values="{new_values}"', tag, count=1)
    tag = re.sub(r'dur="[^"]*"', 'dur="8s"', tag, count=1)
    if "repeatCount=" in tag:
        tag = re.sub(r'repeatCount="[^"]*"', 'repeatCount="indefinite"', tag, count=1)
    else:
        tag = tag[:-1] + ' repeatCount="indefinite">'
    return tag[:-1] + f' keyTimes="{new_key_times}">'


def main(path):
    with open(path, encoding="utf-8") as fh:
        svg = fh.read()
    svg = re.sub(r"<animateTransform\b[^>]*>|<animate\b[^>]*>", fix, svg)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)


if __name__ == "__main__":
    main(sys.argv[1])
