LATEXMK ?= latexmk
LATEXFLAGS = -pdf -interaction=nonstopmode -halt-on-error -outdir=build
OUTPUT_DIR = ../output/pdf

.PHONY: all guide template clean

all: guide template

guide:
	mkdir -p build $(OUTPUT_DIR)
	$(LATEXMK) $(LATEXFLAGS) CompMechReadingGuidePt4.tex
	cp build/CompMechReadingGuidePt4.pdf $(OUTPUT_DIR)/CompMechReadingGuidePt4.pdf

template:
	mkdir -p build $(OUTPUT_DIR)
	$(LATEXMK) $(LATEXFLAGS) template.tex
	cp build/template.pdf $(OUTPUT_DIR)/IliadReadingGuideTemplate.pdf

clean:
	$(LATEXMK) -C -outdir=build CompMechReadingGuidePt4.tex template.tex
