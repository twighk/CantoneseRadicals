ROMANISATIONS = Jyutping Yale

all: $(ROMANISATIONS)

$(ROMANISATIONS): %: pdf/RadicalsPoster-%.pdf

pdf/RadicalsPoster-%.pdf: outer.tex Radicals.tex
	latexmk -jobname="RadicalsPoster-$*" outer.tex -usepretex="\providecommand{\PrintMode}{$*}" 

clean:
	rm -f $(ROMANISATIONS:%=build/RadicalsPoster-%.*)

clean-all: clean
	rm -rf pdf/*.pdf

.PHONY: all $(ROMANISATIONS) clean clean-all