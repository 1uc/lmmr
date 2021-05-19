# SPDX-License-Identifier: MIT
# Copyright (c) 2021 ETH Zurich, Luc Grosheintz-Laval

def merge_dict(d1, d2):
    """Merge two dictionaries, i.e. {**d1, **d2} in Python 3.5 onwards."""
    d12 = d1.copy()
    d12.update(d2)
    return d12


def with_default(obj, default):
    return default if obj is None else obj


def dhhmmss(t):
    days = t.days
    hours, seconds = divmod(t.seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    return "{:d}-{:02d}:{:02d}:{:02d}".format(days, hours, minutes, seconds)


def hhmm(t):
    days = t.days
    hours, seconds = divmod(t.seconds, 3600)
    minutes, _ = divmod(seconds, 60)
    return "{:02d}:{:02d}".format(24 * days + hours, minutes)


def hhmmss(t):
    days = t.days
    hours, seconds = divmod(t.seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return "{:02d}:{:02d}:{:02d}".format(24 * days + hours, minutes, seconds)
