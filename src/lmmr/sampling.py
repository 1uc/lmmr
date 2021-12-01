# SPDX-License-Identifier: MIT
# Copyright (c) 2021 ETH Zurich, Luc Grosheintz-Laval

import numpy as np
import lmmr.random


def rejection_sampling(n_samples, rng, reject_if):
    """Redraw samples that satisfy `reject_if`.

    The `rng` is expected to either return one array with different samples on
    axis 0, or a tuple of array, which each the samples on their axis 0.

    The exclusion criterium is expected to be of the form
        mask = reject_if(samples)

    where `mask` is a boolean mask.
    """

    def keep(samples, valid):
        if isinstance(samples, tuple):
            return tuple(s[valid] for s in samples)
        else:
            return samples[valid]

    def redraw(n_needed, n_redraw):
        extra_samples = rng(n_redraw)
        valid = np.logical_not(reject_if(extra_samples))

        if np.count_nonzero(valid) < n_needed:
            return redraw(n_needed, 2 * n_redraw)

        else:
            return keep(extra_samples, valid)

    samples = rng(n_samples)
    invalid = reject_if(samples)

    n_invalid = np.count_nonzero(invalid)
    extra_samples = redraw(n_invalid, 2 * n_invalid)

    if isinstance(extra_samples, tuple):
        for s, e in zip(samples, extra_samples):
            s[invalid] = e[:n_invalid]

    else:
        samples[invalid] = extra_samples[:n_invalid]

    return samples


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
