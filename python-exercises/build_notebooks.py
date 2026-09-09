"""Generator for the ARENA-style HMM exercise/solutions notebooks.

Single source of truth: the per-method markdown comes from ``prose.json`` (authored
separately); the code stubs and worked solutions are derived directly from
``solutions.py`` via ``inspect`` so they can never drift from the reference. Emits
four notebooks (exercises + solutions, for Part 1 and Part 2) as raw .ipynb JSON.

Run with:  python build_notebooks.py
"""

import inspect
import json
import textwrap

import solutions

HERE = __import__("pathlib").Path(__file__).parent
PROSE = json.loads((HERE / "prose.json").read_text())

CLASS_DOCSTRING = '''"""HMM defined by an observation-indexed transition tensor and an initial vector.

    Shapes
    ------
    transition_tensor        : (n_obs, n_states, n_states)
    belief / state vectors   : (n_states,)
    next-token distributions : (n_obs,)
    """'''

SETUP = '''# Best-effort auto-reload of edited modules (silently skipped where IPython's
# autoreload extension is unavailable, e.g. some Colab Python 3.12 images).
try:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
except Exception:
    pass

import sys
import pathlib

# Make the exercise modules (processes / solutions / tests / plotting) importable
# regardless of the kernel's working directory (the exercises folder or the repo root).
_here = pathlib.Path.cwd()
for _cand in [_here, _here / "exercises"]:
    if (_cand / "tests.py").exists():
        sys.path.insert(0, str(_cand))
        break

import numpy as np
from collections.abc import Sequence

import processes
import solutions
import tests

# Shape aliases (documentation only -- pyright sees plain np.ndarray).
type TransitionTensor = np.ndarray  # (n_obs, n_states, n_states)
type StateVector = np.ndarray       # (n_states,) -- belief / propagated state vector
type TokenDist = np.ndarray         # (n_obs,)    -- distribution over next tokens'''


def method_source(name: str) -> str:
    """Dedented module-level source of a reference HMM method."""
    return textwrap.dedent(inspect.getsource(getattr(solutions.HMM, name)))


def make_stub(name: str) -> str:
    """Signature (possibly multi-line) + a YOUR CODE HERE body."""
    lines = method_source(name).splitlines()
    sig_end = next(i for i, ln in enumerate(lines) if ln.rstrip().endswith(":"))
    sig = "\n".join(lines[: sig_end + 1])
    return f"{sig}\n    # YOUR CODE HERE\n    raise NotImplementedError()\n\nHMM.{name} = {name}"


def make_solution(name: str) -> str:
    return f"{method_source(name).rstrip()}\n\nHMM.{name} = {name}"


def skeleton(given_methods: list[str]) -> str:
    """HMM class with __init__ and any pre-implemented (given) methods in the body."""
    parts = [f"class HMM:\n    {CLASS_DOCSTRING}\n", inspect.getsource(solutions.HMM.__init__).rstrip("\n")]
    for m in given_methods:
        parts.append("")
        parts.append(inspect.getsource(getattr(solutions.HMM, m)).rstrip("\n"))
    body = "\n".join(parts)
    if given_methods:
        body = (
            "# The non-belief-state methods from Part 1 are GIVEN here so this notebook is\n"
            "# standalone. You implement only the belief-state methods below.\n\n" + body
        )
    return body


# ---- notebook cell helpers -------------------------------------------------

def _src(text: str) -> list[str]:
    """nbformat source: list of lines, each (except the last) ending in newline."""
    lines = text.split("\n")
    return [ln + "\n" for ln in lines[:-1]] + [lines[-1]]


def md(text: str, cid: str) -> dict:
    return {"id": cid, "cell_type": "markdown", "metadata": {}, "source": _src(text)}


def code(text: str, cid: str) -> dict:
    return {"id": cid, "cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": _src(text)}


def solution_dropdown(name: str) -> str:
    return ("<details>\n<summary>Solution</summary>\n\n```python\n"
            + make_solution(name) + "\n```\n</details>")


EXERCISES_DIVIDER = (
    "---\n\n## Exercises\n\n"
    "The cells above are **setup**. First run the cell below to define the `HMM` class, "
    "then work through the exercises in order: for each, complete the `# YOUR CODE HERE` "
    "cell (it attaches the method to `HMM` via `HMM.<name> = <name>`), then run its "
    "`tests.test_<name>(HMM)` cell — it prints **All tests passed!** when your "
    "implementation is correct."
)


