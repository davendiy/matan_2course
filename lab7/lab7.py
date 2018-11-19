#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import numpy as np
from dop_classes.multydimensional import cache
import time


def fdt(f: np.ndarray):
    """ Дискретне перетворення Фур'є

    :param f: набір значень функції
    :return: набір значень перетворення Фур'є
    """
    length = len(f)
    res = np.array([complex(0, 0)] * length)  # створюємо масив довжини n
    for n in range(length):  # заповняємо його по формулі
        res[n] = sum([f[k] * cycle_exp(k * n, length) for k in range(length)])
    return res


def inverse_fdf(g: np.ndarray):
    """ Обернене перетворення Фур'є

    :param g: набір значень перетворення Фур'є
    :return: набір значень функції
    """
    length = len(g)
    res = np.array([complex(0, 0)] * length)
    for n in range(length):  # аналогічно заповнюємо масив по формулі
        res[n] = sum([g[k] * cycle_exp(-k * n, length) for k in range(length)])
    return res / length


def cycle_exp(k, n):
    """ Функція обчислення k-го кореня n-го степеня з 1
        Викликає функцію з кешуванням після зміщення k.
        Оскільки _cycle_exp кешується, то в пам'яті зберігається всього n/2 значень
    """
    k %= n  # обчислюємо остачу
    if k > n / 2:  # якщо кут > pi, то можна обчислити для кута (2pi - кут) і знайти до нього спряжений
        return _cycle_exp(n - k, n).conjugate()
    else:
        return _cycle_exp(k, n)  # інакше просто викликаємо


@cache
def _cycle_exp(k, n) -> complex:
    """ Функція з кешуванням, яка просто обчислює корінь по формулі
    """
    return np.exp(-2 * complex(0, 1) * np.pi * k / n)


def fast_fdf(fn: np.ndarray):
    """ Моя спроба реалізувати швидке перетворення Фур'є.
        Функція підготовлює масив значень fn і викликає рекурсивну
        функцію _ffdf_helper

    :param fn: масив значень функції
    :return: масив значень перетворення
    """
    n = len(fn)
    tmp = 1
    for i in range(n):  # знаходимо степінь двійки, який на числовій осі зразу після довжини масиву
        if tmp > n:
            break
        tmp *= 2

    # заповнюємо масив нулями
    fn = np.array(list(fn) + [0] * (tmp - n))
    res = _ffdf_helper(fn, n, 0, 1)
    return res


def _ffdf_helper(fn: np.ndarray, n: int, start: int, k: int) -> np.ndarray:
    """ Рекурсивна функція реалізації швидкого перетворення Фур'є
        Розбиття масиву на частини відбувається шляхом збільшення кроку, з яким
        ітерується масив, тому нові масиви створюються тільки на найнижчому рівні.
        Наче зробив все, як ви сказали, але шось видає хибні значення.

    :param fn: масив значень функції
    :param n: к-ть значень (довжина масиву, щоб кожного разу її не рахувати)
    :param start: початковий індекс (з якого починається підпослідовність)
    :param k: крок, з яким ітерується
    :return: масив значень перетворення
    """
    if n // k <= 3:  # якщо довжина підпослідовності <= 3, то рахуємо в лоб
        return fdt(fn[start::k])  # ось тут тільки створюється новий масив

    else:
        # інакше обчислюємо окремо перетворення Фур'є для обох підпослідовностей
        gk1 = _ffdf_helper(fn, n, start, k * 2)  # індекси змінюються з кроком k * 2, починаючи з start
        gk2 = _ffdf_helper(fn, n, start + k, k * 2)  # індекси змінюються з кроком k * 2, починаючи з start+k

        gk1 = np.array(list(gk1) * 2)  # дублюємо масиви
        gk2 = np.array(list(gk2) * 2)

        # за формулою обчислюємо наступну ітерацію
        res = np.array([gk1[i] + cycle_exp(i, n) * gk2[i] for i in range(len(gk1))])
        return res


def ft_polynom_mult(coeffs1: list, coeffs2: list):
    """ Функція, яка перемножає 2 поліноми, використовуючи дискретне
        перетворення Фур'є

    :param coeffs1: список коефіцієнтів 1-го многочлена
    :param coeffs2: список коефіцієнтів 2-го многочлена
    :return: масив коефіцієнтів добутку
    """
    n = len(coeffs1) + len(coeffs2)  # степінь добутку
    coeffs1 = np.array(coeffs1 + [0] * (n - len(coeffs1)))  # дописуємо необхіду к-ть нулів до кожного списку
    coeffs2 = np.array(coeffs2 + [0] * (n - len(coeffs2)))

    ft_coeff1 = fdt(coeffs1)  # пряме перетворення Фур'є
    ft_coeff2 = fdt(coeffs2)

    ft_res = ft_coeff1 * ft_coeff2  # поточково перемножаємо
    res = inverse_fdf(ft_res)  # обернене перетворення Фур'є
    return transform(res)


