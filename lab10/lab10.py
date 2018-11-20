#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 20.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

# TODO доробити всьо

from dop_classes import derivative
from dop_classes.integrals import meth_of_trap
import numpy as np


def curve_integral(func: callable, a: float, b: float, *u):

    def tmp_func(t):
        params = tuple([tmp_u(t) for tmp_u in u])
        root = np.sqrt(sum([derivative(tmp_u, t) ** 2 for tmp_u in u]))
        return func(*params) * root

    return meth_of_trap(tmp_func, a, b, 10000)


def id_f(*args):
    return 1


def curve1():

    def u1(t):
        return np.exp(t)

    def u2(t):
        return np.cos(t)

    def u3(t):
        return t ** 7

    return u1, u2, u3


def mass_center(curve, mass, rho, a, b):
    res = []
    for i in range(len(curve)):

        def tmp_f(*tmp_args):
            return tmp_args[i] * rho(*tmp_args)

        res.append(curve_integral(tmp_f, a, b, *curve)/mass)


with open('output.txt', 'w', encoding='utf-8') as file:
    file.write('============task1==============\n')

    res1 = curve_integral(id_f, 0, 1, *curve1())
    print(res1)
    res2 = mass_center(curve1(), res1, id_f, 0, 1)
