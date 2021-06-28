import numpy as np

import lmmr
import lmmr.qmc


def test_sobol_variances():
    def phi(xi, ai):
        return (np.abs(4.0 * xi - 2.0) + ai) / (1.0 + ai)

    def g(x, a):
        phi_x = np.array([phi(x[:, i], a[i]) for i in range(a.shape[0])])
        gxa = np.product(phi_x, axis=0)

        return gxa

    a = np.array(2 * [0.0] + 6 * [3.0])

    def sv(indices):
        n_samples = 10_000
        return lmmr.qmc.sobol_variances(
            lambda x: g(x, a), a.shape[0], n_samples, indices
        )

    hi, lo = [0, 1], list(range(2, 8))
    eps = 0.03

    Si = dict()
    for i in range(8):
        Si[i], _ = sv([i])

        exact = 0.329 if i in hi else 0.021
        assert np.abs(Si[i] - exact) < eps

    for i in range(8):
        for j in range(8):
            if i == j:
                continue

            Sy, _ = sv([i, j])
            S_ij = Sy - Si[i] - Si[j]

            if i in hi and j in hi:
                exact = 0.110
            elif i in hi or j in hi:
                exact = 0.007
            else:
                exact = 0.0004

            assert np.abs(S_ij - exact) < eps