def fft_polynom_mult(coeffs1: list, coeffs2: list):
    """ Аналогічна функція, яка перемножає 2 поліноми, використовуючи швидке перетворення
        Фур'є. Використовував numpy функцію, т.к. моя видає неправильні результати.

    :param coeffs1: список коефіцієнтів першого полінома
    :param coeffs2: список коефіцієнтів другого полінома
    :return: масив коефіцієнтів добутку
    """
    n = (len(coeffs2) + len(coeffs1))
    coeffs1 = np.array(coeffs1 + [0] * (n - len(coeffs1)))
    coeffs2 = np.array(coeffs2 + [0] * (n - len(coeffs2)))

    ft_coeff1 = np.fft.fft(coeffs1)  # все те саме, тільки використовуємо швидке перетворення Фур'є
    ft_coeff2 = np.fft.fft(coeffs2)

    ft_res = ft_coeff1 * ft_coeff2
    res = np.fft.ifft(ft_res)
    return transform(res)


def ft_long_numbers(numb1, numb2, mult_func=fft_polynom_mult):
    """ Множення довгих чисел

    :param numb1: 1-ше число
    :param numb2: 2-ге число
    :param mult_func: функція, яка перемножає многочлени
    :return: добуток
    """
    list1 = list(map(int, str(numb1)))  # список коефіцієнтів многочлена, який задає 1-ше число
    list2 = list(map(int, str(numb2)))  # список коефіцієнтів многочлена, який задає 2-ге число

    res_list = mult_func(list1, list2)  # перемножаємо 2 многочлена

    res = 0
    dec = 1
    for el in res_list:  # отримуємо значення многочлена в точці 10
        res += int(el) * dec
        dec *= 10
    return res


def transform(f) -> np.ndarray:
    """ Округляє значення масиву f
    """
    return np.array([round(f[i].real) for i in range(len(f))])


if __name__ == '__main__':

    # ----------------------------------task 1-------------------------------------------------------
    poly1 = list(range(1, 101))
    poly2 = list(range(100, 0, -1))
    test_poly1 = np.polynomial.Polynomial(poly1)
    test_poly2 = np.polynomial.Polynomial(poly2)
    my_res1 = ft_polynom_mult(poly1, poly2)
    my_res2 = fft_polynom_mult(poly1, poly2)
    print("\n\ntask 1")

    print(f'\nstandard polynoms multiplication (numpy): \n{test_poly1 * test_poly2}')
    print(f'\nmultiplication with my Fouirer transform: \n{my_res1} ')
    print(f'\nmultiplication with numpy fast Fouirer transfotm: \n{my_res2}')

    # ----------------------------------task 2-------------------------------------------------------
    a = ''.join(map(str, range(1, 101)))
    b = ''.join(map(str, range(100, 0, -1)))

    rez = np.polynomial.Polynomial(list(map(int, a))) * \
          np.polynomial.Polynomial(list(map(int, b)))

    print("\n\ntask 2")
    print(f"\nstandart python multiplication: \n{int(a) * int(b)}")
    print(f'\nmultiplication using standard numpy polynomial multiplication: \n{rez(10)}')
    print(f'\nmultiplicaion using my poly mult with FFT: \n{ft_long_numbers(a, b)}')

    # ----------------------------------task 3-------------------------------------------------------

    print('\n\ntask3')
    for test_n in [100, 1000, 10000]:
        poly1 = list(range(1, test_n + 1))
        poly2 = list(range(test_n, 0, -1))
        _poly1 = np.polynomial.Polynomial(poly1)
        _poly2 = np.polynomial.Polynomial(poly2)

        t = time.time()
        _poly1 * _poly2
        print(f"n = {test_n}, time for standard numpy multiplication: {time.time() - t}")

        t = time.time()
        # ft_polynom_mult(poly1, poly2)
        print(f"n = {test_n}, time for FT multiplication: {time.time() - t}")

        t = time.time()
        fft_polynom_mult(poly1, poly2)
        print(f"n = {test_n}, time for FFT multiplication: {time.time() - t}")
