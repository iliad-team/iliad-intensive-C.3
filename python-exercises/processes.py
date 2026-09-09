"""Hidden-Markov processes used as fixtures/demos in the HMM exercises.

Each process is given as an observation-indexed transition tensor of shape
(n_obs, n_states, n_states): ``tensor[x, i, j]`` is the probability of emitting
symbol ``x`` and moving from hidden state ``i`` to hidden state ``j``. Summing
over the symbol axis gives a row-stochastic state-transition matrix.
"""

import numpy as np


def arch(a: float) -> np.ndarray:
    """Creates a transition matrix for the Arch Process."""
    assert 0 <= a <= 1, f"a must be in [0, 1], got {a}"
    b = (1 - a) / 3
    return np.array(
        [
            [
                [0.8 * a, 0.0, 0.0, 0.0],
                [0.0, 0.2 * a, 0.0, 0.0],
                [0.0, 0.0, 0.4 * a, 0.0],
                [0.0, 0.0, 0.0, 0.6 * a],
            ],
            [
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.4 * a, 0.0, 0.4 * b],
                [0.0, 0.0, 0.3 * a, 0.0],
                [0.0, 0.0, 0.0, 0.16 * a],
            ],
            [
                [0.2 * a, b, b, b],
                [b, 0.4 * a, b, 0.6 * b],
                [b, b, 0.3 * a, b],
                [b, b, b, 0.24 * a],
            ],
        ]
    )

def z1r(p: float = 0.5) -> np.ndarray:
    """Zero-One-Random (Z1R) process: 3 hidden states, 2 symbols.

    Emits 0 then 1 deterministically, then a random bit with P(1) = ``p``.
    Stationary distribution is uniform, [1/3, 1/3, 1/3].
    """
    q = 1 - p
    return np.array(
        [
            [[0, 1, 0], [0, 0, 0], [q, 0, 0]],
            [[0, 0, 0], [0, 0, 1], [p, 0, 0]],
        ],
        dtype=float,
    )


def mess3(x: float = 0.15, a: float = 0.2) -> np.ndarray:
    """Mess3 process: 3 hidden states, 3 symbols.

    A symmetric process whose belief states trace out a fractal in the
    2-simplex. Stationary distribution is uniform, [1/3, 1/3, 1/3].
    """
    b = (1 - a) / 2
    y = 1 - 2 * x
    ay, bx, by, ax = a * y, b * x, b * y, a * x
    return np.array(
        [
            [[ay, bx, bx], [ax, by, bx], [ax, bx, by]],
            [[by, ax, bx], [bx, ay, bx], [bx, ax, by]],
            [[by, bx, ax], [bx, by, ax], [bx, bx, ay]],
        ],
        dtype=float,
    )


def uniform_initial(n_states: int) -> np.ndarray:
    """Uniform initial state distribution over ``n_states`` hidden states."""
    return np.ones(n_states) / n_states
