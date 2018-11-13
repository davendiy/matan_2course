#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from dop_classes import Function
import numpy as np
import random

ITERATION_LIMIT = 1000


def grad_meth(func: Function, x0: np.array, y0: float, t=1, eps=10e-5):
    """
    метод градієнтного спуску знаходження локального максимуму/мінімуму

    :param func: функція багатьох змінних
    :param x0: стартова точка (вектор чисел)
    :param y0: стартове гамма
    :param t: +- 1 (вказує на максимум/мінімум відповідно)
    :param eps: точність
    :return: точка мінімуму (вектор чисел)
    """
    xn = x0
    for i in range(ITERATION_LIMIT):
        tmp_xn = xn + t * (y0 * np.array(func.derivative(1, tuple(xn))))
        if func(tmp_xn) < func(xn) and t < 0 or func(tmp_xn) > 0 and t > 0:
            xn = tmp_xn
        elif func(tmp_xn) >= func(xn) and t < 0 or func(tmp_xn) <= 0 < t:
            y0 /= 2

        if abs(y0) < eps:
            print("к-ть ітерацій для метода град. спуску:", i)
            break
    else:
        print("перевищено максимальну к-ть ітерацій - {} (метод град. спуску)".format(ITERATION_LIMIT))
    return xn


def find_robot(list_of_lamps, list_of_dxdy):
    """
    простий варіант задачі про робота

    знайти реальні координати x, y робота на площині, якщо відомі координати
    деяких точок у глобальній системі координат і у системі робота (початком координат є він сам_

    :param list_of_lamps: список кортежів (координати точок у глобальній системі координат)
    :param list_of_dxdy: список кортежів (координати точок у системі робота)
    :return: кортеж із 2-х елементів (х, у)
    """
    assert len(list_of_lamps) == len(list_of_dxdy)

    def _tmp_func(x, y):
        """
        функція суми квадратів помилок, яку треба мінімізувати
        :param x: абсциса положення робота
        :param y: ордината положення робота
        :return: середньоквадратичне відхилення
        """
        rez = 0
        for lamp, pos in zip(list_of_lamps, list_of_dxdy):
            rez += (x - lamp[0] + pos[0]) ** 2 + (y - lamp[1] + pos[1]) ** 2
        return rez

    # початкова точка для град спуску (положення робота з похибкою)
    start_x1 = list_of_lamps[0][0] - list_of_dxdy[0][0]
    start_x2 = list_of_lamps[0][1] - list_of_dxdy[0][1]
    res = grad_meth(Function(_tmp_func), np.array((start_x1, start_x2)), 0.2, t=-1)
    return res


def find_robot2(list_of_lamps, list_of_dxdy):
    assert len(list_of_lamps) == len(list_of_dxdy)

    def _tmp_func(x, y, alpha):
        """
        функція суми квадратів помилок, яку треба мінімізувати

        :param x: x абсциса положення робота
        :param y: у ордината положення робота
        :param alpha: кут поворота
        :return: середньоквадратичне відхилення
        """
        rez = 0
        for lamp, pos in zip(list_of_lamps, list_of_dxdy):
            tmp_x = x - (lamp[0] - pos[0] * np.cos(alpha) + pos[1] * np.sin(alpha))
            tmp_y = y - (lamp[1] - pos[0] * np.sin(alpha) - pos[1] * np.cos(alpha))
            rez += tmp_x ** 2 + tmp_y ** 2

        return rez

    # знаходження більш-менш глобального мінімума
    res = []
    min_y = 100500
    n = len(list_of_lamps)

    # проходимо по всіх лампах
    for i in range(n):
        start_alpha = np.pi * 2 * i / n   # кут альфа змінюється від 0 до 2pi з кроком 2pi/n

        # обчислюємо стартові координати робота з заданим кутом
        start_x1 = list_of_lamps[i][0] - list_of_dxdy[i][0] * np.cos(start_alpha) \
                   + list_of_dxdy[i][1] * np.sin(start_alpha)

        start_x2 = list_of_lamps[i][1] - list_of_dxdy[i][0] * np.sin(start_alpha) \
                   - list_of_dxdy[i][1] * np.cos(start_alpha)

        # мінімізуємо функцію методом градієнтного спуску з цими стартовими координатами
        tmp_res = grad_meth(Function(_tmp_func), np.array((start_x1, start_x2, start_alpha)), 0.2, t=-1)
        # перевіряємо, чи знайшли менший локальний мінімум
        tmp = _tmp_func(tmp_res[0], tmp_res[1], tmp_res[2])
        if tmp < min_y:
            min_y = tmp
            res = tmp_res
    return res


if __name__ == '__main__':
    LAMPS_AMOUNT = 30

    print("\n-----------------------------easy_robot-----------------------------------")
    real_coord = [(random.uniform(0, 100), random.uniform(0, 100)) for i in range(LAMPS_AMOUNT)]
    real_pos = (random.uniform(0, 100), random.uniform(0, 100))
    fault_dim = [(x - real_pos[0] + random.uniform(-0.5, 0.5),
                  y - real_pos[1] + random.uniform(-0.5, 0.5)) for x, y in real_coord]

    test_pos = find_robot(real_coord, fault_dim)
    test_pos2 = find_robot2(real_coord, fault_dim)
    print('lamps: ', real_coord)
    print('real position: ', real_pos)
    print('result position by first method (x, y): ', test_pos)
    print("result position by second method (x, y, alpha): ", test_pos2)
    print("\n-----------------------------medium_robot-----------------------------------")
    real_angle = random.uniform(-np.pi, np.pi)
    im_coord = [(random.uniform(0, 100), random.uniform(0, 100)) for i in range(LAMPS_AMOUNT)]

    real_coord = [(x * np.cos(real_angle) - y * np.sin(real_angle) + real_pos[0],
                   x * np.sin(real_angle) + y * np.cos(real_angle) + real_pos[1]) for x, y in im_coord]

    res_x, res_y, res_alpha = find_robot2(real_coord, im_coord)

    print('lamps: ', real_coord)
    print("real position: ", real_pos)
    print("real alpha: ", real_angle)
    print('result position: ', (res_x, res_y))
    print('result alpha: ', res_alpha)
