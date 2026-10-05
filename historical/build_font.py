#!/usr/bin/env python3
"""
build_font.py - Trace the selected historical glyphs and build an OpenType font
- Upscales and binarises each PNG in historical/<stage>/png/
- Traces it to build/historical/<stage>/svg/ with potrace
- Fits each outline into the em square and maps it to the character's codepoint

Usage: build_font.py STAGE FAMILY_NAME OUTPUT.otf
"""
import csv
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import SVGPath

UPM = 1000
ASCENT, DESCENT = 880, -120     # usual CJK em box
MARGIN = 80                     # padding inside the em box
TRACE_SIZE = 600                # long side in pixels before tracing


def trace(png, svg):
    """Upscale, binarise (dark ink on light ground) and trace one glyph."""
    grey = Image.open(png).convert("L")
    scale = TRACE_SIZE / max(grey.size)
    grey = grey.resize((round(grey.width * scale), round(grey.height * scale)), Image.LANCZOS)
    arr = np.asarray(grey, dtype=np.float32)
    lo, hi = np.percentile(arr, 2), np.percentile(arr, 98)
    ink = arr < (lo + hi) / 2
    border = np.concatenate([ink[0], ink[-1], ink[:, 0], ink[:, -1]])
    if border.mean() > 0.5:
        ink = ~ink
    with tempfile.NamedTemporaryFile(suffix=".pbm") as pbm:
        Image.fromarray(~ink).convert("1").save(pbm.name)
        subprocess.run(["potrace", "-s", "--turdsize", "20", "--alphamax", "1.0",
                        "--opttolerance", "0.4", "-o", str(svg), pbm.name], check=True)


def charstring(svg, ascent=ASCENT, descent=DESCENT):
    """Fit the traced outline into the em box, centred, keeping aspect ratio."""
    path = SVGPath(str(svg))
    bounds = BoundsPen(None)
    path.draw(bounds)
    x0, y0, x1, y1 = bounds.bounds
    box = UPM - 2 * MARGIN
    scale = box / max(x1 - x0, y1 - y0)
    # SVGPath ignores potrace's flipping <g transform>, leaving potrace's native
    # y-up coordinates, which already match the font's; just centre in the em box
    dx = (UPM - (x1 - x0) * scale) / 2 - x0 * scale
    mid = (ascent + descent) / 2
    dy = mid - (y0 + y1) / 2 * scale
    pen = T2CharStringPen(UPM, None)
    path.draw(TransformPen(pen, (scale, 0, 0, scale, dx, dy)))
    return pen.getCharString()


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    stage, family, output = sys.argv[1:]
    src = Path("historical") / stage
    svg_dir = Path("build/historical") / stage / "svg"   # traced outlines, regenerated from the PNGs
    svg_dir.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(open(src / "sources.tsv", encoding="utf-8"), delimiter="\t"))
    glyphs, cmap = {".notdef": None}, {}
    for row in rows:
        svg = svg_dir / (Path(row["file"]).stem + ".svg")
        trace(src / "png" / row["file"], svg)
        name = "uni" + row["codepoint"][2:] if len(row["codepoint"]) == 6 else "u" + row["codepoint"][2:]
        glyphs[name] = charstring(svg)
        cmap[ord(row["character"])] = name

    notdef = T2CharStringPen(UPM, None)
    glyphs[".notdef"] = notdef.getCharString()

    order = list(glyphs)
    fb = FontBuilder(UPM, isTTF=False)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    ps_name = family.replace(" ", "") + "-Regular"
    fb.setupCFF(ps_name, {"FullName": family}, glyphs, {})
    fb.setupHorizontalMetrics({g: (UPM, 0) for g in order})
    fb.setupHorizontalHeader(ascent=ASCENT, descent=DESCENT)
    fb.setupNameTable({
        "familyName": family,
        "styleName": "Regular",
        "uniqueFontIdentifier": ps_name,
        "fullName": family,
        "psName": ps_name,
        "description": f"Historical glyphs ({stage}) selected from the EVOBC dataset",
    })
    fb.setupOS2(sTypoAscender=ASCENT, sTypoDescender=DESCENT, usWinAscent=ASCENT,
                usWinDescent=-DESCENT, ulCodePageRange1=(1 << 20))  # Chinese: Big5
    fb.setupPost()
    fb.save(output)
    print(f"{family}: {len(cmap)} glyphs -> {output}")


if __name__ == "__main__":
    main()
