#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from collections import defaultdict
import time
import numpy as np


class Polynome(defaultdict):
    """
    Даний клас реалізує дії над поліномами.

    Поліном представлений у вигляді словника.
    Степінь - ключ, коефіцієнт - значення.
    Зберігаються тільки степені з ненульовими коефіцієнтами.

    Методи:
    input() -> Polynome - Введення поліному з клавіатури.
    fromstring(s) -> Polynome - Перетворення рядка у поліном.
        Рядок повинен мати вигляд (наприклад):
        3.7*x**3 + 0.3*x**1 + -1.2*x**0
    __str__() - Повернути поліном у вигляді рядка.
        Рядок буде мати вигляд (наприклад):
        3.7*x**3 + 0.3*x**1 + -1.2*x**0
    __call__(x) -> float - Значення поліному у точці x.
    __add__(other) -> Polynome - Сума поліномів self + other.
    __radd__(other) -> Polynome - Сума поліномів other + self.
    __sub__(other) -> dict - Різниця поліномів self - other.
    __rsub__(other) -> dict - Різниця поліномів other - self.
    __mul__(other) -> Polynome - Добуток поліномів self * other.
    __rmul__(other) -> Polynome - Добуток поліномів other * self.
    deriv(n = 1) -> dict - n-та похідна поліному self.
    add_monom(deg, coeff) -> None - Додати одночлен
    get_degree() -> int - Повернути степінь поліному
    """

    def __init__(self, **kwargs):
        defaultdict.__init__(self, float, **kwargs)

    def fromstring(s):
        """
        Перетворення рядка у поліном.

        Рядок повинен мати вигляд (наприклад):

        3.7*x**3 + 0.3*x**1 + -1.2*x**0

        Пробіли між коефіцієнтами та степенями не допускаються.
        Від'ємні коефіцієнти записувати як у прикладі вище.
        :param s: рядок
        :return: об'єкт класу Polynome
        """
        p = Polynome()
        s = s.replace('+', ' ')
        ls = s.split()  # розбиваємо на список одночленів
        for m in ls:
            c = m.split('*x**')  # виділяємо степінь та коефіцієнт
            k = int(c[1])
            v = float(c[0])
            p[k] = v
        return p

    fromstring = staticmethod(fromstring)

    def add_monom(self, deg, coeff):
        """
        Додати одночлен степені deg до поліному.
        :param deg: степінь одночлена
        :param coeff: коефіцієнт одночлена
        :return: None
        """
        if coeff != 0:
            self[deg] += coeff

    def get_degree(self):
        """
        Метод повертає степінь поліному
        :return: степінь полінома (int)
        """
        return max(self)

    def __str__(self):
        """
        Повернути рядок, який є зовнішнім представленням поліному.

        Рядок буде мати вигляд (наприклад):
        3.7*x**3 + 0.3*x**1 + -1.2*x**0
        :return: рядок
        """
        monomials = list(self.items())
        if not monomials:
            poly_str = "0.0*x**0"
        else:
            # Впорядковуємо за спаданням степенів
            monomials.sort(reverse=True)
            ls = ["{}*x**{}".format(mono[1], mono[0]) for mono in monomials]
            poly_str = ' + '.join(ls)
        return poly_str

    def __call__(self, x):
        """
        Значення поліному у точці x.

        :param x: дійсне число
        :return: значення поліному у точці x (дійсне)
        """
        return sum([self[k]*x**k for k in self])

    def __add__(self, other):
        """
        Сума поліномів self + other.
        :param other: поліном
        :return: об'єкт класу Polynome
        """
        p = Polynome()
        # утворюємо множину, що містить всі ключі self та other
        keys = set(self.keys()) | set(other.keys())
        for k in keys:
            p[k] = self[k] + other[k]
        return self._delzeroes(p)

    def __radd__(self, other):
        """
        Сума поліномів other + self.
        :param other:
        :return: об'єкт класу Polynome
        """
        return self.__add__(other)

    def __sub__(self, other):
        """
        Різниця поліномів self - other.
        :param other: поліном
        :return: об'єкт класу Polynome
        """
        p = Polynome()
        keys = set(self.keys()) | set(other.keys())
        for k in keys:
            p[k] = self[k] - other[k]
        return self._delzeroes(p)

    def __rsub__(self, other):
        """
        Різниця поліномів other - self.
        :param other: поліном
        :return: об'єкт класу Polynome
        """
        p = Polynome()
        keys = set(self.keys()) | set(other.keys())
        for k in keys:
            p[k] = other[k] - self[k]
        return self._delzeroes(p)

    def __mul__(self, other):
        """
        Добуток поліномів self * other.
        :param other: поліном
        :return: об'єкт класу Polynome
        """
        p = Polynome()
        for k1 in self:
            for k2 in other:
                p[k1 + k2] += self[k1] * other[k2]
        return self._delzeroes(p)

    def __rmul__(self, other):
        """
        Добуток поліномів other * self.
        :param other: поліном
        :return: об'єкт класу Polynome
        """
        return self.__rmul__(other)

    def deriv(self, n=1):
        """
        n-та похідна поліному self.

        Якщо n не вказано, то перша похідна
        :param n: порядок похідної
        :return: об'єкт класу Polynome
        """
        p = self
        for i in range(n):
            p = self._deriv(p)
        return self._delzeroes(p)

    @staticmethod
    def _deriv(p):
        """
        Перша похідна поліному p.

        :return: об'єкт класу Polynome
        """
        pp = Polynome()
        for k in p:
            if k != 0:
                pp[k - 1] = p[k] * k
        return pp

    @staticmethod
    def _delzeroes(p):
        """
        Повертає копію p без нульових елементів.

        Якщо всі нулі, то повертає поліном 0*x**0.
        :param p: об'єкт класу Polynome
        :return: об'єкт класу Polynome
        """
        pp = Polynome()
        for k in p:
            if p[k] != 0:
                pp[k] = p[k]
        return pp


