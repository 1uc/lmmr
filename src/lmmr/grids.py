import numpy as np


def uniform_boundaries(x):
    assert len(x.shape) == 1

    dx = x[1] - x[0]

    x_bd = np.empty((x.size + 1,))
    x_bd[:-1] = x - 0.5 * dx
    x_bd[-1] = x[-1] + 0.5 * dx

    return x_bd
