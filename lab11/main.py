#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 01.12.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from module2 import *
import time

test_a = 1             # write your consts here
test_b = 100


def test_u(x1):

    # write your code here (functions from math module are available)
    return -log(x1)


def test_v(x1):

    # write your code here (functions from math module are available)
    return cos(x1) + 54


def test_r(x1, x2):

    # write your code here (functions from math module are available)
    return x1**2 + x2**2

t = time.time()
print("result: {}".format(mass_center(test_a, test_b, test_u, test_v, test_r)))
print('time elapsed: {}'.format(time.time() - t))
