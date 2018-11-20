#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 19.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import numpy as np
import random


def mul(iterable):
    res = 1
    for el in iterable:
        res *= el
    return res


def msplit(n: int, m: int, start: list, end: list, delta=None):
    """ Розбиття m-вимірного бруса на маленькі бруси

    :param n: [k/2^n, (k+1)/2^n]
    :param m: розмірність
    :param start: список лівих меж для кожної координати
    :param end: список правих меж для кожної координати
    :param delta: довжина ребра бруса
    :yield: центр бруса
    """
    if delta is None:
        delta = 1 / 2 ** n

    if m == 0:
        yield tuple()      # якщо розмірність простору == 0 - видає пустий кортеж
        return
    for center in msplit(n, m-1, start, end, delta):    # рекурсивно проходимо по розбиттю
        tmp_start = start[m - 1] + delta / 2            # простору меншої розмірності
        while tmp_start < end[m-1]:               # проходимо новою координатою по розбиттю відповідного відрізка
            yield center + (tmp_start,)           # видаємо точку з новою координатою
            tmp_start += delta


def cube_points(center: tuple, delta: float, m: int):
    """ Генерує точки бруса (кути + середини всіх гіперграней)

    :param center: центр бруса
    :param delta: допустиме зміщення від центру (довжина ребра / 2)
    :param m: розміність простору
    :yield: кортеж - точка на брусі
    """
    if m == 0:
        yield ()
        return

    # проходимо по всіх таких точках для бруса меншої
    # розмірності і додаємо до кожної точки координату,
    # зміщену на delta вліво і вправо
    for point in cube_points(center[:m - 1], delta, m - 1):
        yield point + (center[m - 1] + delta,)
        yield point + (center[m - 1] - delta,)


def naive_integral(func: callable, check_set: callable, n: int, m: int, start: list, end: list):
    """ Кратна інтегральна сума на множині, яку задає функція check_set.

    :param func: функція на множині
    :param check_set: видає True, якщо точка входить в множину, False - інакше
    :param n: к-ть брусів на 1
    :param m: розмірність простору
    :param start: масив лівих меж інтегрування бруса, який обмежує множину
    :param end: масив правих меж інтегрування бруса, який обмежує множину
    :return: дійсне число
    """
    delta = 1 / 2 ** n                   # довжина ребра бруса
    cube_measure = delta ** m            # міра бруса
    res = 0
    for center in msplit(n, m, start, end, delta):   # проходимо по центрах всіх брусів розбиття
        flag = True
        for point in cube_points(center, delta/2, m):  # якщо всі точки бруса входять у множину,
            if not check_set(*point):
                flag = False
                break
        if flag:
            res += func(*center)        # то додаємо значення функції
    res *= cube_measure                 # в кінці домножаємо на міру куба, скориставшись дистрибутивністю
    return res


def monte_carlo(func: callable, check_set: callable, n: int, start: list, end: list):
    """ Метод Монте-Карло обчислення кратного інтеграла на множині

    :param func: функція на множині
    :param check_set: видає True, якщо точка входить в множину, False - інакше
    :param n: к-ть рандомних точок
    :param start: масив лівих меж інтегрування бруса, який обмежує множину
    :param end: масив правих меж інтегрування бруса, який обмежує множину
    :return: дійсне число
    """
    cube_measure = mul([y - x for x, y in zip(start, end)])   # міра великого бруса
    res = 0
    for i in range(n):     # генеруємо n рандомних точок
        center = tuple([random.uniform(a, b) for a, b in zip(start, end)])

        if check_set(*center):     # перевіряємо, чи належить точка множині
            res += func(*center)   # якщо так, то додаємо значення ф-ції в цій точці

    res = res * cube_measure / n   # домножаємо на міру бруса і ділимо на к-ть точок
    return res


# --------------------------------------------task_functions------------------------------------------------------------
def check_set1(x1, x2):
    """ Задає множину, перевіряючи належність точки їй

    :param x1: координата
    :param x2: координата
    :return: True - точка належить
    """
    return x1 ** 4 + x2 ** 4 <= 1


def check_set2(x1, x2, x3):
    """ Аналогічно

    """
    succ = [x1 ** 2 + x2 ** 2 <= 1,
            x1 + x2 <= x3,
            x3 <= 2 * x2 + 3 * x1]
    return all(succ)


def f(x1, x2):
    return np.sin(np.exp(x1 - x2))


def id_f(*args):
    """ Тривіальна функція для обчислення міри

    :param args: точка
    :return: 1
    """
    return 1


def check_ball(*args):
    """ n-вимірна куля

    :param args: кортеж змінних
    :return: True - точка належить кулі
    """
    res = 0
    for el in args:
        res += el ** 2
    return res <= 0.25

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    with open('output2.txt', 'w', encoding='utf-8') as file:
        file.write('=========task1==========\n')
        file.write('A = {x1, x2 | x1^4 + x2^4 <= 1}\n')
        file.write('Naive method:\n')
        for test_n in [4, 6, 8]:
            rez = naive_integral(id_f, check_set1, test_n, 2, [-1, -1], [1, 1])
            file.write(f'n = {test_n}, measure = {rez}\n')

        file.write("\nMonte-Carlo's method:\n")
        for test_n in [100, 1000, 10000]:
            rez = monte_carlo(id_f, check_set1, test_n, [-1, -1], [1, 1])
            file.write('n = {}, measure = {}\n'.format(test_n, rez))

        # ----------------------------------------------------------------------------
        file.write('\n\nA = {x1, x2, x3 | x1^2 + x2^2 <= 1, x1 + x2 <= x3 <= 2x2 + 3x3}\n')
        file.write('Naive method:\n')
        for test_n in [4, 6, 8]:
            rez = naive_integral(id_f, check_set2, test_n, 3, [-1, -1, -1], [1, 1, 1])
            file.write(f'n = {test_n}, measure = {rez}\n')

        file.write("\nMonte-Carlo's method:\n")
        for test_n in [100, 1000, 10000]:
            rez = monte_carlo(id_f, check_set2, test_n, [-1, -1, -1], [1, 1, 1])
            file.write('n = {}, measure = {}\n'.format(test_n, rez))

        # ----------------------------------------------------------------------------
        file.write('\n\n=========task2==========\n')
        file.write('integral_A (sin(exp(-x1-x2))dx1 dx2, A = {x1, x2 | x1^4 + x2^4 <= 1}\n')
        file.write('Naive method:\n')
        for test_n in [4, 6, 8]:
            rez = naive_integral(f, check_set1, test_n, 2, [-1, -1], [1, 1])
            file.write(f'n = {test_n}, measure = {rez}\n')

        file.write("\nMonte-Carlo's method:\n")
        for test_n in [100, 1000, 10000]:
            rez = monte_carlo(f, check_set1, test_n, [-1, -1], [1, 1])
            file.write('n = {}, measure = {}\n'.format(test_n, rez))

        # ----------------------------------------------------------------------------
        file.write('\n\n=========task3==========\n')
        for test_dim in range(1, 7):
            print(test_dim)
            test_start = [-0.5] * test_dim
            test_end = [0.5] * test_dim
            rez1 = naive_integral(id_f, check_ball, 4, test_dim, test_start, test_end)
            rez2 = monte_carlo(id_f, check_ball, 10000, test_start, test_end)
            file.write('\ndimension = {}, \n'
                       'naive ball measure = {}\n'
                       'ball measure by Monte Carlo = {}\n'.format(test_dim, rez1, rez2))
