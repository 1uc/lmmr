import lmmr

import tempfile
import os
import h5py
import numpy as np


def test_read_array():
    foo = np.random.uniform(size=(160, 800, 40))

    with tempfile.TemporaryDirectory() as wd:
        dummy_file = os.path.join(wd, "__a.h5")
        with h5py.File(dummy_file, "w") as h5:
            h5["foo"] = foo

        I = np.arange(0, 40, 2)
        n = [10, 400, 20]

        subslices = (slice(n[0]), slice(n[1]), I[: n[2]])
        subfoo = lmmr.io.read_array(dummy_file, "foo", slices=subslices)

        assert np.all(subfoo == foo[: n[0], : n[1], : 2 * n[2] : 2])

        os.remove(dummy_file)
