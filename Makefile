ROMANISATIONS = Jyutping Yale

# Run fc-list pipeline to get clean HK font family names
FONTS := $(shell fc-list :lang=zh | grep "HK" | awk -F: '{print $$2}' | awk -F, '{print $$1}' \
		   | sed 's/^[[:space:]]*//;s/[[:space:]]*$$//' | sort -u | tr ' ' '_')
		   
# Cartesian product: each romanisation with each font
VARIANTS = $(foreach r,$(ROMANISATIONS),$(foreach f,$(FONTS),$(r)-$(f)))

all: $(VARIANTS)

checked: Yale-AR_PL_UKai_HK Yale-AR_PL_UMing_HK Jyutping-AR_PL_UKai_HK Jyutping-AR_PL_UMing_HK

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

Radicals-Left.tex Radicals-Right.tex: generate_radicals.py Radicals.csv
	python3 generate_radicals.py

pdf build:
	mkdir -p $@

clean:
	rm -rf build

clean-all: clean
	rm -rf pdf

debug:
	@echo "ROMANISATIONS = $(ROMANISATIONS)"
	@echo "FONTS         = $(FONTS)"
	@echo "VARIANTS      = $(VARIANTS)"

.PHONY: all clean clean-all debug $(VARIANTS)