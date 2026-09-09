LATEXMK ?= latexmk
LATEXFLAGS = -pdf -interaction=nonstopmode -halt-on-error -outdir=build

.PHONY: all exercises solutions exercises-pt2 exercises-pt3 solutions-pt2 solutions-pt3

all: exercises solutions

exercises: exercises-pt2 exercises-pt3

solutions: solutions-pt2 solutions-pt3

exercises-pt2:
	$(LATEXMK) $(LATEXFLAGS) CompMechExercisesPt2.tex
	cp build/CompMechExercisesPt2.pdf CompMechExercisesPt2.pdf

solutions-pt2:
	$(LATEXMK) $(LATEXFLAGS) CompMechSolutionsPt2.tex
	cp build/CompMechSolutionsPt2.pdf CompMechSolutionsPt2.pdf

exercises-pt3:
	$(LATEXMK) $(LATEXFLAGS) CompMechExercisesPt3.tex
	cp build/CompMechExercisesPt3.pdf CompMechExercisesPt3.pdf

solutions-pt3:
	$(LATEXMK) $(LATEXFLAGS) CompMechSolutionsPt3.tex
	cp build/CompMechSolutionsPt3.pdf CompMechSolutionsPt3.pdf
