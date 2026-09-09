"""Generate the Mess3 belief and next-token simplex figure for Part 3."""

from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def mess3_matrices() -> np.ndarray:
    alpha = 1 / 5
    b = 2 / 5
    x = 3 / 20
    y = 7 / 10
    return np.array(
        [
            [[alpha * y, b * x, b * x],
             [alpha * x, b * y, b * x],
             [alpha * x, b * x, b * y]],
            [[b * y, alpha * x, b * x],
             [b * x, alpha * y, b * x],
             [b * x, alpha * x, b * y]],
            [[b * y, b * x, alpha * x],
             [b * x, b * y, alpha * x],
             [b * x, b * x, alpha * y]],
        ]
    )


def belief(sequence: tuple[int, ...], matrices: np.ndarray) -> np.ndarray:
    value = np.full(3, 1 / 3)
    for symbol in sequence:
        value = np.einsum("i,ij->j", value, matrices[symbol])
    return value / value.sum()


def simplex_coordinates(points: np.ndarray) -> np.ndarray:
    vertices = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])
    return np.einsum("ni,ij->nj", points, vertices)


def draw_simplex(ax: plt.Axes, points: np.ndarray, labels: tuple[str, str, str],
                 title: str, final_symbols: np.ndarray) -> None:
    vertices = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])
    triangle = np.vstack([vertices, vertices[0]])
    ax.plot(triangle[:, 0], triangle[:, 1], color="#20262A", linewidth=0.8)

    coords = simplex_coordinates(points)
    colours = np.array(["#255C6A", "#D07A45", "#6D62A8"])
    for symbol in range(3):
        mask = final_symbols == symbol
        ax.scatter(
            coords[mask, 0], coords[mask, 1], s=2.6,
            color=colours[symbol], alpha=0.72, linewidths=0,
            label=f"final symbol {symbol}",
        )

    offsets = [(-0.035, -0.035), (0.015, -0.035), (-0.01, 0.025)]
    for vertex, label, offset in zip(vertices, labels, offsets):
        ax.text(vertex[0] + offset[0], vertex[1] + offset[1], label,
                fontsize=8.5, color="#20262A")
    ax.set_title(title, fontsize=10, color="#20262A", pad=5)
    ax.set_aspect("equal")
    ax.set_xlim(-0.08, 1.08)
    ax.set_ylim(-0.08, np.sqrt(3) / 2 + 0.08)
    ax.axis("off")


def main() -> None:
    matrices = mess3_matrices()
    sequences = list(product(range(3), repeat=7))
    beliefs = np.array([belief(sequence, matrices) for sequence in sequences])
    final_symbols = np.array([sequence[-1] for sequence in sequences])
    next_token_matrix = matrices.sum(axis=2).T
    next_token_vectors = np.einsum("ni,ia->na", beliefs, next_token_matrix)

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9,
        "axes.facecolor": "white",
        "figure.facecolor": "white",
    })
    figure, axes = plt.subplots(1, 2, figsize=(7.2, 3.25))
    draw_simplex(
        axes[0], beliefs, ("state 0", "state 1", "state 2"),
        r"Beliefs $\mathcal{B}_7$", final_symbols,
    )
    draw_simplex(
        axes[1], next_token_vectors, ("symbol 0", "symbol 1", "symbol 2"),
        "Next-token vectors", final_symbols,
    )
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="lower center", ncol=3,
                  frameon=False, fontsize=8, bbox_to_anchor=(0.5, -0.01))
    figure.subplots_adjust(left=0.025, right=0.975, top=0.91, bottom=0.14, wspace=0.14)

    output = Path(__file__).parent / "figures" / "mess3-belief-and-next-token-geometry.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
