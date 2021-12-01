# SPDX-License-Identifier: MIT
# Copyright (c) 2021 ETH Zurich, Luc Grosheintz-Laval

import lmmr

import tempfile
import os
import h5py
import netCDF4
import numpy as np


def run_on_random_file(create_file, run_checks, suffix):
    foo = np.random.uniform(size=(160, 800, 40))

    with tempfile.TemporaryDirectory() as wd:
        filename = os.path.join(wd, "__a" + suffix)

        create_file(filename, foo)
        run_checks(filename, foo)

        os.remove(filename)


def create_file_h5(filename, array):
    with h5py.File(filename, "w") as h5:
        h5["foo"] = array


def create_file_nc(filename, array):
    with netCDF4.Dataset(filename, "w") as nc:
        dims = [f"dim{k}" for k in range(len(array.shape))]
        for dim, n in zip(dims, array.shape):
            nc.createDimension(dim, n)

        var = nc.createVariable("foo", np.float64, dims)
        var[:, :, :] = array


def test_read_array_h5():
    def check_reading(filename, ground_truth):
        I = np.arange(0, 40, 2)
        n = [10, 400, 20]

        subslices = (slice(n[0]), slice(n[1]), I[: n[2]])
        subfoo = lmmr.io.read_array(filename, "foo", slices=subslices)

        assert np.all(subfoo == ground_truth[: n[0], : n[1], : 2 * n[2] : 2])

    run_on_random_file(create_file_h5, check_reading, suffix=".h5")


def test_read_array_nc():
    def check_reading(filename, ground_truth):
        foo = lmmr.io.read_array(filename, "foo")
        assert np.all(foo == ground_truth)

    run_on_random_file(create_file_nc, check_reading, suffix=".nc")
