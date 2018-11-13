#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""
модуль з функціями, які реалізують обчислення визначеного інтегралу різними методами
"""

import math
import random


# -------------------------------------функції з завдання---------------------------------------------------------------
def f1(x):
    """
    f(x) = x + cos(x)
    """
    return x + math.cos(x)


def f2(x):
    """
    f(x) = 3 ** (- x ** 2)
    """
    return 3 ** (- x ** 2)


def f3(x):
    """
    f(x) = sin(x ** 10)
    """
    return math.sin(x ** 10)


# -------------------------кортеж з функціями і відповідними межами інтегрування---------------------------------------
LIST_OF_FUNCTIONS = ((f1, (0, 1)),
                     (f2, (0.9, 1)),
                     (f3, (0, 1)))


# -----------------------------функції обчислення інтегралів різними методами-------------------------------------------
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


if __name__ == '__main__':

    steps = [100, 10000, 1000000]
    with open('output_integrals.txt', 'w', encoding='utf-8') as file:

        # проходимо по всіх функціях і обчислюємо інтеграл кожної різними методами
        for f, (tmp_a, tmp_b) in LIST_OF_FUNCTIONS:
            print('\n----calculate for {}----'.format(f.__name__))

            file.write('\n\n' + f.__doc__.strip() + ', x є [{}, {}]\n'.format(tmp_a, tmp_b))
            file.write('Метод прямокутників:\n')
            print('method of rectangles...')
            for step in steps:    # цикл по всіх точностях
                ans = meth_of_rect(f, tmp_a, tmp_b, step)
                file.write('{}, n = {}\n'.format(ans, step))

            file.write('\nМетод трапецій:\n')
            print('method of trapezes...')
            for step in steps:    # цикл по всіх точностях
                ans = meth_of_trap(f, tmp_a, tmp_b, step)
                file.write('{}, n = {}\n'.format(ans, step))

            file.write('\nМетод Сімпсона:\n')
            print("Simpson's method...")

            for step in steps:   # цикл по всіх точностях
                ans = simpson_meth(f, tmp_a, tmp_b, step)
                file.write('{}, n = {}\n'.format(ans, step))

            file.write('\nМетод Монте-Карло:\n')
            print("Monte-Carlo's method...")

            for step in steps:   # цикл по всіх точностях
                ans = monte_carlo_meth(f, tmp_a, tmp_b, step)
                file.write('{}, n = {}\n'.format(ans, step))
