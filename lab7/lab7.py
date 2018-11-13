#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import numpy as np

# TODO зробити швидке перетворення Фур'є


def fdf(fn: np.ndarray, n: int):
    length = len(fn)
    res = 0
    for k in range(length):
        res += fn[k] * np.exp(-2 * complex(0, 1) * np.pi * k * n / length)
    return res


def inverse_fdf(gn: np.ndarray, n: int):
    length = len(gn)
    res = 0
    for k in range(length):
        res += gn[k] * np.exp(2 * complex(0, 1) * np.pi * k * n / length)
    return res / length


def fast_fdf(fn: np.ndarray, n: int):
    pass
