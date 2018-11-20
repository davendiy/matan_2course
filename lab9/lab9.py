#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 20.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

# TODO доробити завдання з функцією у сферичних координатах

from dop_classes.multiple_integrals import *


def set1(x1, x2):
    return x1 ** 4 + x2 ** 4 <= 1


def rho1(x1, x2):
    return 2 - x1 ** 2 - x2 ** 2


def set2(x1, x2, x3):
    succ1 = x1 ** 2 + x2 ** 2 <= 1
    succ2 = abs(x3) <= 2
    return succ1 and succ2


def rho2(x1, x2, x3):
    return x1 ** 2 + x2 ** 2 + x3 ** 2


def set3(x1, x2, x3):
    succ1 = x1 ** 2 + x2 ** 2 + x3 ** 2 <= 1
    succ2 = x1 > 0 and x2 > 0 and x3 > 0
    return succ1 and succ2


def rho3(x1, x2, x3):
    return x1 ** 2 + x2 ** 2


def mass_center(check_set: callable, rho: callable, m: int, start: list, end: list):
    res = []
    for i in range(m):

        def tmp_f(*tmp_args):
            return tmp_args[i] * rho(*tmp_args)

        res.append(monte_carlo(tmp_f, check_set, 10000, start, end))
    return tuple(res)


with open('output.txt', 'w', encoding='utf-8') as file:
    file.write('============task1==============\n')
    res1 = naive_integral(rho1, set1, 4, 2, [-1, -1], [1, 1])
    res2 = monte_carlo(rho1, set1, 10000, [-1, -1], [1, 1])

    file.write('mass of plate {(x1, x2) | x1^4 + x2^4 <= 1} with rho = 2 - x1^2 - x2^2:\n')
    file.write('by naive method (n = 4) - {}\n'
               'by Monte Carlo method - {}\n'.format(res1, res2))

    res1 = naive_integral(rho2, set2, 4, 3, [-1, -1, -2], [1, 1, 2])
    res2 = monte_carlo(rho2, set2, 10000, [-1, -1, -2], [1, 1, 2])

    file.write('\n\n============task2==============\n')
    file.write('mass of plate {(x1, x2, x3) | x1^2 + x2^2 <= 1, |x3| <= 2} with rho = x1^2 + x2^2 + x3^2:\n')
    file.write('by naive method (n = 4) - {}\n'
               'by Monte Carlo method - {}\n'.format(res1, res2))

    file.write('\n\n============task3==============\n')
    res1 = mass_center(set3, rho3, 3, [0, 0, 0], [1, 1, 1])
    file.write('mass center of solid {(x1, x2, x3) | x1^2 + x2^2 + x3^2 <= 1, x1>=0, x2>=0, x3>=0}\n'
               '    with pho = x1^2 + x2^2:\n')
    file.write('by Monte Carlo method = {}\n'.format(res1))
