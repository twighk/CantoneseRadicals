#!/usr/bin/env python3
"""
select_glyphs.py - Pick one representative historical glyph per poster character
- Reads EVOBC images (one folder per EVOBC ID, filenames <ID>_<Book|Web>_<STAGE>_...)
- For each radical/variant in Radicals.csv, takes every image of the requested stage
- Picks the medoid: the image with the smallest total distance to all the others
- Copies the chosen image into historical/<stage>/png/ and records its provenance

Usage: select_glyphs.py STAGE [EVOBC_DIR]   (STAGE is an EVOBC code, e.g. OBC or SS)
"""
import csv
import json
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

EVOBC_DEFAULT = Path("../characters/static/evobc")
KEYVALUE_NAME = "../../data/sources/evobc/KeyValue.json"  # relative to the image dir
COMPONENTS = Path("historical/components.tsv")
SIZE = 64        # normalised comparison size
BLUR = 2.0       # tolerance for small stroke offsets when comparing


def poster_characters():
    """Radicals and their listed variants, in poster order, without duplicates."""
    chars = []
    for row in list(csv.reader(open("Radicals.csv", encoding="utf-8"), delimiter=";"))[1:]:
        for ch in [row[1]] + row[2].split():
            if ch not in chars:
                chars.append(ch)
    return chars


def ink_mask(path):
    """Binarise to a boolean ink mask, inverting if the background is dark."""
    grey = np.asarray(Image.open(path).convert("L"), dtype=np.float32)
    lo, hi = np.percentile(grey, 2), np.percentile(grey, 98)
    if hi - lo < 32:
        return None
    mask = grey < (lo + hi) / 2
    border = np.concatenate([mask[0], mask[-1], mask[:, 0], mask[:, -1]])
    if border.mean() > 0.5:
        mask = ~mask
    if not 0.005 < mask.mean() < 0.6:
        return None
    return mask


def normalise(mask):
    """Crop to the ink, fit into a SIZE square keeping aspect ratio, blur."""
    rows, cols = np.where(mask.any(axis=1))[0], np.where(mask.any(axis=0))[0]
    crop = mask[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
    h, w = crop.shape
    scale = (SIZE - 8) / max(h, w)
    img = Image.fromarray((crop * 255).astype(np.uint8)).resize(
        (max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    canvas = Image.new("L", (SIZE, SIZE), 0)
    canvas.paste(img, ((SIZE - img.width) // 2, (SIZE - img.height) // 2))
    canvas = canvas.filter(ImageFilter.GaussianBlur(BLUR))
    return np.asarray(canvas, dtype=np.float32).ravel() / 255


def medoid(paths):
    """Return the path whose normalised image is closest to all the others."""
    vecs, kept = [], []
    for p in paths:
        mask = ink_mask(p)
        if mask is not None:
            vecs.append(normalise(mask))
            kept.append(p)
    if not kept:
        return None, 0
    v = np.stack(vecs)
    sq = (v * v).sum(axis=1)
    dist = np.sqrt(np.maximum(sq[:, None] + sq[None, :] - 2 * v @ v.T, 0))
    return kept[int(dist.sum(axis=1).argmin())], len(kept)


def borrowed_components(stage, evobc, png_dir, have):
    """
    Fill gaps from historical/components.tsv: crop a component out of a host
    character's glyph. The crop is x0,y0,x1,y1 as fractions of the host's ink box.
    """
    rows = []
    for comp in csv.DictReader(open(COMPONENTS, encoding="utf-8"), delimiter="\t"):
        if comp["stage"] != stage or comp["character"] in have:
            continue
        ch, host = comp["character"], evobc / comp["evobc_file"].split("_")[0] / comp["evobc_file"]
        img = Image.open(host).convert("L")
        mask = ink_mask(host)
        rows_, cols = np.where(mask.any(axis=1))[0], np.where(mask.any(axis=0))[0]
        x0, y0, x1, y1 = (float(v) for v in comp["crop"].split(","))
        w, h = cols[-1] - cols[0], rows_[-1] - rows_[0]
        box = (round(cols[0] + x0 * w), round(rows_[0] + y0 * h),
               round(cols[0] + x1 * w) + 1, round(rows_[0] + y1 * h) + 1)
        name = f"U+{ord(ch):04X}.png"
        crop = img.crop(box)
        canvas = Image.new("L", (crop.width + 20, crop.height + 20), 255)
        canvas.paste(crop, (10, 10))
        canvas.save(png_dir / name)
        rows.append([ch, f"U+{ord(ch):04X}", name, host.parent.name,
                     f"{host.name} (crop {comp['crop']} of {comp['host']})", 1])
    return rows


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    stage = sys.argv[1]
    evobc = Path(sys.argv[2]) if len(sys.argv) > 2 else EVOBC_DEFAULT
    keyvalue = json.loads((evobc / KEYVALUE_NAME).read_text(encoding="utf-8"))
    ids = {}
    for evobc_id, ch in keyvalue.items():
        ids.setdefault(ch, []).append(evobc_id)

    out = Path("historical") / stage
    png_dir = out / "png"
    if png_dir.exists():
        shutil.rmtree(png_dir)
    png_dir.mkdir(parents=True)

    rows = []
    for ch in poster_characters():
        paths = sorted(
            f for i in ids.get(ch, []) if (evobc / i).is_dir()
            for f in (evobc / i).iterdir() if f.name.split("_")[2:3] == [stage]
        )
        chosen, usable = medoid(paths)
        if chosen is None:
            continue
        name = f"U+{ord(ch):04X}{chosen.suffix.lower()}"
        shutil.copy(chosen, png_dir / name)
        rows.append([ch, f"U+{ord(ch):04X}", name, chosen.parent.name, chosen.name, usable])

    rows += borrowed_components(stage, evobc, png_dir, {r[0] for r in rows})

    with open(out / "sources.tsv", "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
        writer.writerow(["character", "codepoint", "file", "evobc_id", "evobc_file", "candidates"])
        writer.writerows(rows)
    print(f"{stage}: selected {len(rows)} of {len(poster_characters())} characters -> {out}")


if __name__ == "__main__":
    main()
