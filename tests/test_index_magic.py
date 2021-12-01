import lmmr
import numpy as np


def test_uniform_bin_indices():
    edges = np.array([-0.1, 0.0, 0.1, 0.2, 0.3])
    centers = 0.5 * (edges[:-1] + edges[1:])
    xmin, xmax = np.min(edges), np.max(edges)
    n = centers.size

    tests = [(-0.11, 0), (-0.1, 0), (-0.0001, 0), (0.0, 1), (0.3, 3), (0.333, 3)]
    for x, i in tests:
        i_centers = lmmr.index_magic.uniform_bin_index(x, centers=centers)
        assert i_centers == i, f"{x}, {i}"

        i_minmax = lmmr.index_magic.uniform_bin_index(x, min_max_n=(xmin, xmax, n))
        assert i_minmax == i, f"{x}, {i}"
