#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import numpy as np

eps = 10e-9


def compacting_split(a: float, b: float, n: int) -> np.ndarray:
    """
    розбиття, яке ущільнюється
    :param a: початок відрізка
    :param b: кінець відрізка
    :param n: к-ть частинок
    :return: масив з xi
    """
    res = np.zeros(n)
    for i in range(n):
        res[i] = b - (b - a) * (n - i) ** 2 / n ** 2
    return res


def sparse_split(a: float, b: float, n: int) -> np.ndarray:
    """
    розбиття, яке розріджується
    :param a: початок відрізка
    :param b: кінець відрізка
    :param n: к-ть частинок
    :return: масив з xi
    """
    res = np.zeros(n)
    for i in range(n):
        res[i] = a + (b - a) * i ** 2 / n ** 2
    return res


def meth_of_trap(func: callable, a: float, b: float, n: int, split=sparse_split):
    """
    функція знаходження визначеного інтеграла методом трапецій
    :param func: функціональний тип даних
    :param a: початок інтегрування
    :param b: кінець інтегрування
    :param n: к-ть кроків
    :param split: функція, яка розбиває відрізок
    :return: дійсне число
    """
    x = split(a, b, n)
    rez = 0
    for i in range(n-1):
        rez += (func(x[i]) + func(x[i+1])) * (x[i+1] - x[i]) / 2
    return rez


def f1(x) -> float:
    """
    integral exp(-x^2) dx from 0 to inf
    """
    return np.e ** (-x ** 2)


def f1_end(epsilon) -> float:
    """
    виведено з обмеження функції exp(-x^2) функцією f(x) = exp(-x)
    :param epsilon: точність
    :return: права межа
    """
    return -np.log(epsilon) + 1


def f2(x) -> float:
    """
    integral sin(x) / (x^2 + 1) dx from 0 to inf
    """
    return np.sin(x) / (x ** 2 + 1)


def f2_end(epsilon) -> float:
    """
    виведено з обмеження sin(x) / (x^2 + 1) функцією f(x) = 1 / (x^2 + 1)
    """
    return np.tan(np.pi / 2 - epsilon) // 1000


def f3(x) -> float:
    """
    integral sin(x) / sqrt(1 - x) dx from 0 to 1
    """
    return np.sin(x) / np.sqrt(1 - x)


def f3_end(epsilon):
    """
    обмеження - f(x) = 1 / sqrt(1 - x)
    """
    return 1 - (epsilon ** 2) / 4


def f4(x):
    """
    integral sin(x) / x dx from 0 to inf,
    after integration by the parts: integral (-cos(x) + 1) / 2 dx from 0 to inf
    """
    return (-np.cos(x) + 1) / x ** 2


def f4_end(epsilon):
    """
    обмеження функції (-cos(x) + 1) / x^2 функцією f(x) = 2 / x^2
    """
    return 1 / (epsilon * 100)


FUNC_LIST = [(f1, f1_end(eps), sparse_split),
             (f2, f2_end(eps), sparse_split),
             (f3, f3_end(eps), compacting_split),
             (f4, 10000, sparse_split)]


if __name__ == '__main__':

    for tmp_func, A, interval_split in FUNC_LIST:
        print(tmp_func.__doc__)
        print('A = {}'.format(A))
        print('n = 1000: {}'.format(meth_of_trap(tmp_func, eps, A, 1000, interval_split)))
        print("n = 10000: {}".format(meth_of_trap(tmp_func, eps, A, 10000, interval_split)))
