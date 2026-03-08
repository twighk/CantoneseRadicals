#!/usr/bin/env python3
"""
generate_readme.py - Generate README.md for CantoneseRadicals project
- Scans pdf/ directory for built PDFs
- Crops alternating strips from left/right boxes for each font
- Generates README with H2 romanisation, H3 font headings and TOC
"""
from pathlib import Path

import numpy as np
import fitz  # pymupdf

PDF_DIR = Path("pdf")
CLIP_DIR = Path("clips")
README_PATH = Path("README.md")

ROWS_PER_COLUMN = 15
STRIP_ROWS     = 2
ZOOM           = 2


def parse_pdfs():
    """Scan pdf/ dir, split to get (romanisation, font_name) pairs."""
    results = []
    for f in PDF_DIR.glob("*.pdf"):
        name = f.stem  # drop .pdf
        parts = name.split('-', 2)  # RadicalsPoster, Jyutping/Yale, font_key
        if len(parts) < 3:
            print(f"Skipping {f} — unexpected filename format")
            continue
        romanisation = parts[1].replace('_', ' ')
        font_name = parts[2].replace('_', ' ')
        results.append((romanisation, font_name, f))
    return sorted(results)


def get_content_bbox_from_pixels(pix):
    """Find tight bounding box by scanning for non-white pixels."""
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    mask = (arr < 250).any(axis=2)
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    if len(rows) == 0 or len(cols) == 0:
        return 0, 0, pix.width, pix.height
    return int(cols[0]), int(rows[0]), int(cols[-1]), int(rows[-1])


def generate_preview(pdf_path, clip_path, strip_index): # pylint: disable=too-many-locals
    """
    Render full page, detect tight content bbox from pixels,
    alternate between left and right half, crop STRIP_ROWS rows
    advancing by strip_index, save as PNG.
    """
    doc = fitz.open(pdf_path)
    page = doc[0]
    mat = fitz.Matrix(ZOOM, ZOOM)

    full_pix = page.get_pixmap(matrix=mat)
    x0, y0, x1, y1 = get_content_bbox_from_pixels(full_pix)

    arr = np.frombuffer(full_pix.samples, dtype=np.uint8).reshape(
        full_pix.height, full_pix.width, full_pix.n
    )

    content_height = y1 - y0
    row_height = content_height / ROWS_PER_COLUMN
    even_rows = ROWS_PER_COLUMN - (ROWS_PER_COLUMN % STRIP_ROWS)
    mid_x = (x0 + x1) // 2

    strips_per_side = even_rows // STRIP_ROWS
    pos = strip_index % (strips_per_side * 2)
    side = pos // strips_per_side
    cx0, cx1 = (x0, mid_x) if side == 0 else (mid_x, x1)

    row_start = (pos % strips_per_side) * STRIP_ROWS
    ry0 = int(y0 + row_start * row_height)
    ry1 = int(min(y0 + (row_start + STRIP_ROWS) * row_height, y1))
    strip = arr[ry0:ry1, cx0:cx1, :]

    h, w = strip.shape[:2]
    fitz.Pixmap(fitz.csRGB, w, h, strip.tobytes(), False).save(clip_path)
    doc.close()


def heading_anchor(text):
    """Convert heading text to lowercase, replace spaces with dashes, remove parentheses."""
    return text.lower().replace(" ", "-").replace("(", "").replace(")", "")


def main():
    """Main function to generate README.md."""
    print(f"{'='*41}\n ReadMe Generator for Cantonese Radicals\n{'='*41}\n")
    CLIP_DIR.mkdir(exist_ok=True)

    pdfs = parse_pdfs()
    if not pdfs:
        print("No PDFs found in pdf/ — run make first.")
        return

    print(f"Found {len(pdfs)} PDFs")

    # Generate previews
    for i, (romanisation, font_name, pdf_path) in enumerate(pdfs):
        clip_path = CLIP_DIR / f"{pdf_path.stem}.png"
        if not clip_path.exists():
            print(f"  Preview: {font_name} from {pdf_path.name}")
            generate_preview(pdf_path, clip_path, i)

    lines = []
    lines.append("""
# Cantonese Radicals

A reference poster of the 214 Kangxi radicals with Cantonese romanization, typeset in various Hong Kong Chinese fonts.

## Contents

- [Radical Poster Romanisations and Fonts](#radical-poster-romanisations-and-fonts)
"""[1:-1]
    )

    current = None
    for romanisation, font_name, _ in pdfs:
        if romanisation != current:
            lines.append(f"  - [{romanisation}](#{heading_anchor(romanisation)})")
            current = romanisation
        lines.append(f"    - [{font_name}](#{heading_anchor(font_name)})")
    lines.append("- [Building](#building)")
    lines.append("- [Requirements](#requirements)")
    lines.append("- [Sources](#sources)")
    lines.append("")

    # Sections
    lines.append("## Radical Poster Romanisations and Fonts\n")
    current = None
    for romanisation, font_name, pdf_path in pdfs:
        if romanisation != current:
            lines.append(f"### {romanisation}\n")
            current = romanisation
        lines.append(f"#### {font_name}\n")
        clip_path = CLIP_DIR / f"{pdf_path.stem}.png"
        if clip_path.exists() and pdf_path.exists():
            lines.append(f"[![{font_name}]({clip_path})]({pdf_path})\n")
        elif clip_path.exists():
            lines.append(f"![{font_name}]({clip_path})\n")
        elif pdf_path.exists():
            lines.append(f"[Download PDF]({pdf_path})\n")
        else:
            lines.append("*(not built)*\n")

    lines.append("""
## Building

```bash
# Install Python3 dependencies
make setup

# Show available fonts and variants
make debug

# Build a single variant, e.g.:
make Yale-AR_PL_UKai_HK

# Build all variants
make all

# Clean build artifacts (keep PDFs)
make clean

# Clean everything including PDFs
make clean-all
```

## Requirements

- XeLaTeX
- Python 3
- Hong Kong Chinese fonts

## Sources

- <https://repository.lib.cuhk.edu.hk/en/item/cuhk-2023821>
- <https://www.cantoneseclass101.com/chinese-radicals/>
- <https://en.wikipedia.org/wiki/Kangxi_radicals>
- <https://github.com/twighk/CantoneseRadicals>
"""[1:-1])

    README_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {README_PATH}")


if __name__ == "__main__":
    main()
