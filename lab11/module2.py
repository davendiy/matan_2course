#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 30.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from math import *
ITERATION_LIMIT = 1000

MAX = 1
MIN = -1


def derivative(func: callable, x0: float, dx=1e-5):
    """
    функція обчислення похідної в точці (симетричний спосіб)
    :param func: функціональний тип
    :param x0: дійсне число (точка)
    :param dx: дійсне число
    :return: дійсне число
    """
    return (func(x0 + dx) - func(x0 - dx)) / (2 * dx)


def _loc_ext(func: callable, a: float, b: float, t=MAX, eps=1e-5):
    """ Знаходження локального екстремуму на відрізку методом
        градієнтного спуску для 2-вимірного випадку

    :param func: функціональний тип
    :param a: ліва межа
    :param b: права межа
    :param t: MAX, MIN - максимум, або мінімум відповідно
    :param eps: точність
    :return: дійсне число - максимум або мінімум функції
    """
    xn = (a + b) / 2       # починаємо з середини
    _gamma = (a + b) / 4    # з кроком == чверть відрізка (визначено експериментальним шляхом)
    for i in range(ITERATION_LIMIT):

        if abs(_gamma) < eps:
            break
        tmp_xn = xn + t * _gamma * derivative(func, xn)    # крок по формулі

        if not a <= tmp_xn <= b:        # додатково перевіряємо, чи не виходимо за межі відрізка
            _gamma /= 2
            continue
        if func(tmp_xn) < func(xn) and t == MIN or func(tmp_xn) > func(xn) and t == MAX:
            xn = tmp_xn
        elif func(tmp_xn) >= func(xn) and t == MIN or func(tmp_xn) <= func(xn) and t == MAX:
            _gamma /= 2
    return func(xn)


def global_ext(func: callable, a: float, b: float, t=MAX, n=1000):
    """ Знаходження глобального максимуму/мінімуму
        функції на відрізкуFalse

    :param func: функціональний тип - функція однієї змінної
    :param a: ліва межа
    :param b: права межа
    :param t: MAX/MIN - максимум, мінімум відповідно
    :param n: к-ть відрізків, на які розбивається область визначення
    :return: значення глобального максимуму/мінімуму
    """
    res = func(a)      # починаємо з лівої межі
    dx = (b - a) / n   # розбиваємо весь відрізок на n маленьких і на кожному з них
    _pre = a           # шукаємо локальний максимум/мінімум відповідно
    _next = a + dx
    for i in range(n):
        tmp_res = _loc_ext(func, _pre, _next, t)
        if tmp_res > res and t == MAX:             # оновлення глобального максимуму/мінімуму
            res = tmp_res
        elif tmp_res < res and t == MIN:
            res = tmp_res

        _pre = _next
        _next += dx
    return res


def _create_check_set(a: float, b: float, u: callable, v: callable):
    """ створення множини - функції, яка повертає True, якщо
        точка входить у множину і False в іншому випадку

    :param a: ліва межа відрізку
    :param b: права межа відрізку
    :param u: нижня кришка циліндричної множини
    :param v: верхня кришка циліндричної множини
    :return: bool
    """
    def res_set(x1, x2):
        succ1 = u(x1) <= x2 <= v(x1)
        succ2 = a <= x1 <= b
        return succ1 and succ2

    return res_set


def mass_center(a: float, b: float, u: callable, v: callable, r: callable):
    """ Обчислення центра мас циліндричної площини
        Кратні інтеграли обчислюються методом розбиття множини на
        бруси з деякою оптимізацією

    :param a: ліва межа відрізку
    :param b: права межа відрізку
    :param u: нижня кришка циліндричної множини
    :param v: верхня кришка циліндричної множини
    :param r: щільність
    :return: (x, y) - координати центра мас
    """
    check_set = _create_check_set(a, b, u, v)    # створення множини
    _max = global_ext(v, a, b, MAX) + 2      # максимум буде визначати верхню межу обмежувального квадрата
    _min = global_ext(u, a, b, MIN) - 2      # мінімум - нижню відповідно

    s = (b-a +_max-_min)/2          # обчислюємо довжину ребра малого бруса
    delta = s / 500                 # в даному варіанті будь-яка множина розбивається на рівну к-ть брусів

    start = [a, _min]               # межі
    end = [b, _max]

    def func1(x1, x2):            # функція для обчислення першої координати
        return x1 * r(x1, x2)

    def func2(x1, x2):            # функція для обчислення другої координати
        return x2 * r(x1, x2)

    mass = naive_integral(r, check_set, 0, 2, start, end, delta, deep=True)             # маса
    res1 = naive_integral(func1, check_set, 0, 2, start, end, delta, deep=True) / mass  # перша координата
    res2 = naive_integral(func2, check_set, 0, 2, start, end, delta, deep=True) / mass  # друга
    return res1, res2


