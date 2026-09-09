# Iliad — Computational Mechanics Materials

Teaching materials for the computational-mechanics view of sequence models.
The repository contains presentation decks, written exercises, and hands-on
Python notebooks.

## Slides

The compiled decks can be opened directly:

- [Part 1 — Computational mechanics](slides/CompMechSlidesPt1.pdf)
- [Part 2 — Predicting the future](slides/CompMechSlidesPt2.pdf)
- [Part 3 — Representing the past](slides/CompMechSlidesPt3.pdf)
- [Part 1 reader](slides/CompMechPt1-reader.pdf)

Editable LaTeX sources, figures, build instructions, and a reusable starter
template are in [`slides/`](slides/).

## Written exercises

- [Part 2 exercise sheet](written-exercises/CompMechExercisesPt2.pdf)
- [Part 2 solutions](written-exercises/CompMechSolutionsPt2.pdf)

The shared exercise content and separate student/solution wrappers are in
[`written-exercises/`](written-exercises/). To rebuild both PDFs with a LaTeX
installation and `latexmk`:

```bash
cd written-exercises
make
```

## Python exercises: HMM from scratch

The Python exercises are ARENA-style notebooks in two parts. Each part has an
**exercises** notebook (with `# YOUR CODE HERE` stubs, inline tests, and
collapsible solutions) and a fully worked **solutions** notebook.

| Notebook | Open in Colab |
| --- | --- |
| **Part 1 — Sequence probabilities & next-token distributions** (exercises) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/14xp/iliad-comp-mech-materials/blob/main/python-exercises/colab/part1_sequence_probabilities_exercises_colab.ipynb) |
| Part 1 (solutions) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/14xp/iliad-comp-mech-materials/blob/main/python-exercises/colab/part1_sequence_probabilities_solutions_colab.ipynb) |
| **Part 2 — Belief states** (exercises) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/14xp/iliad-comp-mech-materials/blob/main/python-exercises/colab/part2_belief_states_exercises_colab.ipynb) |
| Part 2 (solutions) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/14xp/iliad-comp-mech-materials/blob/main/python-exercises/colab/part2_belief_states_solutions_colab.ipynb) |

The Colab notebooks are self-contained: their setup cells write the helper
modules into the session, so there is nothing else to install or download.

### Running locally

The non-Colab notebooks under [`python-exercises/`](python-exercises/) run in a
Jupyter environment with **Python 3.12**:

```bash
pip install -r requirements.txt        # or: uv venv && uv pip install -r requirements.txt
cd python-exercises
jupyter lab
```

Work through `part1_sequence_probabilities_exercises.ipynb` and then
`part2_belief_states_exercises.ipynb`. Fill in each `# YOUR CODE HERE` cell and
run its `tests.test_*(HMM)` cell; it prints **All tests passed!** when correct.

### Rebuilding the notebooks

All eight notebooks (local and Colab) are generated from a single source of
truth: [`python-exercises/build_notebooks.py`](python-exercises/build_notebooks.py),
the prose in `prose.json`, and the Python helper modules. Regenerate them after
editing those sources with:

```bash
cd python-exercises
python build_notebooks.py
```
