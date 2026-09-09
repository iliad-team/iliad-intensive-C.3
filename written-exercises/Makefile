LATEXMK ?= latexmk
LATEXFLAGS = -pdf -interaction=nonstopmode -halt-on-error -outdir=build

.PHONY: all exercises solutions

all: exercises solutions

exercises:
	$(LATEXMK) $(LATEXFLAGS) CompMechExercisesPt2.tex
	cp build/CompMechExercisesPt2.pdf CompMechExercisesPt2.pdf

solutions:
	$(LATEXMK) $(LATEXFLAGS) CompMechSolutionsPt2.tex
	cp build/CompMechSolutionsPt2.pdf CompMechSolutionsPt2.pdf
