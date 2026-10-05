# Historical-script fonts

Two experimental fonts of early scripts, covering every character EVOBC has for the stage
(not just the poster's radicals), so they can be used for other text too:

| Font | Stage | Glyphs | Poster characters |
|---|---|---|---|
| `fonts/EVOBCOracleBone.otf` — *EVOBC Oracle Bone* | 甲骨文 oracle bone (EVOBC `OBC`) | 1,762 | 172 / 276 |
| `fonts/EVOBCSeal.otf` — *EVOBC Seal* | 篆書 seal (EVOBC `SS`) | 9,082 | 235 / 276 |

Characters with no attested form in a stage (e.g. 丨 丶 丿 in oracle bone) have no glyph,
and the posters leave them as gaps rather than mixing in modern forms (`GAP_FONTS` in the
Makefile).

## How the glyphs are chosen

`select_glyphs.py` takes every EVOBC image of a character at the given stage, binarises
it, crops it to the ink, fits it into a square and blurs it slightly, then picks the
**medoid**: the real inscription with the smallest total distance to all the others.
That is the most typical attested form, not an average of them.

Gaps can be filled from `components.tsv`, which crops a component out of a host
character's glyph (e.g. seal 亠 is the top of seal 高). Borrowed glyphs are marked as crops
in `sources.tsv`.

`build_font.py` upscales each chosen image, traces it with potrace (into
`build/historical/<stage>/svg/`, not committed) and builds a
CFF OpenType font, each glyph centred and scaled to fill the em square.

```bash
make historical-fonts    # build the fonts from the committed glyphs
make historical-select   # re-pick glyphs from a local EVOBC copy (EVOBC_DIR=...)
```

Requires `potrace`.

## Source and provenance

Glyph images are from **EVOBC** (Evolution of Oracle Bone Characters), Guan et al.,
[arXiv:2401.12467](https://arxiv.org/abs/2401.12467), dataset at
<https://github.com/RomanticGodVAN/character-Evolution-Dataset>.

EVOBC has no formal licence file. The glyphs depict ancient public-domain forms and are
used here as isolated character images with the dataset cited; this is a deliberate
choice, not a licence grant. `<stage>/sources.tsv` records each glyph's EVOBC ID and
original filename so every glyph can be traced back to its source.
