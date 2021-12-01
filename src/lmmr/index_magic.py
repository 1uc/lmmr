# SPDX-License-Identifier: MIT
# Copyright (c) 2021 ETH Zurich, Luc Grosheintz-Laval

import numpy as np


def percentile_indices(values, percentiles):
    """Compute the indices corresponding to certain percentiles.

    Example:
        x = np.random.random(1000)
        I = percentile_indices(x, [0.0, 0.5, 0.75, 0.9, 0.99, 1.0])
        print(x[I])

    Args:
        values: 1D array from which certain percentiles should be taken.
        percentiles: 1D array of percentiles.
    """

    n_values = values.size
    ranked_values = sorted(np.arange(n_values), key=lambda i: values[i])
    return [ranked_values[int(p * (n_values - 1))] for p in percentiles]


def uniform_bin_index(x, min_max_n=None, centers=None):
    if min_max_n is not None:
        xmin, xmax, n = min_max_n

    elif centers is not None:
        dx = centers[1] - centers[0]
        xmin = centers[0] - 0.5 * dx
        xmax = centers[-1] + 0.5 * dx
        n = centers.size

    dx = (xmax - xmin) / n
    i = np.array(np.floor((x - xmin) / dx), dtype=np.int64)

    return np.clip(i, 0, n - 1)
