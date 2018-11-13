#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""
реалізувати розв'язання диференціального рівняння
    -
    |f'(t) = k0 * f(t) + g(t)  t >= t0
    |f(t0) = f0
    -
"""
import numpy as np
import matplotlib.pyplot as mat
# нехай f(t) = t^3, k0 = 2,  g(t) = 3t^2 - 2t^3, t є [0, 1]


def test_f(t):
    return t ** 3


def g(t):
    return 3 * t ** 2 - 2 * t ** 3


def diff_eq(sub_func, a, b, k0, delta):
    y0 = sub_func(a)
    yn = y0
    rez_y = [y0]
    rez_x = [a]
    xn = a
    t = True
    while xn < b:
        tmp = delta * (k0 * yn + sub_func(xn))

        if xn > 6 and t:
            delta *= 0.01
            t = False
        yn = tmp + yn
        xn += delta
        rez_y.append(yn)
        rez_x.append(xn)
    return rez_y, rez_x


if __name__ == '__main__':
    array_y, array_x = diff_eq(g, 0, 4.5, 2, 0.001)
    array_x = np.array(array_x)
    array_y = np.array(array_y)

    print(array_x)
    print(array_y)

    test_func_x = [0 + j * 0.01 for j in range(500)]
    test_func_y = list(map(test_f, test_func_x))
    test_func_x = np.array(test_func_x)
    test_func_y = np.array(test_func_y)

    mat.plot(array_x, array_y)
    mat.plot(test_func_x, test_func_y)
    mat.show()
