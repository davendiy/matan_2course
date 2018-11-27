#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import numpy as np
from numpy import cos, sin, pi


def _int1_1(n, mass):
    pts = []
    area = lambda r, phi, psi: r ** 2 * (cos(phi) ** 4 + sin(phi) ** 4 + cos(psi) ** 4 + sin(psi) ** 4)
    density = lambda r, phi, psi: (r**2*cos(psi)) * (r*cos(psi)*cos(phi)) * (phi ** 2 + psi ** 2)   # Jacobean + x1 in spherical + density func
    amt = (1 << n) - 1
    delta = 1 / (1 << n + 1)
    side = 1 / (1 << n)
    for phi in np.linspace(0, 2 * pi, 2 * amt):
        for psi in np.linspace(-pi / 2, pi / 2, amt):
            for r in np.linspace(0, 0.5, amt):
                mid = (r + delta, phi + delta, psi + delta)
                if area(*mid):
                    pts.append((r, phi, psi))
    res = sum([density(*p) * side ** 3 for p in pts])
    return res/mass


def _int2_1(n, mass):
    pts = []
    area = lambda r, phi, psi: r ** 2 * (cos(phi) ** 4 + sin(phi) ** 4 + cos(psi) ** 4 + sin(psi) ** 4)
    density = lambda r, phi, psi: (r**2*cos(psi)) * (r*cos(psi)*sin(phi)) * (phi ** 2 + psi ** 2)        # Jacobean + x2 in spherical + density func
    amt = (1 << n) - 1
    delta = 1 / (1 << n + 1)
    side = 1 / (1 << n)
    for phi in np.linspace(0, 2 * pi, 2 * amt):
        for psi in np.linspace(-pi / 2, pi / 2, amt):
            for r in np.linspace(0, 0.5, amt):
                mid = (r + delta, phi + delta, psi + delta)
                if area(*mid):
                    pts.append((r, phi, psi))
    res = sum([density(*p) * side ** 3 for p in pts])
    return res/mass


def _int3_1(n, mass):
    pts = []
    area = lambda r, phi, psi: r ** 2 * (cos(phi) ** 4 + sin(phi) ** 4 + cos(psi) ** 4 + sin(psi) ** 4)
    density = lambda r, phi, psi: (r**2*cos(psi))*(r*sin(psi))*(phi ** 2 + psi ** 2)
    amt = (1 << n) - 1
    delta = 1 / (1 << n + 1)
    side = 1 / (1 << n)
    for phi in np.linspace(0, 2 * pi, 2 * amt):
        for psi in np.linspace(-pi / 2, pi / 2, amt):
            for r in np.linspace(0, 0.5, amt):
                mid = (r + delta, phi + delta, psi + delta)
                if area(*mid):
                    pts.append((r, phi, psi))
    res = sum([density(*p) * side ** 3 for p in pts])
    return res/mass


def task4(n):
    m = mass(n)
    x1 = _int1_1(n, m)
    x2 = _int2_1(n, m)
    x3 = _int3_1(n, m)
    return x1, x2, x3
