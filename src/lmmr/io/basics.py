# SPDX-License-Identifier: MIT
# Copyright (c) 2021 ETH Zurich, Luc Grosheintz-Laval

import json
import os
import pickle
import itertools
import csv
import hashlib

import lmmr


def random_hash(length=5):
    import numpy as np

    hash = hashlib.sha256(f"{np.random.randint(2**32-1)}".encode()).hexdigest()
    return hash[:length]


def symlink(src, dst, overwrite=False):
    if overwrite and os.path.islink(dst):
        os.unlink(dst)

    os.symlink(src, dst)


def first_non_existant(pattern):
    """Returns the first path which does not exist.

    Input:
        pattern: This is a format string containing one (integer) field.
    """
    dir_gen = (pattern.format(k) for k in itertools.count())
    return next(d for d in dir_gen if not os.path.exists(d))


def ensure_directory_exists(filename=None, dirname=None):
    if dirname is None:
        dirname = os.path.dirname(filename)

    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)


def _guess_hdf5_netcdf(filename):
    if filename.endswith(".h5"):
        return "HDF5"

    elif filename.endswith(".nc"):
        return "NETCDF"

    else:
        raise RuntimeError("Can't deduce file format.")


def read_array(filename, key, slices=None, format=None):
    if format is None:
        format = _guess_hdf5_netcdf(filename)

    if format == "HDF5":
        return read_array_h5(filename, key, slices)

    if format == "NETCDF":
        return read_array_nc(filename, key, slices)

    raise RuntimeError(f"Unknown format. [{format}]")


def read_array_h5(filename, key, slices=None):
    import numpy as np
    import h5py

    with h5py.File(filename, "r") as h5:
        if slices is None:
            return np.array(h5[key])

        else:
            return np.array(h5[key][slices])


def read_array_nc(filename, key, slices=None):
    import numpy as np
    import netCDF4

    if slices is not None:
        raise NotImplemented("Slicing must be implement first.")

    with netCDF4.Dataset(filename, "r") as nc:
        return np.array(nc[key])


def read_array_shape(filename, key):
    import h5py

    with h5py.File(filename, "r") as h5:
        return h5[key].shape


def read_something(filename, command, mode="r", **kwargs):
    with open(filename, mode, **kwargs) as f:
        return command(f)


def write_something(filename, command, mode="w", **kwargs):
    ensure_directory_exists(filename)
    with open(filename, mode=mode, **kwargs) as f:
        command(f)


def read_txt(filename):
    return read_something(filename, lambda f: f.read())


def write_txt(filename, string):
    write_something(filename, lambda f: f.write(string))


def read_json(filename):
    return read_something(filename, lambda f: json.load(f))


class NumpyEncoder(json.JSONEncoder):
    # credit: https://stackoverflow.com/a/47626762

    def default(self, obj):
        import numpy as np

        transforms = [
            (np.ndarray, lambda obj: obj.tolist()),
            (np.float16, lambda obj: float(obj)),
            (np.float32, lambda obj: float(obj)),
            (np.float64, lambda obj: float(obj)),
            (np.float128, lambda obj: float(obj)),
            (np.int16, lambda obj: int(obj)),
            (np.int32, lambda obj: int(obj)),
            (np.int64, lambda obj: int(obj)),
        ]

        for T, f in transforms:
            if isinstance(obj, T):
                return f(obj)

        return json.JSONEncoder.default(self, obj)


def write_json(filename, obj):
    write_something(filename, lambda f: json.dump(obj, f, indent=4, cls=NumpyEncoder))


def read_pickle(filename):
    return read_something(filename, lambda f: pickle.load(f), mode="rb")


def write_pickle(filename, obj):
    write_something(filename, lambda f: pickle.dump(obj, f), mode="wb")


def read_csv(filename, delimiter=","):
    def parse(f):
        reader = csv.DictReader(f, delimiter=delimiter)
        return [row for row in reader]

    return read_something(filename, parse, newline="", encoding="utf-8")


def savefig(filename, dpi=300, bbox_inches="tight", **kwargs):
    import matplotlib.pyplot as plt

    lmmr.io.ensure_directory_exists(filename)
    plt.savefig(filename, dpi=dpi, bbox_inches=bbox_inches, **kwargs)
