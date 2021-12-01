import numpy as np

import lmmr


def test_rejection_sampling_1d():
    def rng(n_samples):
        return lmmr.random.uniform(-1.0, 3.0, size=(n_samples))

    def reject_if(x):
        return np.logical_or(x < xlow, x > xhigh)

    xlow, xhigh = -0.5, 0.5

    n_samples = 100
    x = lmmr.sampling.rejection_sampling(n_samples, rng, reject_if)

    assert np.all(x >= xlow), "Too low."
    assert np.all(x <= xhigh), "Too high."
    assert x.shape == (n_samples,)


def test_rejection_sampling_2d():
    def rng(n_samples):
        x = lmmr.random.uniform(-1.0, 3.0, size=(n_samples))
        y = lmmr.random.uniform(-1.0, 3.0, size=(n_samples))
        return x, y

    def reject_if(samples):
        x, y = samples
        return x ** 2 + y ** 2 > rcrit ** 2

    rcrit = 0.25
    n_samples = 100
    x, y = lmmr.sampling.rejection_sampling(n_samples, rng, reject_if)

    assert np.all(x ** 2 + y ** 2 <= rcrit ** 2), "Radius too large."
    assert x.shape == (n_samples,)
