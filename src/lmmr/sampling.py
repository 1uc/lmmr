# SPDX-License-Identifier: MIT
# Copyright (c) 2021 ETH Zurich, Luc Grosheintz-Laval

import numpy as np


def joint_choice(arrays, n, axis=0):
    rng = np.random.default_rng()

    N = arrays[0].shape[axis]
    I = rng.choice(N, size=(n,), replace=False)

    return tuple(np.swapaxes(np.swapaxes(a, 0, axis)[I, ...], 0, axis) for a in arrays)
