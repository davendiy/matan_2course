#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""
sage скрипт для побудови графіка з завдання 3
"""

import numpy as np


def f3(x, y):
    return x ** 2 + y ** 4


def der3(x, y):
    return np.array([2 * x, 4 * y ** 3])


def dot_plane(x, y):
    return f3(1, 1) + np.sum(der3(1, 1) * np.array([x - 1, y - 1]))


Plot1 = plot3d(f3, (-5, 5), (-5, 5), color='purple')
Plot2 = plot3d(dot_plane, (-5, 5), (-5, 5), color='yellow')
show(Plot1 + Plot2)
