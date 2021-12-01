# SPDX-License-Identifier: MIT
# Copyright (c) 2021 ETH Zurich, Luc Grosheintz-Laval

import numpy as np
import lmmr.random


def univariate_normal(mean, sigma, size):
    return lmmr.random.normal(mean, sigma, size=size)


def multivariate_normal(mean, cov, size):
    return lmmr.random.multivariate_normal(mean, cov, size=size)


def joint_choice(arrays, n, axis=0):
    N = arrays[0].shape[axis]
    I = lmmr.random.choice(N, size=(n,), replace=False)

    subsampled_arrays = tuple(
        np.swapaxes(np.swapaxes(a, 0, axis)[I, ...], 0, axis) for a in arrays
    )

    return subsampled_arrays, I
