LATEXMK ?= latexmk
LATEXFLAGS = -pdf -interaction=nonstopmode -halt-on-error -outdir=build

.PHONY: all slides pt2 pt3 reader template
all: slides pt2 pt3 reader template

slides:
	$(LATEXMK) $(LATEXFLAGS) CompMechSlidesPt1.tex
	cp build/CompMechSlidesPt1.pdf CompMechSlidesPt1.pdf

pt2:
	$(LATEXMK) $(LATEXFLAGS) CompMechSlidesPt2.tex
	cp build/CompMechSlidesPt2.pdf CompMechSlidesPt2.pdf

pt3:
	$(LATEXMK) $(LATEXFLAGS) CompMechSlidesPt3.tex
	cp build/CompMechSlidesPt3.pdf CompMechSlidesPt3.pdf

reader:
	$(LATEXMK) $(LATEXFLAGS) CompMechPt1-reader.tex
	cp build/CompMechPt1-reader.pdf CompMechPt1-reader.pdf

template:
	$(LATEXMK) $(LATEXFLAGS) template.tex
	cp build/template.pdf template.pdf
