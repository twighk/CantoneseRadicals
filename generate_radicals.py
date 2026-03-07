#!/usr/bin/env python3
"""Generate the `Radicals.tex` file from `Radicals.csv`.

This script does *not* create any surrounding document; the LaTeX driver
is expected to live in a separate (hand‑maintained) file that \input s
`Radicals.tex`.

It is intended to be invoked automatically by latexmk whenever the CSV
changes, so it simply overwrites `Radicals.tex` each time it runs.
"""
import csv

CSV_PATH = 'Radicals.csv'
RADICALS_TEX = 'Radicals.tex'


def write_radicals():
    """Read the CSV and emit a TeX file with the two macros."""
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile, \
         open(RADICALS_TEX, 'w', encoding='utf-8') as out:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            count = row.get('STROKE COUNT', '').strip()
            rad = row.get('RADICAL', '').strip()
            var = row.get('VARIANT', '').strip()
            eng = row.get('ENGLISH', '').strip()
            jy = row.get('JYUTPING', '').strip()
            yale = row.get('Yale', '').strip()
            if count:
                out.write(f"\\StrokeCount{{{count}}}\n")
            if rad:
                out.write(
                    f"\\Character{{{rad}}}{{{var}}}{{{eng}}}{{{jy}}}{{{yale}}}\n"
                )


if __name__ == '__main__':
    write_radicals()
