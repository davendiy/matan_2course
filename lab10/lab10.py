#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 20.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from dop_classes import derivative
from dop_classes.integrals import meth_of_trap
import numpy as np
from math import log10


def curve_integral(func: callable, a: float, b: float, u: tuple):
    """ Обчислює криволінійний інтеграл першого порядку

    :param func: функція, яка приймає на вхід певну к-ть змінних
    :param a: ліва межа
    :param b: права межа
    :param u: кортеж функцій, які параметрично задають криву
    :return: дійсне число
    """

    def tmp_func(t):
        """ Створення підінтегральної функції
        """
        # значення (u1(t), u2(t) ... um(t)) - вхідні параметри функції
        params = tuple([tmp_u(t) for tmp_u in u])

        # значення sqrt(u1'(t)^2 + u2'(t)^2 ... + un'(t)^2
        root = np.sqrt(sum([derivative(tmp_u, t) ** 2 for tmp_u in u]))
        return func(*params) * root

    return meth_of_trap(tmp_func, a, b, 10000)     # обчислюємо інтеграл від tmp_func методом трапецій


def id_f(*args):
    """ Тотожна функція для обчислення інтеграла від 1"""
    return 1


def curve1():
    """ Функція, яка параметрично задає криву - повертає
        кортеж з 3 функцій від t
    """

    def u1(t):
        return np.exp(t)

    def u2(t):
        return np.cos(t)

    def u3(t):
        return t ** 7

    return u1, u2, u3


def curve2():
    """ Функція, яка параметрично задає криву - повертає
        кортеж з 2 функцій від t
    """

    def u1(t):
        return t

    def u2(t):
        return log10(t)   # параметризація функції x2=lg(x1)

    return u1, u2


def rho2(x1, x2):
    """ Функція щільності
    """
    return x1 + np.exp(x2)


def curve3():
    """ Функція, яка параметрично задає криву - повертає
        кортеж з 2 функцій від t
    """

    def u1(t):
        return np.log(t)       # параметризація x1 = exp(x2) через логарифм

    def u2(t):                 # для того, щоб функція не зростала так швидко
        return t

    return u1, u2


def rho3(x1, x2):
    """ Функція щільності
    """
    return np.exp(-4*x1)


def mass_center(curve: tuple, mass: float, rho: callable, a: float, b: float):
    """ Обчислення центра мас кривої

    :param curve: кортеж функцій, які параметрично задають криву
    :param mass: маса кривої
    :param rho: функція щільності, має приймати на вхід стільки змінних, скільки всього функцій в curve
    :param a: ліва межа
    :param b: права межа
    :return: список з m чисел - координати
    """
    res = []
    for i in range(len(curve)):      # проходимо по всіх змінних

        def tmp_f(*tmp_args):
            """ Для кожної змінної створюємо нову функцію, від якої треба
                взяти криволінійний інтеграл
            """
            return tmp_args[i] * rho(*tmp_args)

        res.append(curve_integral(tmp_f, a, b, curve)/mass)     # додаємо до списку обчисленні координати
    return res


with open('output.txt', 'w', encoding='utf-8') as file:

    file.write('============task1==============\n')

    file.write('homogeneous curve ((e^t, cos(t), t^7), tє[0, 1])\n')
    length_mass = curve_integral(id_f, 0, 1, curve1())
    mcenter = mass_center(curve1(), length_mass, id_f, 0, 1)
    file.write('length - {}\nmass center - {}'.format(length_mass, mcenter))

    file.write('\n\n============task2==============\n')

    file.write('curve x2 = lg(x1), x1є[1, 10] or ((t, lg(t), tє[1, 10]) with density rho = x1 + exp(x2)\n')
    length = curve_integral(id_f, 1, 10, curve2())
    mass_ = curve_integral(rho2, 1, 10, curve2())
    mcenter = mass_center(curve2(), mass_, rho2, 1, 10)
    file.write('length - {}\nmass center - {}'.format(length, mcenter))

    # Не придумав нічого краще, чим напряму брати інтеграл від 1 до якогось великого числа.
    # Результати порівнював з вольфрамом, при b == 1000 точність складає 1е-6, проте при
    # збільшенні b точність швидко падає через переповнення
    file.write('\n\n============task3==============\n')
    file.write('curve x2 = exp(x1), x1є[1, +inf] or ((t, exp(t), tє[1, +inf]) with density rho = exp(-4x1)\n')
    mass_ = curve_integral(rho3, np.e, 1000, curve3())
    mcenter = mass_center(curve3(), mass_, rho3, np.e, 1000)
    file.write('mass - {}\nmass center - {}'.format(mass_, mcenter))