def build_notebook(part: dict, kind: str) -> dict:
    """kind in {'exercises', 'solutions'}."""
    cells = [
        md(PROSE[part["overview_key"]], "overview"),
        md("## Setup", "setup-h"),
        code(SETUP, "setup"),
        md(EXERCISES_DIVIDER, "exercises-h"),
        md("The `HMM` skeleton — each exercise adds a method to this class via "
           "`HMM.<name> = <name>`.", "skel-h"),
        code(skeleton(part["given"]), "skeleton"),
    ]
    for name in part["methods"]:
        key = f"m_{name}"
        cells.append(md(PROSE[key], f"{name}-md"))
        body = make_solution(name) if kind == "solutions" else make_stub(name)
        cells.append(code(body, f"{name}-code"))
        cells.append(code(f"tests.test_{name.lstrip('_')}(HMM)", f"{name}-test"))
        if kind == "exercises":
            cells.append(md(solution_dropdown(name), f"{name}-sol"))
    cells.append(md(part.get("demo_md", "## Demo"), "demo-h"))
    demo_cells = part["demo"] if isinstance(part["demo"], list) else [part["demo"]]
    code_i = 0
    for j, entry in enumerate(demo_cells):
        kind_, text = entry if isinstance(entry, tuple) else ("code", entry)
        if kind_ == "md":
            cells.append(md(text, f"demo-md-{j}"))
        else:
            cells.append(code(text, "demo" if code_i == 0 else f"demo-{code_i}"))
            code_i += 1

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


PART1 = {
    "stub": "part1_sequence_probabilities",
    "overview_key": "part1_overview",
    "given": [],
    "demo_md": "## Demo\n\nWith the methods implemented, we can explore a process. The cells below render "
               "the **next-token-distribution geometry** interactively (via the local "
               "`plotting.py`): every reachable sequence's next-token "
               "distribution, plotted on the symbol simplex and colored by its coordinates. "
               "Hover a point to see the sequence that induces it. We show two 3-symbol "
               "processes — **Mess3** (3 states; a fractal) and **arch** (4 states).",
    "methods": ["validate", "_propagate", "sequence_probability",
                "conditional_next_token_probabilities", "all_next_token_probabilities"],
    "demo": ['''from itertools import product

import plotting

hmm = HMM(processes.mess3(0.15, 0.2), processes.uniform_initial(3))
hmm.validate()  # a well-formed process passes silently

# A proper process: probabilities over all length-3 sequences sum to 1.
total = sum(hmm.sequence_probability(s) for s in product(range(3), repeat=3))
print("sum P(length-3 sequences) =", round(float(total), 6))

print("P(next | (0, 1))           =", np.round(hmm.conditional_next_token_probabilities((0, 1)), 4))
print("# reachable seqs <= depth 4:", len(hmm.all_next_token_probabilities(4)))

# Interactive next-token-distribution geometry (uses the local plotting.py).
# Each point is the next-token distribution after some sequence, plotted on the
# symbol simplex and colored by its coordinates; hover shows the inducing sequence.
depth = 7
ntps = hmm.all_next_token_probabilities(depth)
plotting.plot_next_token_distributions(
    np.array([np.real(v) for v in ntps.values()]),
    sequences=list(ntps.keys()),
    title=f"Mess3 next-token-distribution geometry (depth {depth})",
)''',
'''# The arch process: 4 hidden states, 3 symbols. Its next-token distributions still
# live on the 3-symbol simplex (a 2D triangle), but trace a different geometry.
arch_hmm = HMM(processes.arch(0.6), processes.uniform_initial(4))
arch_hmm.validate()

arch_ntps = arch_hmm.all_next_token_probabilities(depth)
plotting.plot_next_token_distributions(
    np.array([np.real(v) for v in arch_ntps.values()]),
    sequences=list(arch_ntps.keys()),
    title=f"Arch next-token-distribution geometry (depth {depth})",
)''',
        ("md",
         "### Bring your own process\n\n"
         "The processes above come from `processes.py`, but nothing is special about them — "
         "**any** non-negative transition tensor whose observation-summed matrix is "
         "row-stochastic defines a valid HMM. Here we define one **inline** (not in "
         "`processes.py`): the **Fern** process (3 states, 2 symbols). `validate()` confirms "
         "it is well-formed, then it runs through exactly the same machinery. With only 2 "
         "symbols, its next-token distributions live on a 1-simplex (a line segment)."),
        '''def fern(x: float) -> np.ndarray:
    """Fern process (custom): 3 hidden states, 2 symbols."""
    assert 0.0 <= x <= 1.0
    return np.array([
        [[0.3942, 0.00512, 0.0381], [0.0, 0.53, 0.0], [0.0, 0.326 * x, 0.554]],
        [[0.3358, 0.01088, 0.2159], [0.0, 0.0, 0.47], [0.12, 0.326 * (1 - x), 0.0]],
    ])

fern_hmm = HMM(fern(0.5), processes.uniform_initial(3))
fern_hmm.validate()  # a custom process still has to be a valid HMM

fern_depth = 12
fern_ntps = fern_hmm.all_next_token_probabilities(fern_depth)
plotting.plot_next_token_distributions(
    np.array([np.real(v) for v in fern_ntps.values()]),
    sequences=list(fern_ntps.keys()),
    title=f"Fern next-token-distribution geometry (depth {fern_depth})",
)'''],
}

