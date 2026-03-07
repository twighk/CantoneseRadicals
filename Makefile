ROMANISATIONS = Jyutping Yale

# Run fc-list pipeline to get clean HK font family names
FONTS := $(shell fc-list :lang=zh | grep "HK" | awk -F: '{print $$2}' | awk -F, '{print $$1}' \
		   | sed 's/^[[:space:]]*//;s/[[:space:]]*$$//' | sort -u | tr ' ' '_')
		   
# Cartesian product: each romanisation with each font
VARIANTS = $(foreach r,$(ROMANISATIONS),$(foreach f,$(FONTS),$(r)-$(f)))

all: $(VARIANTS)

# Bridge each variant name to its PDF
$(VARIANTS):
	$(MAKE) pdf/RadicalsPoster-$@.pdf

pdf/RadicalsPoster-%.pdf: outer.tex Radicals.tex
	latexmk -halt-on-error -jobname=RadicalsPoster-$* outer.tex \
	  -usepretex="\providecommand{\PrintMode}{$(word 1,$(subst -, ,$*))} \
				  \providecommand{\FontChoice}{$(subst _, ,$(word 2,$(subst -, ,$*)))} "
clean:
	rm -rf build

clean-all: clean
	rm -rf pdf

debug:
	@echo "ROMANISATIONS = $(ROMANISATIONS)"
	@echo "FONTS = $(FONTS)"
	@echo "VARIANTS = $(VARIANTS)"

.PHONY: all $(VARIANTS) clean clean-all