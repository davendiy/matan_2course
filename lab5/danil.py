#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from lab4.task1 import minimize


def _build_err_func(points, mes):
    """
    :param points: [(x1, y1), (x2, y2), ..., (xn, yn)]  anchor points on the ceil (lights)
    :param mes: [(dx1, dy1), (dx2, dy2), ..., (dxn, dyn)] measurements, made by robot, distances forwards/backwards,
                right/left to reach a certain anchor point
    :return: function of errors
    """

    def f(x, y):
        return sum([(x - p[0] + dx[0])**2 + (y - p[1] + dx[1])**2 for p in points for dx in mes])

    return f


def get_pos(points, mes):
    """
    :param points: [(x1, y1), (x2, y2), ..., (xn, yn)]  anchor points on the ceil (lights)
    :param mes: [(dx1, dy1), (dx2, dy2), ..., (dxn, dyn)] measurements, made by robot, distances forwards/backwards,
                right/left to reach a certain anchor point
    :return: minimum of the error function (certain position)
    """
    f = _build_err_func(points, mes)
    x0 = [points[0][0] + mes[0][0], points[0][1] + mes[0][1]]     # first point in list of measured (probably closest, not first will be better)
    minimum = minimize(10e-8, 1, f, x0)
    # minimum = task1newton(10e-2, f, x0)
    return minimum


def __test(n):
    import random
    points = []
    measurements = []
    cur_point = random.random() * 4, random.random() * 5
    for i in range(n):
        xi = random.random()*4
        yi = random.random()*5
        points.append((xi, yi))
        distortion = random.random()*0.1 - 0.05, random.random()*0.1 - 0.05
        dx, dy = xi - cur_point[0] + distortion[0], yi - cur_point[1] + distortion[1]
        measurements.append((dx, dy))
    pos = get_pos(points, measurements)
    return pos, cur_point


if __name__ == '__main__':
    print(__test(10))