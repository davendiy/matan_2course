#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from math import log, cos, sqrt
import numpy as np
import random


def derivative(func, x0, dx):
    """
    функція обчислення похідної в точці (симетричний спосіб)
    :param func: функціональний тип
    :param x0: дійсне число (точка)
    :param dx: дійсне число
    :return: дійсне число
    """
    return (func(x0 + dx) - func(x0 - dx)) / (2 * dx)


def f1(x):
    """
    функція для першого завдання
    """
    return 0.5 * cos(x)


def f2(x):
    """
    функція для другого завдання
    """
    return x ** 5 - x - 1


def norm(vector: np.ndarray):
    """
    норма вектора в евклідовому просторі
    """
    return sqrt(sum(vector.ravel() ** 2))


def find_root1(func, x0, lamb, eps):
    """
    знаходження розв'язку рівняння f(x) = x для f(x) = 0.5cos(x) за допомогою теореми Банаха

    lambda є [0.5, 1] => вибираємо lambda = 0.5 (перше завдання)

    :param func: функціональний тип
    :param x0: стартова точка
    :param lamb: лямбда
    :param eps: епсилон (точність)
    :return: корінь, мінімальна к-ть ітерацій
    """
    x1 = func(x0)
    if type(x0) in [np.array, np.matrix, np.ndarray]:
        m = (log(eps / norm(x1 - x0)) + log(1 - lamb)) / (log(lamb))
    else:
        m = (log(eps / abs(x1 - x0)) + log(1 - lamb)) / (log(lamb))
    x_m = x0
    for i in range(int(m) + 1):
        x_m = func(x_m)

    return x_m, int(m) + 1


def find_root2(func, m, x0):
    """
    знаходження розв'язку р-ння f(x) = 0 для f(x) = x ** 5 - x - 1 за допомогою теореми Банаха

    додаткова функція f_temp(x) = x - lambda * f(x). Для неї застосовуємо метод з першої функції, вважаючи,
    що lambda = 1 / (2 * M), де M - мінімальне число, яке більше за похідну f'(x) для всякого x є [a, b]

    :param func: функціональний тип
    :param m: дійсне число
    :param x0: початкова точка
    :return: результат
    """
    lamb1 = 1 / (2 * m)

    lamb2 = 1 - lamb1

    def f_tmp(x):                  # функція стиску, для якої шукаємо розв'язок f(x) = x
        return x - lamb1 * func(x)

    x_m, m = find_root1(f_tmp, x0, lamb2, 10 ** (-9))
    return x_m, m


def _check_convergence(a: np.array):
    """
    знаходить лямбда**2 для слр
    :param a: матриця коефіцієнтів
    :return: лямбда
    """
    e = np.eye(*a.shape)
    tmp_c = (a - e) ** 2
    lamb = sum(tmp_c.ravel())
    return lamb


def find_root_sle(a_matrix: np.array, b_matrix: np.array):
    """
    розв'язання слр за допомогою теореми Банаха
    :param a_matrix: матриця коефіцієнтів
    :param b_matrix: матриця вільних членів
    :return: вектор невідомих
    """

    def f_tmp(x):       # фунція стиску, для якої будемо розв'язувати рівняння f(x) = x
        rez = a_matrix.dot(x.transpose())
        rez = rez.ravel() - b_matrix.ravel() + x.ravel()
        return rez

    lamb = _check_convergence(a_matrix)    # знаходимо лямбда

    if 0 < lamb < 1:    # перевірка збіжності
        x0 = np.zeros(a_matrix.shape[0])        # перший вектор (рандомний)
        x0[0] = 1
        result = find_root1(f_tmp, x0, lamb, 10e-9)
    else:
        result = [None, None]
    return result


def create_random_matrix(n, m, start_range, end_range, equal=False):
    """
    створення матриці з рандомними елементами
    :param n: к-ть рядків
    :param m: к-ть стовпчиків
    :param start_range: ліва межа
    :param end_range: права межа
    :param equal: флаг {True - матриця з рівних елементів, False - матриця з різних елементів}
    :return: матриця розміру nxm
    """
    a = np.zeros((n, m))
    t = random.uniform(start_range, end_range)
    for i in range(n):
        for j in range(m):
            if equal:
                a[i, j] = t
            else:
                a[i, j] = random.uniform(start_range, end_range)
    return a


if __name__ == '__main__':
    print('завдання 1 (корінь, к-ть операцій):\n', find_root1(f1, -10, 0.5, 10 ** (-9)))
    print('завдання 2 (корінь, к-ть операцій):\n', find_root2(f2, 79, 0))

    A = create_random_matrix(10, 10, -0.05, 0.05) + np.eye(10, 10)
    B = create_random_matrix(1, 10, -10, 10)
    res = find_root_sle(A, B)

    print("завдання 3 (а):\n", res[0], '\nк-ть операцій: ', res[1])
    tmp = A.dot(res[0])

    A = create_random_matrix(80, 80, -0.01, 0.01, equal=True) + np.eye(80, 80)
    B = create_random_matrix(80, 1, -10, 10)
    res = find_root_sle(A, B)

    print("завдання 3 (б):\n", res[0], '\nк-ть операцій: ', res[1])
