"""Interactive simplex plotting for the HMM exercises.

Self-contained — only numpy + plotly are required; scikit-learn is
imported lazily and only used for the >4-dimensional PCA path (the example
processes here are 3-4 dimensional, so it is never needed).
"""

import numpy as np
import plotly.graph_objects as go


def regular_simplex_vertices(n: int) -> np.ndarray:
    """Vertices of a regular (n-1)-simplex, centered, as an (n, n-1) array.

    The n probability-simplex corners e_i live in the hyperplane sum=1; centering
    them and projecting onto an orthonormal basis of the ones-orthogonal-complement
    yields a regular simplex in R^(n-1) (equilateral triangle for n=3, regular
    tetrahedron for n=4). Orientation is arbitrary -- only used for visualization.
    """
    centered = np.eye(n) - 1.0 / n
    # Rows of `centered` span the (n-1)-dim subspace orthogonal to the all-ones
    # vector; Vt[:n-1] is an orthonormal basis of it.
    _, _, vt = np.linalg.svd(centered)
    return centered @ vt[: n - 1].T


def _coords_to_rgb(beliefs: np.ndarray) -> list:
    """Map each belief vector to an RGB color via its first up-to-3 coordinates.

    For a 3-state model this is the exact barycentric coloring (each simplex
    corner -> pure red/green/blue); for more states only the first 3 coordinates
    drive the color.
    """
    rgb = np.zeros((len(beliefs), 3))
    k = min(3, beliefs.shape[1])
    rgb[:, :k] = np.clip(beliefs[:, :k], 0.0, 1.0)
    return ["rgb(%d,%d,%d)" % tuple((c * 255).astype(int)) for c in rgb]


def plot_belief_states(beliefs, sequences=None, path=None, title=None,
                       color_by_coords=True):
    """Plot HMM belief states on the hidden-state simplex (see plot_simplex_points)."""
    n = np.asarray(beliefs).shape[1]
    if title is None:
        title = f"Belief states ({n} hidden states)"
    return plot_simplex_points(beliefs, sequences, path, title, color_by_coords)


def plot_next_token_distributions(ntps, sequences=None, path=None,
                                  title=None, color_by_coords=True):
    """Plot next-token distributions on the symbol simplex (see plot_simplex_points)."""
    n = np.asarray(ntps).shape[1]
    if title is None:
        title = f"Next-token distributions ({n} symbols)"
    return plot_simplex_points(ntps, sequences, path, title, color_by_coords)


def plot_simplex_points(points, sequences=None, path=None, title=None,
                        color_by_coords=True):
    """Build an interactive Plotly scatter of probability vectors on a simplex.

    points: (N, d) array of probability vectors (complex inputs, e.g. GHMM
        beliefs/NTPs, are cast to their real part).
    sequences: optional length-N list of the observation sequences that induced
        each point; shown on hover. If None, hover shows the point index.
    path: if given, also write the figure to this HTML file. The Plotly figure is
        always returned (renders inline in a notebook).
    color_by_coords: if True, color each point by its coordinates (RGB from the
        first up-to-3 components); for d == 3 this is the exact barycentric coloring.

    The points are projected onto the probability simplex, then:
      - d == 2 -> 1D strip (x-axis)
      - d == 3 -> 2D triangle
      - d == 4 -> 3D tetrahedron
      - d  > 4 -> PCA to the top 3 components, 3D scatter
    """
    beliefs = np.real(np.asarray(points, dtype=complex))
    n_points, n = beliefs.shape
    if n < 2:
        raise ValueError(f"need at least 2 simplex dimensions to plot, got {n}.")
    if title is None:
        title = f"Simplex points ({n}-simplex)"

    if sequences is not None:
        if len(sequences) != n_points:
            raise ValueError(
                f"sequences has length {len(sequences)} but there are {n_points} points."
            )
        hover = [f"input sequence: {tuple(s)}" if len(tuple(s)) else "input sequence: () [start]"
                 for s in sequences]
    else:
        hover = [f"index {i}" for i in range(n_points)]

    coords = beliefs @ regular_simplex_vertices(n)

    marker = dict(size=5, opacity=0.7)
    if color_by_coords:
        marker["color"] = _coords_to_rgb(beliefs)
    hovertemplate = "%{text}<extra></extra>"

    if n == 2:
        fig = go.Figure(
            go.Scatter(
                x=coords[:, 0], y=np.zeros(n_points), mode="markers",
                marker=marker, text=hover, hovertemplate=hovertemplate,
            )
        )
        fig.update_yaxes(visible=False)

    elif n == 3:
        verts = regular_simplex_vertices(3)
        loop = np.vstack([verts, verts[0]])  # close the triangle
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=loop[:, 0], y=loop[:, 1], mode="lines",
            line=dict(color="black"), hoverinfo="skip", showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=coords[:, 0], y=coords[:, 1], mode="markers",
            marker=marker, text=hover, hovertemplate=hovertemplate, showlegend=False,
        ))
        fig.update_yaxes(scaleanchor="x", scaleratio=1, autorange="reversed")

    elif n == 4:
        verts = regular_simplex_vertices(4)
        edges = [(i, j) for i in range(4) for j in range(i + 1, 4)]
        ex, ey, ez = [], [], []
        for i, j in edges:
            ex += [verts[i, 0], verts[j, 0], None]
            ey += [verts[i, 1], verts[j, 1], None]
            ez += [verts[i, 2], verts[j, 2], None]
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=ex, y=ey, z=ez, mode="lines",
            line=dict(color="black"), hoverinfo="skip", showlegend=False,
        ))
        fig.add_trace(go.Scatter3d(
            x=coords[:, 0], y=coords[:, 1], z=coords[:, 2], mode="markers",
            marker=marker, text=hover, hovertemplate=hovertemplate, showlegend=False,
        ))
        fig.update_scenes(yaxis_autorange="reversed")

    else:  # n > 4: PCA to 3D
        from sklearn.decomposition import PCA

        coords = PCA(n_components=3).fit_transform(coords)
        fig = go.Figure(go.Scatter3d(
            x=coords[:, 0], y=coords[:, 1], z=coords[:, 2], mode="markers",
            marker=marker, text=hover, hovertemplate=hovertemplate,
        ))
        fig.update_scenes(
            xaxis_title="PC1", yaxis_title="PC2", zaxis_title="PC3"
        )

    fig.update_layout(title=title)
    if path is not None:
        fig.write_html(path)
    return fig
