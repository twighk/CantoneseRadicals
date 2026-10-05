# Cantonese Radicals

A reference poster of the 214 Kangxi radicals with Cantonese romanization, typeset in various Hong Kong Chinese fonts, plus experimental oracle bone and seal script fonts built from historical glyphs.

## Contents

- [Radical Poster Romanisations and Fonts](#radical-poster-romanisations-and-fonts)
  - [Jyutping](#jyutping)
    - [AR PL UKai HK](#ar-pl-ukai-hk)
    - [AR PL UMing HK](#ar-pl-uming-hk)
    - [Chiron GoRound TC](#chiron-goround-tc)
    - [Chiron Hei HK](#chiron-hei-hk)
    - [Chiron Sung HK](#chiron-sung-hk)
    - [EVOBC Oracle Bone](#evobc-oracle-bone)
    - [EVOBC Seal](#evobc-seal)
    - [Noto Sans CJK HK](#noto-sans-cjk-hk)
    - [Noto Serif CJK HK](#noto-serif-cjk-hk)
  - [Yale](#yale)
    - [AR PL UKai HK](#ar-pl-ukai-hk)
    - [AR PL UMing HK](#ar-pl-uming-hk)
    - [Chiron GoRound TC](#chiron-goround-tc)
    - [Chiron Hei HK](#chiron-hei-hk)
    - [Chiron Sung HK](#chiron-sung-hk)
    - [EVOBC Oracle Bone](#evobc-oracle-bone)
    - [EVOBC Seal](#evobc-seal)
    - [Noto Sans CJK HK](#noto-sans-cjk-hk)
    - [Noto Serif CJK HK](#noto-serif-cjk-hk)
- [Building](#building)
- [Requirements](#requirements)
- [Sources](#sources)

## Radical Poster Romanisations and Fonts

### Jyutping

#### AR PL UKai HK

[![AR PL UKai HK](clips/RadicalsPoster-Jyutping-AR_PL_UKai_HK.png)](pdf/RadicalsPoster-Jyutping-AR_PL_UKai_HK.pdf)

#### AR PL UMing HK

[![AR PL UMing HK](clips/RadicalsPoster-Jyutping-AR_PL_UMing_HK.png)](pdf/RadicalsPoster-Jyutping-AR_PL_UMing_HK.pdf)

#### Chiron GoRound TC

[![Chiron GoRound TC](clips/RadicalsPoster-Jyutping-Chiron_GoRound_TC.png)](pdf/RadicalsPoster-Jyutping-Chiron_GoRound_TC.pdf)

#### Chiron Hei HK

[![Chiron Hei HK](clips/RadicalsPoster-Jyutping-Chiron_Hei_HK.png)](pdf/RadicalsPoster-Jyutping-Chiron_Hei_HK.pdf)

#### Chiron Sung HK

[![Chiron Sung HK](clips/RadicalsPoster-Jyutping-Chiron_Sung_HK.png)](pdf/RadicalsPoster-Jyutping-Chiron_Sung_HK.pdf)

#### EVOBC Oracle Bone

[![EVOBC Oracle Bone](clips/RadicalsPoster-Jyutping-EVOBC_Oracle_Bone.png)](pdf/RadicalsPoster-Jyutping-EVOBC_Oracle_Bone.pdf)

#### EVOBC Seal

[![EVOBC Seal](clips/RadicalsPoster-Jyutping-EVOBC_Seal.png)](pdf/RadicalsPoster-Jyutping-EVOBC_Seal.pdf)

#### Noto Sans CJK HK

[![Noto Sans CJK HK](clips/RadicalsPoster-Jyutping-Noto_Sans_CJK_HK.png)](pdf/RadicalsPoster-Jyutping-Noto_Sans_CJK_HK.pdf)

#### Noto Serif CJK HK

[![Noto Serif CJK HK](clips/RadicalsPoster-Jyutping-Noto_Serif_CJK_HK.png)](pdf/RadicalsPoster-Jyutping-Noto_Serif_CJK_HK.pdf)

### Yale

#### AR PL UKai HK

[![AR PL UKai HK](clips/RadicalsPoster-Yale-AR_PL_UKai_HK.png)](pdf/RadicalsPoster-Yale-AR_PL_UKai_HK.pdf)

#### AR PL UMing HK

[![AR PL UMing HK](clips/RadicalsPoster-Yale-AR_PL_UMing_HK.png)](pdf/RadicalsPoster-Yale-AR_PL_UMing_HK.pdf)

#### Chiron GoRound TC

[![Chiron GoRound TC](clips/RadicalsPoster-Yale-Chiron_GoRound_TC.png)](pdf/RadicalsPoster-Yale-Chiron_GoRound_TC.pdf)

#### Chiron Hei HK

[![Chiron Hei HK](clips/RadicalsPoster-Yale-Chiron_Hei_HK.png)](pdf/RadicalsPoster-Yale-Chiron_Hei_HK.pdf)

#### Chiron Sung HK

[![Chiron Sung HK](clips/RadicalsPoster-Yale-Chiron_Sung_HK.png)](pdf/RadicalsPoster-Yale-Chiron_Sung_HK.pdf)

#### EVOBC Oracle Bone

[![EVOBC Oracle Bone](clips/RadicalsPoster-Yale-EVOBC_Oracle_Bone.png)](pdf/RadicalsPoster-Yale-EVOBC_Oracle_Bone.pdf)

#### EVOBC Seal

[![EVOBC Seal](clips/RadicalsPoster-Yale-EVOBC_Seal.png)](pdf/RadicalsPoster-Yale-EVOBC_Seal.pdf)

#### Noto Sans CJK HK

[![Noto Sans CJK HK](clips/RadicalsPoster-Yale-Noto_Sans_CJK_HK.png)](pdf/RadicalsPoster-Yale-Noto_Sans_CJK_HK.pdf)

#### Noto Serif CJK HK

[![Noto Serif CJK HK](clips/RadicalsPoster-Yale-Noto_Serif_CJK_HK.png)](pdf/RadicalsPoster-Yale-Noto_Serif_CJK_HK.pdf)

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
- potrace (for the historical-script fonts)

## Sources

- <https://repository.lib.cuhk.edu.hk/en/item/cuhk-2023821>
- <https://www.cantoneseclass101.com/chinese-radicals/>
- <https://en.wikipedia.org/wiki/Kangxi_radicals>
- <https://github.com/twighk/CantoneseRadicals>
- Oracle bone and seal script glyphs: EVOBC (Evolution of Oracle Bone Characters), Guan et al.,
  <https://arxiv.org/abs/2401.12467>, <https://github.com/RomanticGodVAN/character-Evolution-Dataset>;
  see [historical/README.md](historical/README.md) for how they were selected and their provenance