PART2 = {
    "stub": "part2_belief_states",
    "overview_key": "part2_overview",
    "given": ["validate", "_propagate", "sequence_probability",
              "conditional_next_token_probabilities", "all_next_token_probabilities"],
    "methods": ["belief_state", "belief_update",
                "ntp_from_belief_state", "all_belief_states"],
    "demo_md": "## Demo\n\nWith the belief-state methods implemented, we can collect the reachable belief "
               "states and view their geometry interactively (via the local `plotting.py`). "
               "Belief states live on the **hidden-state** simplex: **Mess3** (3 states) gives a "
               "2D triangle whose reachable beliefs trace out a fractal, and **arch** (4 states) "
               "gives a 3D tetrahedron. Hover a point to see the inducing sequence.",
    "demo": ['''import plotting

hmm = HMM(processes.mess3(0.15, 0.2), processes.uniform_initial(3))

beliefs = hmm.all_belief_states(5)
print("# distinct reachable sequences <= depth 5:", len(beliefs))
print("belief after observing (0, 1, 2):", np.round(hmm.belief_state((0, 1, 2)), 4))
print("next-token dist from that belief :", np.round(hmm.ntp_from_belief_state(hmm.belief_state((0, 1, 2))), 4))

# Mess3 (3 hidden states): belief states live on the 2-simplex (a triangle) and
# trace out a fractal.
depth = 7
mess3_beliefs = hmm.all_belief_states(depth)
plotting.plot_belief_states(
    np.array([np.real(v) for v in mess3_beliefs.values()]),
    sequences=list(mess3_beliefs.keys()),
    title=f"Mess3 belief-state geometry (depth {depth})",
)''',
'''# The arch process: 4 hidden states, 3 symbols. Belief states lie on the 4-state
# simplex, so they are plotted in 3D (a tetrahedron).
import plotting

arch_hmm = HMM(processes.arch(0.6), processes.uniform_initial(4))
depth = 7
arch_beliefs = arch_hmm.all_belief_states(depth)
plotting.plot_belief_states(
    np.array([np.real(v) for v in arch_beliefs.values()]),
    sequences=list(arch_beliefs.keys()),
    title=f"Arch belief-state geometry (depth {depth})",
)''',
        ("md",
         "### Bring your own process\n\n"
         "The processes above come from `processes.py`, but nothing is special about them — "
         "**any** non-negative transition tensor whose observation-summed matrix is "
         "row-stochastic defines a valid HMM. Here we define one **inline** (not in "
         "`processes.py`): the **Fern** process (3 states, 2 symbols). `validate()` confirms "
         "it is well-formed, then it runs through exactly the same machinery — and its 3-state "
         "belief geometry traces out its own fractal in the 2-simplex."),
        '''def fern(x: float) -> np.ndarray:
    """Fern process (custom): 3 hidden states, 2 symbols."""
    assert 0.0 <= x <= 1.0
    return np.array([
        [[0.3942, 0.00512, 0.0381], [0.0, 0.53, 0.0], [0.0, 0.326 * x, 0.554]],
        [[0.3358, 0.01088, 0.2159], [0.0, 0.0, 0.47], [0.12, 0.326 * (1 - x), 0.0]],
    ])

fern_hmm = HMM(fern(0.5), processes.uniform_initial(3))
fern_hmm.validate()  # a custom process still has to be a valid HMM

fern_depth = 12
fern_beliefs = fern_hmm.all_belief_states(fern_depth)
plotting.plot_belief_states(
    np.array([np.real(v) for v in fern_beliefs.values()]),
    sequences=list(fern_beliefs.keys()),
    title=f"Fern belief-state geometry (depth {fern_depth})",
)'''],
}


