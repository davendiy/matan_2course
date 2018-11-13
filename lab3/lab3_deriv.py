#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""
основний скрипт
"""

from math import log, e, sqrt
import numpy as np
from lab3.classes import Function, taylor_formula

# %% task1


def f1(x1, x2):
    """
    f(x, y) = x ^ 5 * log(1 + y)
    """
    return x1 ** 5 * log(1 + x2)


def task1(x: np.array):
    """
    завдання 1 (наближено обчислити значення функції)
    :param x:
    :return:
    """
    x0 = np.array([1, 0])             # нульова точка
    func1 = Function(['x1', 'x2'], f1)    # створюємо об'єкт класу Function
    f_x1 = func1([x[0], x[1]])            # реальне значення в точці
    tmp_der = func1.derivative(1, (x[0], x[1]))    # похідна
    tmp_der = np.array(tmp_der)
    f_x2 = func1([x0[0], x0[1]]) + sum(tmp_der * (x - x0))   # наближене обчислення значення в точці
    return f_x1, f_x2


# %% task2

def f2(x1, x2, x3):
    """
    f(x1, x2, x3) = e ^ (x1 + x2 + x3)
    """
    return e ** (x1 + x2 + x3)


def der2(x1, x2, x3):
    """
    обчислення похідної в точці через універсальну функцію з модуля
    """
    tmp_func = Function(['x1', 'x2', 'x3'], f2)
    return np.array(tmp_func.derivative(1, (x1, x2, x3)))


def task2(x: np.array):
    """
    завдання 2 (наближено обчислити значення функції за допомогою диференціала)
    """
    x0 = np.array([0, 0, 0])
    f_x1 = f2(*tuple(x))
    f_x2 = f2(*tuple(x0)) + sum(der2(*tuple(x)) * (x - x0))
    return f_x1, f_x2


def estimation(eps):
    """
    знаходження точного околу початку координат, в якому помилка обчислення наближеної
    функції < eps

    працює все через формулу, яку я вивів на практичному занятті, але я її забув

    :param eps: дійсне додатнє число
    :return: дійсне число
    """
    max_delta_x1 = sqrt(sqrt(eps) / 3) + 100
    max_delta_x2 = log(sqrt(eps) + 1) / 3 + 100
    max_delta = max(max_delta_x1, max_delta_x2)

    start = np.zeros(3)
    end = np.array([max_delta] * 3)

    delta = abs(start - end) > 0.0001
    tmp_x = end
    while delta.any():

        tmp_x = (start + end) / 2
        tmp_right_y = f2(*tuple(tmp_x))
        tmp_approx_y = f2(0, 0, 0) + sum(der2(*tuple(tmp_x)) * tmp_x)
        if (tmp_approx_y - tmp_right_y) <= eps:
            start = tmp_x
        else:
            end = tmp_x
        delta = abs(start - end) > 0.0001
    return tmp_x


# %% task3

def f3(x, y):
    """
    f(x, y) = x ^ 2 + y ^ 4
    """
    return x ** 2 + y ** 4


def der3(x, y):
    """
    обчислення похідної в точці через універсальну функцію з модуля
    """
    tmp_func = Function(['x', 'y'], f3)
    return np.array(tmp_func.derivative(1, (x, y)))


def dot_plane(x, y):
    """
    функція дотичної площини
    """
    return f3(1, 1) + np.sum(der3(1, 1) * np.array([x - 1, y - 1]))


# %% task4

def f4(x, y):
    """
    f(x, y) = (x - y + 1) * sin(x + y)
    """
    return (x - y + 1) * np.sin(x + y)


def task4():
    """
    обчислення наближених значень функції через формули тейлора
    """
    func = Function(['x', 'y'], f4)
    res1 = func([0.1, 0.05])

    # через універсальну формулу
    res2 = taylor_formula(func, 2, (0, 0), (0.1, 0.05))   # n = 2
    res3 = taylor_formula(func, 3, (0, 0), (0.1, 0.05))   # n = 3
    return res1, res2, res3


# %% task5


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


if __name__ == '__main__':

    print('--------------task1----------------')
    print(f1.__doc__)
    for point in [(1.5, 0.7), (1.05, 0.07), (1.005, 0.007)]:
        rez1, rez2 = task1(np.array(point))
        print("point: {}".format(point))
        print("f(x) = {}, approx_f(x) = {}".format(rez1, rez2))
        print()
    input("press enter to continue...\n")

    print("\n--------------task2----------------")
    print(f2.__doc__)
    rez1, rez2 = task2(np.array([0.1, 0.05, -0.01]))
    print('f(x) = {}, approx_f(x) = {}'.format(rez1, rez2))
    print("estimation =", estimation(0.1))
    input("press enter to continue...\n")

    print("\n--------------task3----------------")

    print("look in the plot.sage")
    input("press enter to continue...\n")

    print("\n--------------task4----------------")
    print(f4.__doc__)
    rez1, rez2, rez3 = task4()
    print("f(x) = {}\napprox_f(x, 2) = {}\napprox_f(x, 3) = {}".format(rez1, rez2, rez3))
    input("press enter to continue...\n")

    print("\n--------------task5----------------")
    print('look in the plot.py')
