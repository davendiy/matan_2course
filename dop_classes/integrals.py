#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 20.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


def meth_of_rect(func, a, b, n):
    """
    функція знаходження визначеного інтеграла методом прямоктуників
    :param func: функціональний тип даних
    :param a: початок інтегрування
    :param b: кінець інтегрування
    :param n: к-ть кроків
    :return: дійсне число
    """
    x = a
    rez = 0
    dx = abs(a - b) / n
    for i in range(n):
        rez += func((2 * x + dx) / 2)
        x += dx
    return rez * dx


def meth_of_trap(func, a, b, n):
    """
    функція знаходження визначеного інтеграла методом трапецій
    :param func: функціональний тип даних
    :param a: початок інтегрування
    :param b: кінець інтегрування
    :param n: к-ть кроків
    :return: дійсне число
    """
    x = a
    rez = 0
    dx = abs(a - b) / n
    for i in range(n):
        rez += (func(x) + func(x + dx)) / 2
        x += dx
    return rez * dx


def simpson_meth(func, a, b, n):
    """
    функція знаходження визначеного інтеграла методом Сімпсона
    :param func: функціональний тип даних
    :param a: початок інтегрування
    :param b: кінець інтегрування
    :param n: к-ть кроків
    :return: дійсне число
    """
    x = a
    rez = 0
    dx = abs(a - b) / n
    for i in range(n):
        rez += (func(x) + 4 * func((2 * x + dx) / 2) + func(x + dx))
        x += dx
    return 1 / 6 * rez * dx


def monte_carlo_meth(func, a, b, n):
    """
    функція знаходження визначеного інтеграла методом Сімпсона
    :param func: функціональний тип даних
    :param a: початок інтегрування
    :param b: кінець інтегрування
    :param n: к-ть кроків
    :return: дійсне число
    """
    rez = 0
    for i in range(n):
        rez += func(random.uniform(a, b))
    return rez * (b - a) / n
