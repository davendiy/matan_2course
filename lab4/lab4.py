#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""
для f4 мінімумом буде точка (1, 1, 1), метод градієнтного спуску показує такий же результат

для f3 нема ні мінімума, ні максимума
(в точці (0, 0) є такою, як точка 0 в f(x) = x^3, обидва методи видають її)

для f2 мінімум - (0, 0), такий результат видають обидва методи, але тільки якщо точка x0 - (0, 0),
максимуми - (+-10, +-10), видаються обома методами

для f1 мінімум - (1, -5/6). Це єдина функція, для якої обидва методи чомусь видають (-6.25, 1).

Мінімуми перевіряв з тими, які показує Вольфрам
"""

from dop_classes.multydimensional import Function
import numpy as np


ITERATION_LIMIT = 1000


def grad_meth(func: Function, x0: np.array, y0: float, t=1, eps=10e-5):
    """
    метод градієнтного спуску знаходження локального максимуму/мінімуму

    :param func: функція багатьох змінних
    :param x0: стартова точка (вектор чисел)
    :param y0: стартове гамма
    :param t: +- 1 (вказує на максимум/мінімум відповідно)
    :param eps: точність
    :return: точка мінімуму (вектор чисел)
    """
    xn = x0
    for i in range(ITERATION_LIMIT):
        tmp_xn = xn + t * (y0 * np.array(func.derivative(1, tuple(xn))))
        if func(tmp_xn) < func(xn) and t < 0 or func(tmp_xn) > 0 and t > 0:
            xn = tmp_xn
        elif func(tmp_xn) >= func(xn) and t < 0 or func(tmp_xn) <= 0 < t:
            y0 /= 2

        if abs(y0) < eps:
            print("к-ть ітерацій для метода град. спуску:", i)
            break
    else:
        print("перевищено максимальну к-ть ітерацій - {} (метод град. спуску)".format(ITERATION_LIMIT))
    return xn


def newton_meth(func: Function, x0: np.array, t=1, eps=10e-5):
    """
    метод Ньютона знаходження локального мінімуму/максимуму

    :param func: функція багатьох змінних
    :param x0: стартова точка (вектор чисел)
    :param t: +- 1 (вказує на максимум/мінімум відповідно)
    :param eps: точність
    :return: точка мінімуму (вектор чисел)
    """

    xn = x0
    for i in range(ITERATION_LIMIT):
        der1 = func.derivative(1, tuple(x0))
        der2 = _gradient2(func, tuple(x0))

        der1 = np.array(der1)
        if np.linalg.det(der2) == 0:
            print('Метод Ньютона не працює')
            return

        der2 = np.linalg.inv(der2)
        step = der2.dot(der1)
        tmp_xn = xn + t * step

        if np.sum(np.abs(step)) < eps or func(tmp_xn) > func(xn) and t < 0 or \
                func(tmp_xn) < func(xn) and t > 0:
            print("к-ть ітерацій для метода Ньютона:", i)
            break
        xn = tmp_xn
    else:
        print("перевищено максимальну к-ть ітерацій - {} (метод Ньютона)".format(ITERATION_LIMIT))
    return xn


def _gradient2(func: Function, x0: tuple) -> np.array:
    """
    побудова матриці похідної 2-го порядку
    :param func: функція багатьох змінних
    :param x0: точка, в якій шукається значення
    :return: матриця
    """
    res = np.zeros((len(func.variables), len(func.variables)))
    for i, var1 in enumerate(func.variables):
        for j, var2 in enumerate(func.variables):
            res[i, j] = func.partial_derivative_n(2, [var1, var2], x0)
    return res


def f1(x, y):
    """
    f(x, y) = 2x^2 + 3y^2 - 4x + 5y - 1
    """
    return 2 * x ** 2 + 3 * y ** 2 - 4 * x + 5 * y - 1


def f2(x, y):
    """
    f(x, y) = x^2 + 2y^2 - 4y^4 - x^4 + 3
    """
    return x ** 2 + 2 * y ** 2 - 4 * y ** 4 - x ** 4 + 3


def f3(x, y):
    """
    f(x, y) = x^2 - y^2
    """
    return x ** 2 - y ** 2


def f4(x, y, z):
    """
    f(x, y, z) = (x^2 + y^2 + z^2)^2 + ((x - 2)^2 + (y - 2)^2 + (z - 2)^2)^2
    """
    return (x ** 2 + y ** 2 + z ** 2) ** 2 + ((x - 2) ** 2 + (y - 2) ** 2 + (z - 2) ** 2) ** 2


# словник з фукнціями і відповідними точками старту
DICT_OF_POINT = {f1: [(10, 10)],
                 f2: [(10, 10), (10, -10), (-10, -10), (-10, 10), (0, 0)],
                 f3: [(1, 1)],
                 f4: [(3, 3, 3), (-1, -2, -3), (1, 1, 1)]}


if __name__ == '__main__':

    for f, points in DICT_OF_POINT.items():
        tmp_func = Function(f)
        print('\n' + str(tmp_func) + '\n')
        for point in points:
            tmp_point = np.array(point)
            print("point:", point)
            rez1 = grad_meth(tmp_func, tmp_point, 2, t=-1)
            rez2 = newton_meth(tmp_func, tmp_point, t=-1)
            print("minimum by grad method: {}\n"
                  "minimum by Newton's method: {}".format(rez1, rez2))
            rez1 = grad_meth(tmp_func, tmp_point, 2, t=1)
            rez2 = newton_meth(tmp_func, tmp_point, t=1)
            print("maximum by grad method: {}\n"
                  "maximum by Newton's method: {}".format(rez1, rez2))
            print()
