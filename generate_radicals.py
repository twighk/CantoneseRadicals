#!/usr/bin/env python3
r"""Generate the `Radicals.tex` file from `Radicals.csv`.

This script does *not* create any surrounding document; the LaTeX driver
is expected to live in a separate (hand‑maintained) file that \input s
`Radicals.tex`.

It is intended to be invoked automatically by latexmk whenever the CSV
changes, so it simply overwrites `Radicals.tex` each time it runs.
"""
import csv

CSV_PATH = 'Radicals.csv'
RADICALS_LEFT_TEX = 'build/Radicals-left.tex'
RADICALS_RIGHT_TEX = 'build/Radicals-right.tex'


def write_radicals():
    """Read the CSV and emit a TeX file with the two macros."""
    out = []
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            count = row.get('STROKE COUNT', '').strip()
            rad = row.get('RADICAL', '').strip()
            var = row.get('VARIANT', '').strip()
            eng = row.get('ENGLISH', '').strip().replace(',', '\u200b,')
            jy = row.get('JYUTPING', '').strip()
            yale = row.get('Yale', '').strip()
            if count:
                if count.isdigit() and int(count) == 15:
                    out.append(r"\StrokeCount{}")
                out.append(f"\\StrokeCount{{{count}}}")
            if rad:
                out.append(
                    f"\\Character{{{rad}}}{{{var}}}{{{eng}}}{{{jy}}}{{{yale}}}"
                )

    out_rounded_to_8 = len(out) + 7
    half = out_rounded_to_8 // 2 + 1
    with open(RADICALS_LEFT_TEX, 'w', encoding='utf-8') as f:
        for line in out[:half]:
            f.write(line + "\n")

    with open(RADICALS_RIGHT_TEX, 'w', encoding='utf-8') as f:
        for line in out[half:]:
            f.write(line + "\n")


if __name__ == '__main__':
    write_radicals()
