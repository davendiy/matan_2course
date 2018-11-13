#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


import numpy as np
from math import sin, exp, pi
from dop_classes import movespinesticks, norm_plot
import matplotlib.pyplot as plt
import random


def tabulate(func: callable, start, end, n, fault=0):
    """Табулює функцію f на інтервалі [a,b] у n точках

    :param func: функція
    :param start: лівий кінець відрізку
    :param end: правий кінець відрізку
    :param n: к-ть точок у розбитті
    :param fault: вказує на те, чи табулювати з похибкою (0 або 1)
    """
    x = np.linspace(start, end, n)
    x = x
    y = []
    for i in x:
        y.append(func(i) + fault * random.uniform(0, 1))

    y = np.array(y)
    return x, y


def approx_regression(func: callable, start: float, end: float, n=100, m=99):
    """
    наближення функції одної змінної многочленом методом найменших квадратів
    :param func: фукнція одної змінної
    :param start:    початок відрізку
    :param end: кінець відрізку
    :param n: к-ть точок розбиття
    :param m: степінь многочлена
    :return: функція
    """
    x, b = tabulate(func, start, end, n)

    a = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            a[i, j] = x[i] ** j

    coeff = np.linalg.solve(a.transpose().dot(a), a.transpose().dot(b))

    def res_func(_x):
        y = 0
        tmp_x = 1
        for tmp_coeff in coeff:
            y += tmp_coeff * tmp_x
            tmp_x *= _x
        return y

    tmp_str = ''
    for i, tmp_a in enumerate(coeff):
        tmp_str += ' + {}x^{}'.format(tmp_a, i)
    tmp_str = tmp_str[2:]
    res_func.__doc__ = "P(x) = " + tmp_str
    return res_func


def f1(x):
    """
    f(x) = sin(x)
    """
    return sin(x)


def f2(x):
    """
    f(x) = e^x
    """
    return exp(x)


DICT_FUNCTIONS = {f1: (0, 2 * pi),
                  f2: (0, 1)}


if __name__ == '__main__':

    graph_number = 1

    # цикл по функціях
    for test_func, (tmp_start, tmp_end) in DICT_FUNCTIONS.items():
        print("function: {}, x in [{}, {}]".format(test_func.__doc__.strip(), tmp_start, tmp_end))
        k = 1
        for test_m, test_n in [(2, 2), (20, 30)]:     # цикл по к-тях точок
            movespinesticks()
            print("n = {}, m = {}".format(test_n, test_m))
            polinom = approx_regression(test_func, tmp_start, tmp_end, test_n, test_m)
            print("approx func: {}".format(polinom.__doc__))

            test_x, test_y = tabulate(test_func, tmp_start, tmp_end, 100)
            polinom_x, polinom_y = tabulate(polinom, tmp_start, tmp_end, 100)

            norm_plot(test_x, test_y, test_func.__doc__.strip())
            norm_plot(polinom_x, polinom_y, 'P{}(x)'.format(k))
            k += 1
            plt.show()
