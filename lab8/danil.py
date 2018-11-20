#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import numpy as np
from random import random


def recursive_iter(n, iterable):
    """
    Plays role of n-times 'for' on 'iterable' items

    :return All n-combinations form iterable elements
    """

    res = []

    def _rec(n, collec, iterable):
        if len(collec) == n:
            res.append(tuple(collec[:]))
            collec.pop()
            return
        for i in range(len(iterable)):
            collec.append(iterable[i])
            _rec(n, collec, iterable)
        if collec:
            collec.pop()

    _rec(n, [], iterable)
    return res


def test1_naive(n):
    f = lambda x, y: x**4 + y**4 <= 1
    a = (-1, 1)
    b = (-1, 1)
    amt1 = abs(a[1] - a[0]) * (1 << n)  # (b-a)*2^n
    amt2 = abs(b[1] - b[0]) * (1 << n)
    inner = 0                           # внутреннее
    outer = 0                           # внешнее
    for x0 in np.linspace(a[0], a[1], amt1 -1):
        for y0 in np.linspace(b[0], b[1], amt2 - 1):
            # print(x0, y0)
            delta = 1/(1 << n)
            l_down = (x0, y0)
            l_up = (x0, y0 + delta)
            r_down = (x0 + delta, y0)
            r_up = (x0 + delta, y0 + delta)
            mid = (x0 + delta/2, y0 + delta/2)
            points = [l_down, l_up, r_down, r_up, mid]
            if any([f(*p) for p in points]):    # if any of points satisfies equation (in area or intersects area)
                outer += 1/(1 << (2 * n))
            if all([f(*p) for p in points]):    # if all points satisfies equation (strictly IN area)
                inner += 1/(1 << (2 * n))
    return inner, outer, outer - inner

#  res, error
# (3.015625, 0.3828125)
# (3.5205078125, 0.11181640625)
# (3.661956787109375, 0.02935791015625)


def test1_monte_carlo(n):
    f = lambda x, y: x ** 4 + y ** 4 <= 1
    a = (-1, 1)
    b = (-1, 1)
    pts = [(random() * 2 - 1, random() * 2 - 1) for i in range(n)]
    inner_pts = [p for p in pts if f(*p)]
    big_area = 4
    factor = len(inner_pts)/len(pts)
    small_area = big_area * factor
    return small_area

# 3.92
# 3.752
# 3.7048


def test2_naive(n):
    f = lambda x, y, z: x ** 2 + y ** 2 <= 1 and z == 0 or\
                        x ** 2 + y ** 2 <= 1 and x + y - z <= 0 or \
                        x ** 2 + y ** 2 <= 1 and 2 * y + 2 * z >= 0
    a = (-1, 1)
    b = (-1, 1)
    c = (-1.5, 1)   # between -2*0.5 and 1
    amt1 = (a[1] - a[0]) * (1 << n)
    amt2 = (b[1] - b[0]) * (1 << n)
    amt3 = (c[1] - c[0]) * (1 << n)
    inner = 0
    outer = 0
    for x0 in np.linspace(a[0], a[1], amt1 - 1):
        for y0 in np.linspace(b[0], b[1], amt2 - 1):
            for z0 in np.linspace(c[0], c[1], amt3 - 1):
                delta = 1/(1 << n)
                mid = (x0 + delta / 2, y0 + delta / 2, z0 + delta / 2)
                points = [      # points of unit block for certain space fragmentation
                    (x0, y0, z0), (x0, y0 + delta, z0), (x0 - delta, y0 + delta, z0), (x0 - delta, y0, z0),
                    (x0, y0, z0 + delta), (x0, y0 + delta, z0 + delta), (x0 - delta, y0 + delta, z0 + delta), (x0 - delta, y0, z0 + delta),
                    mid
                ]
                if any([f(*p) for p in points]): # if any of points satisfies equation (in area or intersects area)
                    outer += 1/(1 << 3*n)
                if all([f(*p) for p in points]): # if all points satisfies equation (strictly in area)
                    inner += 1/(1 << 3*n)
    return inner, outer, outer - inner

# res, err
# (3.765625, 2.3125) n = 2
# (4.71142578125, 1.2099609375) n = 4


def test2_monte_carlo(n):
    f = lambda x, y, z: x ** 2 + y ** 2 <= 1 and z == 0 or \
                        x ** 2 + y ** 2 <= 1 and x + y - z <= 0 or \
                        x ** 2 + y ** 2 <= 1 and 2 * y + 2 * z >= 0
    pts = [(random() * 2 - 1, random() * 2 - 1, random() * 2.5 - 1.5) for i in range(n)]
    inner_pts = [p for p in pts if f(*p)]
    big_area = 10
    factor = len(inner_pts)/len(pts)
    small_area = big_area * factor
    return small_area
# 4.5
# 4.61
# 4.6401
