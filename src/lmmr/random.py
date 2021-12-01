
# This file is a shallow wrapper around `np.random`. Enabling use of the
# new RNG with a familiar API.

import numpy as np

def global_rng():
    # TODO enable (re)setting the RNG.
    if not hasattr(global_rng, "_rng"):
        global_rng._rng = np.random.default_rng()

    return global_rng._rng

def uniform(*args, **kwargs):
    rng = global_rng()
    return rng.uniform(*args, **kwargs)


def normal(*args, **kwargs):
    rng = global_rng()
    return rng.normal(*args, **kwargs)


def multivariate_normal(*args, **kwargs):
    rng = global_rng()
    return rng.multivariate_normal(*args, **kwargs)


def choice(*args, **kwargs):
    rng = global_rng()
    return rng.choice(*args, **kwargs)