# ---- Google Colab variants -------------------------------------------------

# Helper modules embedded (verbatim) into the self-contained Colab notebooks.
COLAB_MODULES = ["processes", "solutions", "tests", "plotting"]

# Set to "owner/repo/blob/branch/path-to-colab-dir" to emit working per-notebook
# "Open in Colab" badges. None -> instructions only (Colab can also open via Upload).
COLAB_BADGE_REPO = "iliad-team/iliad-intensive-C.3/blob/main/python-exercises/colab"

COLAB_SETUP_IMPORTS = '''# Best-effort auto-reload of the helper modules written above (silently skipped
# where IPython's autoreload extension is unavailable, e.g. some Colab 3.12 images).
try:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
except Exception:
    pass

import numpy as np
from collections.abc import Sequence

import processes
import solutions
import tests

# Shape aliases (documentation only).
type TransitionTensor = np.ndarray  # (n_obs, n_states, n_states)
type StateVector = np.ndarray       # (n_states,) -- belief / propagated state vector
type TokenDist = np.ndarray         # (n_obs,)    -- distribution over next tokens'''


def _colab_header(filename: str) -> str:
    lines = []
    if COLAB_BADGE_REPO:
        url = f"https://colab.research.google.com/github/{COLAB_BADGE_REPO}/{filename}"
        lines.append(f"[![Open In Colab](https://colab.research.google.com/assets/"
                     f"colab-badge.svg)]({url})\n")
    lines.append(
        "> **Running on Colab.** This notebook is self-contained: the **Setup** cells "
        "below write the helper modules (`processes`, `solutions`, `tests`, `plotting`) "
        "into the session, then import them — nothing else to download. Just run the "
        "cells top to bottom. (To open it: *File → Upload notebook*, or from Google "
        "Drive / a GitHub link.)")
    return "\n".join(lines)


def build_colab_notebook(part: dict, kind: str) -> dict:
    """Self-contained Colab version: %%writefile the helper modules, no path bootstrap."""
    nb = build_notebook(part, kind)
    cells = nb["cells"]

    # Replace the local setup region (`setup-h` + `setup`) with the Colab setup.
    setup_region = [
        md("## Setup\n\nThese cells write the helper modules into the Colab session and "
           "import them. Run them once, top to bottom.", "setup-h"),
    ]
    for name in COLAB_MODULES:
        source = (HERE / f"{name}.py").read_text().rstrip("\n")
        setup_region.append(code(f"%%writefile {name}.py\n{source}", f"writefile-{name}"))
    setup_region.append(code(COLAB_SETUP_IMPORTS, "setup"))

    setup_idx = next(i for i, c in enumerate(cells) if c["id"] == "setup-h")
    cells[setup_idx:setup_idx + 2] = setup_region

    # Prepend the Colab header (badge links to this notebook's own GitHub path).
    filename = f"{part['stub']}_{kind}_colab.ipynb"
    cells.insert(0, md(_colab_header(filename), "colab-header"))

    nb["cells"] = cells
    return nb


def _preserve_scratch(nb: dict, path) -> dict:
    """Re-append any user-added cells (ids not produced by the generator) found in
    an existing notebook on disk, so regenerating never drops hand-added cells."""
    if not path.exists():
        return nb
    existing = json.loads(path.read_text())
    base_ids = {c["id"] for c in nb["cells"]}
    scratch = [c for c in existing["cells"] if c["id"] not in base_ids]
    if scratch:
        nb = {**nb, "cells": nb["cells"] + scratch}
        print("  preserved scratch cells:", [c["id"] for c in scratch])
    return nb


def main():
    colab_dir = HERE / "colab"
    colab_dir.mkdir(exist_ok=True)
    for part in (PART1, PART2):
        for kind in ("exercises", "solutions"):
            path = HERE / f"{part['stub']}_{kind}.ipynb"
            nb = build_notebook(part, kind)
            if kind == "solutions":
                nb = _preserve_scratch(nb, path)
            path.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
            print("wrote", path.name, f"({len(nb['cells'])} cells)")

            colab_nb = build_colab_notebook(part, kind)
            colab_path = colab_dir / f"{part['stub']}_{kind}_colab.ipynb"
            colab_path.write_text(json.dumps(colab_nb, indent=1, ensure_ascii=False))
            print("wrote", f"colab/{colab_path.name}", f"({len(colab_nb['cells'])} cells)")


if __name__ == "__main__":
    main()
