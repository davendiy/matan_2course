#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""
модуль для побудови графіка з завдання 5
"""

import numpy as np
import pylab
from mpl_toolkits.mplot3d import Axes3D
from lab3.classes import Function, taylor_formula


def f5(x1, x2):
    """
    f(x1, x2) = arctan(x1 ^ 3 - sin(x2) + 1)
    """
    return np.arctan(x1 ** 3 - np.sin(x2) + 1)


def dot_surface():
    """
    повертає функцію наближеної поверхні четвертого порядку
    """
    func = Function(['x1', 'x2'], f5)

    def tmp_taylor(x: tuple):
        return taylor_formula(func, 4, (0, 0), x)

    return tmp_taylor


def make_data():
    # Строим сетку в интервале от -10 до 10 с шагом 0.1 по обоим координатам
    _x = np.arange(-3, 3, 0.1)
    _y = np.arange(-3, 3, 0.1)

    # Создаем двумерную матрицу-сетку
    x_grid, y_grid = np.meshgrid(_x, _y)

    # В узлах рассчитываем значение функции
    return x_grid, y_grid


grid_x, grid_y = make_data()

surface = dot_surface()
z1 = f5(grid_x, grid_y)
z2 = surface((grid_x, grid_y))

fig = pylab.figure()
axes = Axes3D(fig)

axes.plot_surface(grid_x, grid_y, z1)
axes.plot_surface(grid_x, grid_y, z2)
pylab.show()
