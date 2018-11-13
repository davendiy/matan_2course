#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from lab3.classes import taylor_formula, Function

test_func = Function(['x1', 'x2'], lambda a, b: a ** 4 + b ** 4)

print(test_func([2, 2]))
print(test_func.partial_derivative_n(3, ['x1', 'x1', 'x1'], (2, 2)))
print(taylor_formula(test_func, 4, (1.9, 1.9), (2, 2)))
