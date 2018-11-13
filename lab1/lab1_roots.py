#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import math


# -------------------------------------функції з завдання---------------------------------------------------------------
def f1(x):
    return x ** 10 - 0.1 * x - 0.01


def f2(x):
    return 6 * math.sin(x ** 7) + x ** 21 - 6 * x ** 14


# -------------------------кортеж з функціями і відповідними межами інтегрування---------------------------------------
LIST_OF_FUNCTIONS = ((f1, (0, 1)),
                     (f2, (-0.4, 0.6)),
                     (f2, (-1.5, 1.6)))


def derivative(func, x0, dx):
    """
    функція обчислення похідної в точці (симетричний спосіб)
    :param func: функціональний тип
    :param x0: дійсне число (точка)
    :param dx: дійсне число
    :return: дійсне число
    """
    return (func(x0 + dx) - func(x0 - dx)) / (2 * dx)


def half_division_method(func, a, b, eps):
    """
    знаходження нуля функції методом половинного поділу
    :param func: функціональний тип даних
    :param a: ліва межа
    :param b: права межа
    :param eps: епсилон
    :return: кортеж(f(x), x)
    """
    y1 = func(b)
    tmp_y = func(a)
    tmp_x = a

    # якщо кінці функції знаходяться по одну сторону від осі ох
    if y1 * tmp_y > 0:
        return None

    # продовжуємо ділити відрізок посередині, поки значення функції не буде менше епсилон
    while abs(tmp_y) > eps:
        tmp_x = (a + b) / 2   # середина відрізка
        tmp_y = func(tmp_x)   # значення функції в середині
        if tmp_y * y1 < 0:
            a = tmp_x         # вибір правильного кінця
        else:
            b = tmp_x
            y1 = tmp_y
    return tmp_y, tmp_x


def method_of_secants(func, a, b, eps):
    """
    знаходження нулів функції методом січних
    :param func: функціональний тип даних
    :param a: ліва межа#!/usr/bin/env python3
    :param b: права межа
    :param eps: епсилон
    :return: кортеж(f(x), x)
    """
    x0 = a
    x1 = b
    tmp_y = func(a)
    i = 0
    while abs(tmp_y) > eps:    # продовжуємо поки значення ф-ції в точці > епсилон
        func_x1 = func(x1)
        tmp_x = x1
        x1 = x1 - func_x1 * (x1 - x0) / (func_x1 - func(x0))
        x0 = tmp_x
        tmp_y = func(tmp_x)

        i += 1              # додаткова умова виходу з циклу у випадку відсутності нуля
        if i > 100000:
            return None
    return tmp_y, x1


def method_of_tangents(func, a, b, eps):
    """
    знаходження нуля функції методом дотичних
    :param func: функціональний тип даних
    :param a: ліва межа
    :param b: права межа
    :param eps: епсилон
    :return: кортеж(f(x), x)
    """
    xn = b
    tmp_y = func(b)
    while abs(tmp_y) > eps:      # поки значення > епсилон, а абсциса більша ніж ліва межа
        xn = xn - tmp_y / derivative(func, xn, 0.0001)
        tmp_y = func(xn)

        if xn < a:     # якщо виходимо за область визначення - зупиняємо цикл
            tmp_y = None
            xn = None
            break
    return tmp_y, xn


if __name__ == '__main__':

    with open('output_roots.txt', 'w', encoding='utf-8') as file:

        for f, (tmp_a, tmp_b) in LIST_OF_FUNCTIONS:
            file.write('\n\n' + f.__name__ + '[{}, {}]'.format(tmp_a, tmp_b))

            file.write('\nМетод половинного поділу:\n')
            file.write(str(half_division_method(f, tmp_a, tmp_b, 0.0001)))

            file.write('\nМетод січних:\n')
            file.write(str(method_of_secants(f, tmp_a, tmp_b, 0.0001)))

            file.write('\nМетод дотичних:\n')
            file.write(str(method_of_tangents(f, tmp_a, tmp_b, 0.0001)))
