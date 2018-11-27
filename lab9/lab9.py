#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 20.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from dop_classes.multiple_integrals import *
from math import sqrt, atan, cos, sin


# -------------------------------------------------task1----------------------------------------------------------------
def set1(x1, x2):
    """ Функція, яка задає множину у 2-мірному просторі:
        повертає True, якщо задана точка належить множині
    """
    return x1 ** 4 + x2 ** 4 <= 1


def rho1(x1, x2):
    """ Щільність тіла у 2-вимірному просторі
    """
    return 2 - x1 ** 2 - x2 ** 2


# -------------------------------------------------task2----------------------------------------------------------------
def set2(x1, x2, x3):
    """ Функція, яка задає множину у 3-мірному просторі:
        повертає True, якщо задана точка належить множині
    """
    succ1 = x1 ** 2 + x2 ** 2 <= 1
    succ2 = abs(x3) <= 2
    return succ1 and succ2


def rho2(x1, x2, x3):
    """ Щільність тіла у 3-вимірному просторі
    """
    return x1 ** 2 + x2 ** 2 + x3 ** 2


# -------------------------------------------------task3----------------------------------------------------------------
def set3(x1, x2, x3):
    """ Функція, яка задає множину у 3-мірному просторі:
        повертає True, якщо задана точка належить множині
    """
    succ1 = x1 ** 2 + x2 ** 2 + x3 ** 2 <= 1
    succ2 = x1 > 0 and x2 > 0 and x3 > 0
    return succ1 and succ2


def rho3(x1, x2, x3):
    """ Щільність тіла у 3-вимірному просторі
    """
    return x1 ** 2 + x2 ** 2


# -------------------------------------------------task4----------------------------------------------------------------
def descartes2spherical(x1, x2, x3):
    """ Перетворення декартових координат у сферичні

    :return: кортеж із трьох дійсних чисел
    """
    return sqrt(x1**2 + x2**2 + x3**2), \
           atan(sqrt(x1**2 + x2**2)/x3), \
           atan(x2/x1)


def set4(x1, x2, x3):
    """ Функція, яка задає множину у 3-мірному просторі:
        повертає True, якщо задана точка належить множині
    """
    r, phi, psi = descartes2spherical(x1, x2, x3)   # transform coord before check
    return r**2 * (cos(phi)**4 + sin(phi)**4 + cos(psi)**4 + sin(psi) ** 4 + 2) <= 1


def rho4(x1, x2, x3):
    """ Щільність тіла у 3-вимірному просторі
    """
    r, phi, psi = descartes2spherical(x1, x2, x3)
    return phi**2 + psi**2


def mass_center(check_set: callable, rho: callable, m: int, start: list, end: list):
    """ Обчислення центру мас тіла у m-мірному просторі

    :param check_set: функція, яка приймає на вхід m змінних і повертає True, якщо точка знаходиться в множині
    :param rho: функція щільності (теж приймає m змінних на вхід)
    :param m: к-ть вимірів
    :param start: список лівих меж на всіх координатних осях
    :param end: список правих меж на всіх координатних осях    (задання великого бруса)
    :return: кортеж із m елементів
    """
    res = []
    for i in range(m):     # проходимо циклом по всім змінним

        def tmp_f(*tmp_args):
            """ Створення підінтегральної функції для кожної координати
            """
            return tmp_args[i] * rho(*tmp_args)   # xi * rho(x)

        # обчислюємо кожну координату методом Монте-Карло
        res.append(monte_carlo(tmp_f, check_set, 10000, start, end))
    return tuple(res)



with open('output.txt', 'w', encoding='utf-8') as file:

    # громіздке виведення
    # ¯\_(ツ)_/¯
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
               'with pho = x1^2 + x2^2:\n')
    file.write('by Monte Carlo method - {}\n'.format(res1))

    file.write('\n\n============task4==============\n')
    res1 = mass_center(set4, rho4, 3, [-1, -1, -1], [1, 1, 1])
    file.write('mass center of solid {(r, phi, psi) | r^2(cos^4(phi) + sin^4(phi) + cos^4(psi) + sin^4(psi)) <= 1}\n'
               'with pho = phi^2 + psi^2:\n')

    file.write('by Monte Carlo method - {}\n'.format(res1))
