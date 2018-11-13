#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""
модуль з реалізованим класом функції багатьох змінних
"""

# TODO зробити метод знаходження похідної за напрямом
# TODO перетворити рекурсивну функцію знаходження похідної старшого порядку
# TODO в динаміку (через піраміду похідних)

import inspect
from itertools import product
import functools
from collections import Counter


class HashableCounter(Counter):
    """
    Мультимножина на базі Counter, яка хешується (для кешування)
    """
    def __hash__(self):
        return hash(str(self))


def cache(func):
    """
    декоратор кешування
    :param func: функціональний тип
    :return: змінена функція
    """
    results = {}

    @functools.wraps(func)
    def __cache(*args):
        nonlocal results
        if args in results.keys():
            # print("{} - взято з кеша".format(args))
            rez = results[args]
        else:
            rez = func(*args)
            results[args] = rez
        return rez

    return __cache


@cache
def factorial(n):
    """
    функція обчислення факторіала
    :param n: ціле число
    :return: ціле число
    """
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


@cache
def count_of_permute_with_replacement(num_list: tuple):
    """
    функція підрахунку к-ті перестановок з повторами для заданого списку
    (просто реалізація комбінаторної формули)

    :param num_list: кортеж (для можливості кешування)
    :return: ціле число
    """
    n = len(num_list)
    tmp = HashableCounter(num_list)
    res = factorial(n)
    for i in tmp.values():
        res //= factorial(i)
    return res


class Function:
    """
    Функція багатьох змінних

    Клас для полегшення роботи з функціями багатьох змінних, зокрема знаходження часткових похідних в точці,
    похідних за напрямком, градієнтів і т.п.

    >>> f = Function(func=lambda a, b: a ** 2 + b ** 2, variables=['x1', 'x2'])
    >>> f([2, 2])     # значення функції в точці
    8
    >>> f.partial_derivative('x1', (1, 1))     # часткова похідна по x1 в точці [1, 1]
    2.0000000000000018
    >>> f.derivative(2, (1, 1))                # похідна 2-го порядку в точці [1, 1]
    [1.9999999998909779, -5.551115123125783e-11, -5.551115123125783e-11, 1.9999999998909779]
    """

    delta_x = 10e-4

    def __init__(self, func, variables=None):
        """Створення об'єкту класу 'Функція багатьох змінних'.
        Параметри, які характеризують функцію: список з n імен змінних і функція, яка
        приймає на вхід n числових аргументів, а повертає число

        >>> def func(x1, x2):     # функція від 2-х змінних, яка повертає число
        ...      return x1 + x2
        ...

        >>> f1 = Function(func, variables=['x', 'y'])   # об'єкт класу 'функція', з змінними х1 і х2

        >>> f2 = Function(func)    # якщо variables не вказаний, то імена змінних автоматично стають виду хі

        :param variables: список рядків
        :param func: функціональний тип
        """
        assert isinstance(variables, list) or variables is None, "неправильний тип змінних"
        if variables is not None:
            for el in variables:
                assert isinstance(el, str), "неправильний тип змінних"

            self._var = variables
        else:
            self._var = None
            self._create_variables(func)
        self._func = func

    def _create_variables(self, func):
        """
        створення списку змінних за угодою (х1, х2, х3 ... хn)
        :param func: функція, яка приймає на вхід n позиційних змінних
        """
        self._var = []
        for i in range(len(inspect.getfullargspec(func).args)):
            self._var.append('x' + str(i + 1))

    @cache
    def partial_derivative(self, variable: str, x0: tuple, func=None) -> float:
        """
        знаходження значення часткової похідної в точці за означенням, без пошуку ліміта
        (використовючи симетричну ітеративну форму)

        метод використовує кешування

        :param variable: рядок, в якому ім'я змінної, по якій береться похідна
        :param x0: точка (вектор чисел)
        :param func: функція від якої береться похідна (опціонально)
        :return: число
        """
        assert variable in self._var, "ім'я змінної має бути у списку імен"
        assert len(x0) == len(self._var), "розмірність вектора має дорівнювати к-ті змінних"

        n = self._var.index(variable)   # позиція змінної в списку імен змінних
        tmp_x1 = list(x0)
        tmp_x1[n] += self.delta_x     # значення ф-ції в точці x + delta
        tmp_x2 = list(x0)
        tmp_x2[n] -= self.delta_x     # значення ф-ції в точці x - delta

        # якщо функція не вказана - беремо від внутрішньої
        if func is not None:
            res = (func(*tuple(tmp_x1)) - func(*tuple(tmp_x2))) / (self.delta_x * 2)
        else:
            res = (self._func(*tuple(tmp_x1)) - self._func(*tuple(tmp_x2))) / (self.delta_x * 2)
        return res

    @cache
    def _partial_derivative_n(self, n: int, variables: HashableCounter, x0: tuple) -> float:
        """
        Знаходження часткової похідної n-го порядку в точці.
        Функція рекурсивна і використовує кешування, а оскільки часткові похідні не залежать
        від порядку змінних, по яких вони беруться, параметр variables є мультимножиною

        :param n: порядок похідної
        :param variables: мультимножина (Counter, що хешується) змінних
        :param x0: вектор чисел (точка)
        :return: число
        """
        if n == 1:         # якщо похідна першого порядку - вертаємо часткову похідну
            return self.partial_derivative(next(variables.elements()), x0)

        var = next(variables.elements())   # вибираємо змінну з мультимножини
        variables[var] -= 1
        if variables[var] == 0:
            del variables[var]

        def tmp_func(*args):         # функція, яка рекурсивно вертає значення похідної (n-1)-го порядку
            return self._partial_derivative_n(n-1, variables, args)

        # знаходимо часткову похідну по вибраній змінній від тимчасової функції
        res = self.partial_derivative(var, x0, tmp_func)
        if var in variables:
            variables[var] += 1
        else:
            variables[var] = 1
        return res

    def partial_derivative_n(self, n: int, variables: list, x0: tuple) -> float:
        """
        Знаходження часткової похідної n-го порядку в точці.
        Викликає рекурсивну функцію _partial_derivative_n

        :param n: порядок похідної
        :param variables: список змінних, по яких береться похідна
        :param x0: точка (кортеж чисел)
        :return: дійсне число
        """
        # перевірка коректності введених даних
        assert 1 <= n, "неправильний тип порядку"
        assert len(list(variables)) == n, "розмірність вектора має дорівнювати к-ті змінних"
        assert len(x0) == len(self._var)
        for var in variables:
            assert isinstance(var, str), "неправильний тип змінної"

        # список змінних переводиться в Counter з хешуванням
        return self._partial_derivative_n(n, HashableCounter(variables), x0)

    @cache
    def derivative(self, n: int, x0: tuple) -> list:
        """
        Знаходження похідної функції (градієнта) n-го порядку
        Поки не придумав, як розміщувати відповідні часткові похідні у правильних позиціях
        n-вимірної матриці, тому покищо ця функція вертає просто список всіх часткових похідних

        :param n: порядок похідної
        :param x0: точка (кортеж чисел)
        :return: список дійсних чисел
        """
        assert 1 <= n, 'не коректний порядок похідної'
        assert len(x0) == len(self._var), 'розмірність вектора має дорівнювати к-ті змінних'

        num_list = range(n + 1)          # послідовність натуральних чисел
        res = []
        # проходимо по всіх виборках з повторами довжини == к-ть змінних
        for num_permute in product(num_list, repeat=len(self._var)):

            if sum(num_permute) != n:  # сума елементів вибірки має дорівнювати n
                continue

            tmp_variables = []
            # вибірка однозначно задає список змінних, для яких береться похідна
            for i, el in enumerate(num_permute):
                tmp_variables += [self._var[i]] * el

            # підрахунок к-ті всіх можливих перестановок нашого списку змінних
            count = count_of_permute_with_replacement(tuple(tmp_variables))
            # додаємо до нашого списку count часткових похідних
            res += [self.partial_derivative_n(n, tmp_variables, x0)] * count
        return res

    @property
    def variables(self):
        return self._var

    def __call__(self, iterable):
        """
        знаходження значення функції в точці
        :param iterable: об'єкт, що ітерується
        :return: дійсне число
        """
        assert len(iterable) == len(self._var), "розмірність вектора має дорівнювати к-ті змінних"
        return self._func(*tuple(iterable))

    def __repr__(self):
        return 'Function({})'.format(self._func.__doc__.strip())

    def __str__(self):
        return 'Function({})'.format(self._func.__doc__.strip())


def taylor_formula(func: Function, n: int, x0: tuple, x: tuple) -> Function:
    """
    Універсальна формула Тейлора для функції func, з n доданків, в точці x0

    >>> test_func = Function(lambda a, b: a ** 4 + b ** 4, variables=['x1', 'x2'])
    >>> test_func([2, 2])      # значення ф-ції в точці
    32
    >>> taylor_formula(test_func, 4, (1.9, 1.9), (2, 2))    # значення ф-ції в точці через формулу тейлора до 4 доданка
    31.9998016013903

    :param func: функція, для якої обчислюється ряд Тейлора
    :param n: к-ть додатнків
    :param x0: нульова точка
    :param x: точка, в якій знаходиться значення
    :return: дійсне число
    """

    res = func(x0)
    for i in range(1, n):         # цикл по доданкам
        factor = factorial(i)     # факторіал
        tmp_add = _taylor_addition(func, i, x0, x)    # обчислюємо і-ий доданок
        res += tmp_add / factor
    return res


def _taylor_addition(func: Function, addition_numb: int, x0: tuple, x: tuple) -> float:
    """
    обчислення і-ого доданка в формулі Тейлора

    :param func: функція, для якої обчислюється ряд Тейлора
    :param addition_numb: номер доданку
    :param x0: нульова точка
    :param x: точка, в якій знаходиться значення
    :return: дійсне число
    """
    res = 0
    # проходимо по всіх вибірках з повторами довжини == к-ть змінних
    # з послідовності натуральних чисел від 0 до addition_number
    for permute in product(range(addition_numb + 1), repeat=len(func._var)):
        # сума елементів вибірки має дорівнювати addition_number
        if sum(permute) != addition_numb:
            continue
        a = 1
        tmp_variables = []

        # вибірка однозначно задає послідовність змінних, по яких береться похідна
        for index, el in enumerate(permute):
            tmp_variables += [func._var[index]] * el   # будуємо послідовність змінних
            a *= (x[index] - x0[index]) ** el          # обчислюємо a для заданої часткової похідної
        # к-ть можливих перестановок даної послідовності
        count = count_of_permute_with_replacement(tuple(tmp_variables))
        res += a * (count * func.partial_derivative_n(addition_numb, tmp_variables, x0))
    return res
