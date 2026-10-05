ROMANISATIONS = Jyutping Yale

# Run fc-list pipeline to get clean HK (and Chiron, which follows HK glyph standards) font family names
FONTS := $(shell fc-list :lang=zh | grep -E "HK|Chiron" | awk -F: '{print $$2}' | awk -F, '{print $$1}' \
		   | sed 's/^[[:space:]]*//;s/[[:space:]]*$$//' | sort -u | tr ' ' '_')
		   
# Cartesian product: each romanisation with each font
VARIANTS = $(foreach r,$(ROMANISATIONS),$(foreach f,$(FONTS),$(r)-$(f)))

PYTHON = .venv/bin/python3

all: $(VARIANTS) readme

checked: $(foreach r,$(ROMANISATIONS),$(foreach f,AR_PL_UKai_HK AR_PL_UMing_HK Chiron_Hei_HK Chiron_Sung_HK Chiron_GoRound_TC Noto_Sans_CJK_HK Noto_Serif_CJK_HK,$(r)-$(f))) readme

# Convenience targets: make Yale-AR_PL_UMing_HK → builds the PDF
$(VARIANTS):
	$(MAKE) pdf/RadicalsPoster-$@.pdf

pdf/RadicalsPoster-%.pdf: outer.tex Radicals-Left.tex Radicals-Right.tex | pdf build
	xelatex --halt-on-error \
	  -output-directory=build \
	  -jobname=RadicalsPoster-$* \
	  "\providecommand{\PrintMode}{$(word 1,$(subst -, ,$*))}\
	   \providecommand{\FontChoice}{$(subst _, ,$(word 2,$(subst -, ,$*)))}\
	   \input{outer.tex}"
	cp build/RadicalsPoster-$*.pdf pdf/

Radicals-Left.tex Radicals-Right.tex: generate_radicals.py Radicals.csv setup | build
	$(PYTHON) generate_radicals.py

README.md: setup $(wildcard pdf/*.pdf) generate_readme.py
	$(PYTHON) generate_readme.py

# Historical-script fonts built from glyphs selected out of EVOBC (see historical/README.md)
EVOBC_DIR = ../characters/static/evobc

historical-fonts: fonts/EVOBCOracleBone.otf fonts/EVOBCSeal.otf

fonts/EVOBCOracleBone.otf: historical/OBC/sources.tsv historical/build_font.py | .venv fonts
	$(PYTHON) historical/build_font.py OBC "EVOBC Oracle Bone" $@

fonts/EVOBCSeal.otf: historical/SS/sources.tsv historical/build_font.py | .venv fonts
	$(PYTHON) historical/build_font.py SS "EVOBC Seal" $@

# Re-pick the glyphs from a local EVOBC copy (only needed to change the selection)
historical-select: setup
	$(PYTHON) historical/select_glyphs.py OBC $(EVOBC_DIR)
	$(PYTHON) historical/select_glyphs.py SS $(EVOBC_DIR)

pdf build fonts:
	mkdir -p $@

clean:
	rm -rf build

clean-all: clean
	rm -rf clips
	rm -rf pdf
	rm -rf .venv

debug:
	@echo "ROMANISATIONS = $(ROMANISATIONS)"
	@echo "FONTS         = $(FONTS)"
	@echo "VARIANTS      = $(VARIANTS)"

.venv: Makefile
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

setup: .venv

readme: README.md

.PHONY: all clean clean-all debug setup $(VARIANTS) readme historical-fonts historical-select