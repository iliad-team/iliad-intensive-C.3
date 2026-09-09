# HMM exercises — Google Colab versions

Self-contained Colab notebooks for the HMM-from-scratch exercises. Each notebook
writes its helper modules (`processes`, `solutions`, `tests`, `plotting`) into the
Colab session via `%%writefile` cells, so there is **nothing else to download** —
no repo, no `pip install`.

## Notebooks
- `part1_sequence_probabilities_exercises_colab.ipynb` — Part 1 (sequence
  probabilities / next-token distributions), with `# YOUR CODE HERE` stubs.
- `part1_sequence_probabilities_solutions_colab.ipynb` — Part 1, fully worked.
- `part2_belief_states_exercises_colab.ipynb` — Part 2 (belief states), stubs.
- `part2_belief_states_solutions_colab.ipynb` — Part 2, fully worked.

## How to use
1. Open the notebook in Colab — either **File → Upload notebook**, or open it from
   Google Drive / a GitHub link. (Colab runs Python 3.12, which these require.)
2. Run the **Setup** cells top to bottom. They write the helper modules into the
   session and import them.
3. Work through each exercise: fill in the `# YOUR CODE HERE` cell, run it (it
   monkeypatches the method onto `HMM`), then run the `tests.test_*(HMM)` cell —
   it prints `All tests passed!` when correct. Each exercise has a collapsible
   **Solution** dropdown.
4. The **Demo** cells at the end render interactive Plotly figures of the
   next-token / belief-state geometry.

## Regenerating
These are generated from the canonical sources by
[`../build_notebooks.py`](../build_notebooks.py) (which embeds the live
`processes.py` / `solutions.py` / `tests.py` / `plotting.py`). To rebuild after
editing the exercises or helper modules:

```bash
cd ..            # python-exercises
python build_notebooks.py
```

To emit an "Open in Colab" badge once the notebooks are hosted, set
`COLAB_BADGE_REPO = "owner/repo/blob/branch/python-exercises/colab"` near
the top of `build_notebooks.py` and regenerate.
