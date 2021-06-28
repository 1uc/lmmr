import numpy as np

from sobol import i4_sobol


def unit_box(n_dims):
    return [[0.0, 1.0] for k in range(n_dims)]


def rescale(points, domain):
    domain = np.array(domain)

    x0 = domain[:, 0]
    x1 = domain[:, 1]

    return x0 + points * (x1 - x0)


def sobol_points(domain, n_samples, seed=0):
    """Generate the `n_samples` Sobol points."""

    if type(domain) == int:
        domain = unit_box(domain)

    n_dims = len(domain)
    points = np.array([i4_sobol(n_dims, k + seed)[0] for k in range(n_samples)])

    return rescale(points, domain)


def sobol_variances(f, n_params, n_samples, indices):
    # See Sobol (2001), https://doi.org/10.1016/S0378-4754(00)00270-6

    domain = unit_box(2 * n_params)
    X = sobol_points(domain, n_samples)

    x1, x2 = X[:, :n_params], X[:, n_params:]

    mask = np.array([i in indices for i in range(n_params)])
    x12 = np.where(mask, x1, x2)
    x21 = np.where(mask, x2, x1)

    fx1, fx12, fx21 = f(x1), f(x12), f(x21)

    f0 = np.mean(fx1, axis=0)
    dfx1 = fx1 - f0
    dfx12 = fx12 - f0
    dfx21 = fx21 - f0

    D = np.mean(dfx1 ** 2, axis=0)
    Dy = np.mean(dfx1 * dfx12, axis=0)
    Dz = np.mean(dfx1 * dfx21, axis=0)

    Sy = Dy / D
    Stot_y = 1 - Dz / D

    return Sy, Stot_y
