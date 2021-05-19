# SPDX-License-Identifier: MIT
# Copyright (c) 2021 ETH Zurich, Luc Grosheintz-Laval

import json
import os
import pickle
import itertools


def first_non_existant(pattern):
    """Returns the first path which does not exist.

    Input:
        pattern: This is a format string containing one (integer) field.
    """
    dir_gen = (pattern.format(k) for k in itertools.count())
    return next(d for d in dir_gen if not os.path.exists(d))


def ensure_directory_exists(filename):
    dirname = os.path.dirname(filename)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)


def read_array(filename, key):
    import numpy as np
    import h5py

    with h5py.File(filename, "r") as h5:
        return np.array(h5[key])


def read_something(filename, command, mode="r"):
    with open(filename, mode) as f:
        return command(f)


def write_something(filename, command, mode="w"):
    ensure_directory_exists(filename)
    with open(filename, mode) as f:
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
