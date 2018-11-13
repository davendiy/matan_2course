#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import scipy.integrate
import numpy as np
import math
import random
import time


def uniform_split(seg: list, n: int) -> list:
    """
    Равномерное разбитие отрезка на n отрезков

    :param seg: отрезок [start, end]
    :param n: кол-во точек разбиения
    :return: список точек разбиений
    """
    assert len(seg) == 2, 'Неверный формат отрезка'
    a, b = seg
    ans = []
    i = 0
    while i != n + 1:
        ans.append(a + ((b - a) * i) / n)
        i += 1
    return ans


def tapers_off_split(seg: list, n: int, side='right') -> list:
    """

    Сужающееся разбиение отрезка на n отрезков

    :param seg: отрезок [start, end]
    :param n: кол-во точек разбиения
    :param side: сужающееся или расширяющееся разбиение (right, left) соответсвенно
    :return: список точек разбиений
    """
    assert len(seg) == 2, 'Неверный формат отрезка'
    a, b = seg
    ans = []
    i = 0
    if side == 'left':
        while i != n + 1:
            ans.append(a + ((b - a) * i**2) / n**2)
            i += 1
    else:
        while i != n + 1:
            ans.append(b - ((b - a) * (n - i)**2) / n**2)
            i += 1
    return ans


def rectangle_method(func: callable, seg: list) -> float:
    """

    Метод прямоугольников

    :param func: функция
    :param seg: отрезок разбиений
    :return: приближенное значение интеграла
    """
    sum = 0
    n = len(seg)
    for k in range(n-1):
        sum += func((seg[k] + seg[k+1]) / 2) * (seg[k+1] - seg[k])
    return sum


def trapeze_method(func: callable, seg: list) -> float:
    """

    Метод трапеций

    :param func: функция
    :param seg: отрезок разбиений
    :return: приближенное значение интеграла
    """
    n = len(seg)
    sum = 0
    for k in range(n-1):
        sum += ((func(seg[k]) + func(seg[k+1])) / 2) * (seg[k+1] - seg[k])
    return sum


def simpson_method(func: callable, seg: list) -> float:
    """

    Метод Симпсона

    :param func: функция
    :param seg: отрезок разбиений
    :return: приближенное значение интеграла
    """
    n = len(seg)
    sum = 0
    for k in range(n-1):
        sum += (func(seg[k]) + 4 * func((seg[k] + seg[k+1]) / 2) + func(seg[k+1])) * (seg[k+1] - seg[k])
    return sum / 6


def monte_carlo_method(func: callable, a: int, b: int, n: int) -> float:
    """

    Метод Монте-Карло

    :param func: функция
    :param a: начало промежутка
    :param b: конец промежутка
    :param n: кол-во точек разбиения
    :return: приближенное значение интеграла
    """
    seg_list = []
    for i in range(n):
        seg_list.append(random.uniform(a, b))
    sum = 0
    for k in range(n-1):
        sum += func(seg_list[k])
    sum /= n
    sum *= (b-a)
    return sum


if __name__ == '__main__':
    P = lambda: print('\n\n')
    # task 1
    eps = 1e-9
    n = 1000, 10000
    f1 = lambda x: math.exp(-x**2)
    f2 = lambda x: math.sin(x) / (x**2 + 1)
    f3 = lambda x: math.sin(x) / (math.sqrt(1 - x))
    res1 = scipy.integrate.quad(lambda x: np.exp(-x**2), 0, np.inf)[0]
    res2 = scipy.integrate.quad(lambda x: np.sin(x) / (x**2 + 1), 0, np.inf)[0]
    res3 = scipy.integrate.quad(lambda x: np.sin(x) / np.sqrt(1 - x), 0, 1)[0]
    res_last = scipy.integrate.quad(lambda x: np.sin(x) / x, 0, np.inf)[0]
    time.sleep(1)
    P()
    print('task 1\n')
    # a
    print('a\n')
    print('f(x) = e**(-x**2), a=0, b=+oo')
    print('точный результат - ', res1)
    print(f'n={n[0]}')
    a1 = 0
    b1 = - int(math.log(eps))
    s1_1 = uniform_split([a1, b1], n[0])
    s1_2 = tapers_off_split([a1, b1], n[0])
    print('метод трапеций, равномерное разбиение: ', trapeze_method(f1, s1_1))
    print('метод трапеций, сужающееся разбиение: ', trapeze_method(f1, s1_2))
    print(f'n={n[1]}')
    s1_1 = uniform_split([a1, b1], n[0])
    s1_2 = tapers_off_split([a1, b1], n[0])
    print('метод трапеций, равномерное разбиение: ', trapeze_method(f1, s1_1))
    print('метод трапеций, сужающееся разбиение: ', trapeze_method(f1, s1_2))
    P()
    # b
    print('b\n')
    print('f(x) = sin(x)/(x**2+1), a=0, b=+oo')
    print('точный результат - ', res2)
    a2 = 0
    b2 = int(math.tan(math.pi/2 - eps))
    s2_1 = uniform_split([a2, b2], 1000000)
    s2_2 = tapers_off_split([a2, b2], 1000000, side='left')
    print('метод трапеций, равномерное разбиение: ', trapeze_method(f2, s2_1))
    print('метод трапеций, сужающееся разбиение: ', trapeze_method(f2, s2_2))

    P()
    # c
    print('c\n')
    print('f(x) = sin(x)/(sqrt(1-x)), a=0, b=1')
    print('точный результат - ', res3)
    a3 = 0
    b3 = 0.99999
    print(f'n={n[0]}')
    s3_1 = uniform_split([a3, b3], n[0])
    s3_2 = tapers_off_split([a3, b3], n[0])
    print('метод трапеций, равномерное разбиение: ', trapeze_method(f3, s3_1))
    print('метод трапеций, сужающееся разбиение: ', trapeze_method(f3, s3_2))
    print(f'n={n[1]}')
    s3_1 = uniform_split([a3, b3], n[1])
    s3_2 = tapers_off_split([a3, b3], n[1])
    print('метод трапеций, равномерное разбиение: ', trapeze_method(f3, s3_1))
    print('метод трапеций, сужающееся разбиение: ', trapeze_method(f3, s3_2))
    P()
    # task 2
    print('task2\n')
    print('f(x) = sin(x)/x, a=0, b=+oo')
    print('точный результат - ', res_last)
    print('после интегрирования частями получили:')
    print('f(x) = (1-cos(x))/x**2')
    f_l = lambda x: (1 - math.cos(x)) / x**2
    # a_2 = 0
    # b_2 = 25
    # s_2 = tapers_off_split([a_2, b_2], n[0])
    # print('метод трапеций, сужающееся разбиение: ', trapeze_method(f_l, s_2))