def directFourierTransform(f: list) -> list:
    return [sum([f[k] * np.exp(-2*complex(0, 1)*np.pi*k*n/len(f)) for k in range(len(f))]) for n in range(len(f))]


def inverseFourierTransform(g: list) -> list:
    return [sum([g[k]*np.exp(2*complex(0, 1)*np.pi*k*n/len(g)) for k in range(len(g))])/len(g) for n in range(len(g))]


def transform(f: list) -> list:
    return [round(f[i].real) for i in range(len(f))]


if __name__ == '__main__':
    # task 1

    print('task 1\n')

    p1 = Polynome()
    p2 = Polynome()
    a = []
    b = []
    n = 100
    for i in range(n):
        p1.add_monom(i, i+1)
        a.append(i+1)
        p2.add_monom(i, n-i)
        b.append(n-i)
    print(f'P(x) = {p1}')
    print(f'Q(x) = {p2}')
    print('перемножим явно:')
    t_start = time.time()
    print(p1*p2)
    t_end = time.time()
    print(f'времени потрачено: {t_end - t_start}\n')
    del t_start, t_end

    print('через дискретное преборазование Фурье: ')
    t_start = time.time()
    print(f'a = {a}')
    print(f'b = {b}')

    # дополним нулями наборы a и b до степеня произведения (198)
    while not (len(a) == len(b) == 199):
        a.append(0)
        b.append(0)

    gn_a = directFourierTransform(a)  # прямое преобразование для а
    gn_b = directFourierTransform(b)  # прмое преобразование для b

    gn_c = [gn_a[i] * gn_b[i] for i in range(len(gn_a))]  # набор коэффицентов произведения
    fn_c = transform(inverseFourierTransform(gn_c))  # обратное для произведения
    print(f'\nРезультат:\n{fn_c}')
    t_end = time.time()
    print(f'времени потрачено: {t_end - t_start}\n')
    del t_start, t_end, gn_a, gn_b, gn_c

    # task 2
    print('task 2\n')

    print('через дискретное преобразование Фурье:\n')
    t_start = time.time()
    p3 = Polynome()
    for i in enumerate(fn_c):
        p3.add_monom(i[0], i[1])
    print(f'полином : {p3}')
    print(f'полином в точке x = 10 : {p3(10)}')
    t_end = time.time()
    print(f'времени потрачено: {t_end - t_start}\n')

    print('через быстрое дискретное преобразование Фурье:\n')
    # по аналогии с 1

    del fn_c, t_start, t_end, p3

    t_start = time.time()
    gn_a = np.fft.fft(a)
    gn_b = np.fft.fft(b)
    gn_c = [gn_a[i] * gn_b[i] for i in range(len(gn_a))]
    fn_c = transform(np.fft.ifft(gn_c))
    p3 = Polynome()
    for i in enumerate(fn_c):
        p3.add_monom(i[0], i[1])
    print(f'полином : {p3}')
    print(f'полином в точке x = 10 : {p3(10)}')
    t_end = time.time()
    print(f'времени потрачено: {t_end - t_start}\n')

    del fn_c, t_start, t_end, p3, n, a, b, p1, p2

    # task 3
    print('task 3\n')

    a1 = []
    b1 = []
    a2 = []
    b2 = []
    n1 = 1000
    n2 = 10000
    for i in range(n1):
        a1.append(i + 1)
        b1.append(n1 - i)
    for i in range(n2):
        a2.append(i + 1)
        b2.append(n2 - i)

    print(f'n = {n1}\n')
    print('через дискретное преборазование Фурье: ')
    t_start = time.time()
    print(f'a1 = {a1}')
    print(f'b1 = {b1}')

    # дополним нулями наборы a и b до степеня произведения (198)
    while not (len(a1) == len(b1) == 2 * n1 - 1):
        a1.append(0)
        b1.append(0)

    gn_a = directFourierTransform(a1)  # прямое преобразование для а
    gn_b = directFourierTransform(b1)  # прмое преобразование для b

    gn_c = [gn_a[i] * gn_b[i] for i in range(len(gn_a))]  # набор коэффицентов произведения
    fn_c = transform(inverseFourierTransform(gn_c))  # обратное для произведения
    print(f'\nРезультат:\n{fn_c}')
    t_end = time.time()
    print(f'времени потрачено: {t_end - t_start}\n')

    del gn_c, gn_b, gn_a, t_end, t_start, fn_c

    print('через быстрое дискретное преобразование Фурье:\n')

    t_start = time.time()
    gn_a = np.fft.fft(a1)
    gn_b = np.fft.fft(b1)
    gn_c = [gn_a[i] * gn_b[i] for i in range(len(gn_a))]
    fn_c = transform(np.fft.ifft(gn_c))
    p3 = Polynome()
    for i in enumerate(fn_c):
        p3.add_monom(i[0], i[1])
    print(f'полином : {p3}')
    t_end = time.time()
    print(f'времени потрачено: {t_end - t_start}\n')

    del gn_c, gn_b, gn_a, t_end, t_start, fn_c

    # n = 10000

    print(f'n = {n2}')

    print('через дискретное преборазование Фурье: ')
    t_start = time.time()
    print(f'a1 = {a2}')
    print(f'b1 = {b2}')

    # дополним нулями наборы a и b до степеня произведения (198)
    while not (len(a2) == len(b2) == 2 * n2 - 1):
        a1.append(0)
        b1.append(0)

    gn_a = directFourierTransform(a2)  # прямое преобразование для а
    gn_b = directFourierTransform(b2)  # прмое преобразование для b

    gn_c = [gn_a[i] * gn_b[i] for i in range(len(gn_a))]  # набор коэффицентов произведения
    fn_c = transform(inverseFourierTransform(gn_c))  # обратное для произведения
    print(f'\nРезультат:\n{fn_c}')
    t_end = time.time()
    print(f'времени потрачено: {t_end - t_start}\n')

    del gn_c, gn_b, gn_a, t_end, t_start, fn_c

    print('через быстрое дискретное преобразование Фурье:\n')

    t_start = time.time()
    gn_a = np.fft.fft(a2)
    gn_b = np.fft.fft(b2)
    gn_c = [gn_a[i] * gn_b[i] for i in range(len(gn_a))]
    fn_c = transform(np.fft.ifft(gn_c))
    p3 = Polynome()
    for i in enumerate(fn_c):
        p3.add_monom(i[0], i[1])
    print(f'полином : {p3}')
    t_end = time.time()
    print(f'времени потрачено: {t_end - t_start}\n')

    del gn_c, gn_b, gn_a, t_end, t_start, fn_c