# ---функції з 8 лабораторної для обчислення кратного інтеграла в загальному випадку з деякою оптимізацією--------------

def _msplit(n: int, m: int, start: list, end: list, delta=None):
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
    for center in _msplit(n, m - 1, start, end, delta):    # рекурсивно проходимо по розбиттю
        tmp_start = start[m - 1] + delta / 2            # простору меншої розмірності
        while tmp_start < end[m-1]:               # проходимо новою координатою по розбиттю відповідного відрізка
            yield center + (tmp_start,)           # видаємо точку з новою координатою
            tmp_start += delta


def _cube_points(center: tuple, delta: float, m: int):
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
    for point in _cube_points(center[:m - 1], delta, m - 1):
        yield point + (center[m - 1] + delta,)
        yield point + (center[m - 1] - delta,)


def naive_integral(func: callable, check_set: callable, n: int, m: int, start: list, end: list, delta=None, deep=False):
    """ Кратна інтегральна сума на множині, яку задає функція check_set.
        Тепер оптимізація не забирає стільки часу, скільки в попередньому варіанті

    :param func: функція на множині
    :param check_set: видає True, якщо точка входить в множину, False - інакше
    :param n: к-ть брусів на 1
    :param m: розмірність простору
    :param start: масив лівих меж інтегрування бруса, який обмежує множину
    :param end: масив правих меж інтегрування бруса, який обмежує множину
    :param delta: довжина ребра бруса (якщо вона вказана, то n ігнорується)
    :param deep: флаг, який вказує, чи потрібно рекурсивно обчислювати бруси, що частково входять
    :return: дійсне число
    """
    if delta is None:
        delta = 1 / 2 ** n                   # довжина ребра бруса
    cube_measure = delta ** m            # міра бруса
    res = 0
    diff = 0      # величина, обчислена рекурсивно
    for center in _msplit(n, m, start, end, delta):   # проходимо по центрах всіх брусів розбиття
        flag = True
        count = 0
        for point in _cube_points(center, delta / 2, m):  # якщо всі точки бруса входять у множину,
            if not check_set(*point):
                flag = False
                count += 1
        if flag:
            res += func(*center)        # то додаємо значення функції
        elif count < 4 and deep:        # інакше, якщо брус частково входить у множину
            tmp_start = [center[0] - delta/2, center[1] - delta/2]    # розбиваємо цей брус на менші частини
            tmp_end = [center[0]+delta/2, center[1]+delta/2]          # і рекурсивно рахуємо міру цього бруса
            diff += naive_integral(func, check_set, n+2, m, tmp_start, tmp_end, delta/10)

    res *= cube_measure                 # в кінці домножаємо на міру куба, скориставшись дистрибутивністю
    return res + diff                    # додаємо величину, яку рекурсивно обчислили (оптимізація)


# -------------------------------------------функції для тестування-----------------------------------------------------

def _test_r1(x1, x2):
    return 0.5 * x1**2 + 0.1 * x2**2


def _test_u1(x1):
    return -((4 - x1**2)**0.5)


def _test_v1(x1):
    return (4 - x1**2) ** 0.5


def _test_r2(x1, x2):
    return x1**2 + x2**2


def _test_u2(x1):
    return -10 + sin(x1)


def _test_v2(x1):
    return log(x1) + 100


def _test_u3(x1):
    return sqrt(100 - x1**2)


def _test_v3(x1):
    return log(abs(x1) + 1) + 100


def _test_r3(x1, x2):
    return e ** x1 * cos(x2)


def _test_f(x):
    return x * sin(x)


if __name__ == '__main__':

    print(mass_center(-1, 1, _test_u1, _test_v1, _test_r1))

    print(mass_center(1, 100, _test_u2, _test_v2, _test_r2))

    print(mass_center(-9, 9, _test_u3, _test_v3, _test_r3))
