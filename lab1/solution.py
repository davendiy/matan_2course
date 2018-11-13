#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""
Програма, яка розв'язує рівняння виду f(x) = g(x) в заданих межах

Користувач вводить рядок, в якому записане рівняння, вводить межі,
рядок перетворюється у функцію 'y = f(x) - g(x)', для якої шукаємо нулі
за допомогою методів з lab1_roots.

Дана програма є поганою з точки зору захищенності в стресовій ситуації, оскільки
користувач, по суті, вводить код програми, який потім запускається (хоч мінімальний захист і написаний)
"""

from math import *             # для генерування функцій
from lab1.lab1_roots import *


class ErrorBadEqual(Exception):
    """
    клас помилки для програми,
    викликається коли користувач ввів некоректне рівняння (нема '=', або після
    '=' нічого нема
    """

    def __str__(self):
        return 'некоректне рівняння'


def find_root(str_func, a, b):
    """
    функція знаходження кореня рівняння (тільки одного)

    :param str_func: рядок, який представляє собою функцію у пітонівській формі
    :param a: ліва межа області визначень
    :param b: права межа області визначень
    :return: дійсне число або None
    """

    def tmp_func(x):
        """
        генерується пітонівська функція на основі введеного рядка
        :param x: дійсне число
        :return: дійсне число
        """
        # рядок переводиться в програмний код (підхід максимально поганий, просто інший алгоритм довго реалізовувати)
        return eval(str_func)

    y1 = tmp_func(a)     # значення функції в країніх точках
    y2 = tmp_func(b)
    if y1 * y2 < 0:       # якщо значення по різні боки осі ох, то використовуємо
        rez = half_division_method(tmp_func, a, b, 0.0001)   # метод половинного поділу
    elif y1 * y2 > 0:
        rez = method_of_tangents(tmp_func, a, b, 0.0001)     # інакше - метод дотичних, а якщо він не дає результату
        if rez is None:
            rez = method_of_secants(tmp_func, a, b, 0.0001)  # то метод січних
    else:
        rez = a if y1 == 0 else b   # значення ф-ції == 0 в крайній точці, то виводимо крайню точку

    return rez


def parse_string(string: str):
    """
    функція, яка аналізує введений рядок користувача і переводить рівняння (якщо
    воно коректне) у функцію
    :param string: рядок виду 'f(x) = g(x)' пітонівським синтаксисом
    :return: перетворений рядок виду 'f(X) - (g(x))', щоб потім перетворити його у програмний код
    """
    string = string.split('=')  # розбиваємо рядок на два по знаку '='
    if len(string) == 2:
        string = '{} - ({})'.format(string[0], string[1])
    else:
        raise ErrorBadEqual     # якщо рядок не розбився, значить щось не так

    return string


if __name__ == '__main__':
    try:
        equal = input("введіть рівняння відносно змінної х (f(x) = g(x)) у пітонівській формі:\n--> ")
        start = float(input("межі функції:\na = "))
        end = float(input("b = "))
        equal = parse_string(equal)               # перетворюємо рядок
        res = find_root(equal, start, end)       # знаходимо корені
        if res is not None:
            res = res[1]
        print("результат:", res)
    except Exception as e:
        print('помилка:', str(ErrorBadEqual()), "({})".format(e))
