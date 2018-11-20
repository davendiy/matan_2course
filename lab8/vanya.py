import random
import numpy as np


def _test(func: list, dot):
    res = []
    for i in range(len(func)):
        res.append(func[i](dot))
    if not all(res):
        return False
    return True


def monte_carlo(func: list, limits: list, n):
    """
    Monte-carlo function
    :param func: list of functions
    :param limits: list of limits, of area
    :param n: number of iterations
    :return:
    """
    m_q = limits[0]
    for i in range(1, len(limits)):
        m_q *= limits[i]
    k = 0
    for i in range(n):
        tmp = [random.uniform(-limits[i] / 2, limits[i] / 2) for i in range(len(limits))]
        if _test(func, tmp):
            k += 1
    return k / n * m_q


def monte_carlo_integral(f: callable, func: list, limits: list, n):
    m_q = limits[0]
    for i in range(1, len(limits)):
        m_q *= limits[i]
    k = 0
    dots = []
    for i in range(n):
        tmp = [random.uniform(-limits[i] / 2, limits[i] / 2) for i in range(len(limits))]
        if _test(func, tmp):
            k += 1
            dots.append(tmp)
    res = 0
    for i in dots:
        res += f(i)
    return res / n * m_q


# -------------------------------------------------- Task 1 ------------------------------------------------------------
def task_1_1(n):
    func = lambda x: x[0] ** 4 + x[1] ** 4 <= 1
    tmp = 1 / 2 ** n
    # corners,center and its duplicates
    c_1, c_2, c_3, c_4, c_0 = [-1, 1], [-1 + tmp, 1], [-1 + tmp, 1 - tmp], [-1, 1 - tmp], [-1 + tmp / 2, 1 - tmp / 2]
    _c_1, _c_2, _c_3, _c_4, _c_0 = c_1[:], c_2[:], c_3[:], c_4[:], c_0[:]
    res_low = 0
    res_up = 0
    for i in range(2 ** (n + 1)):
        for j in range(2 ** (n + 1)):
            c_1[0] = c_1[0] + tmp
            c_2[0] = c_2[0] + tmp
            c_3[0] = c_3[0] + tmp
            c_4[0] = c_4[0] + tmp
            c_0[0] = c_0[0] + tmp
            ktp = [func(i) for i in [c_1, c_2, c_3, c_4, c_0]]
            if all(ktp):
                res_low += 1 / (2 ** (2 * n))
            if any(ktp):
                res_up += 1 / (2 ** (2 * n))

        c_1 = [_c_1[0], c_1[1] - tmp]
        c_2 = [_c_2[0], c_2[1] - tmp]
        c_3 = [_c_3[0], c_3[1] - tmp]
        c_4 = [_c_4[0], c_4[1] - tmp]
        c_0 = [_c_0[0], c_4[1] - tmp]

    return res_low, res_up


def task_1_2(n):
    func_1 = lambda x: x[0] ** 2 + x[1] ** 2 <= 1
    func_2 = lambda x: x[0] + x[1] <= x[2] <= 2 * x[1] + 3 * x[2]
    # x = [-1,1] , y[-1,1] , z = [-2 , 5]
    tmp = 1 / 2 ** n
    c_1 = [1, -1, 5]
    c_2 = [1 - tmp, -1, 5]
    c_3 = [1 - tmp, -1 + tmp, 5]
    c_4 = [1, -1 + tmp, 5]
    c_5 = [1, -1, 5 - tmp]
    c_6 = [1 - tmp, -1, 5 - tmp]
    c_7 = [1 - tmp, -1 + tmp, 5 - tmp]
    c_8 = [1, -1 + tmp, 5 - tmp]
    c_0 = [1 - tmp / 2, -1 + tmp / 2, 5 - tmp / 2]
    coords = [c_1, c_2, c_3, c_4, c_5, c_6, c_7, c_8, c_0]
    _c_1, _c_2, _c_3, _c_4, _c_5, _c_6, _c_7, _c_8, _c_0 = c_1[:], \
                                                           c_2[:], \
                                                           c_3[:], \
                                                           c_4[:], \
                                                           c_5[:], \
                                                           c_6[:], \
                                                           c_7[:], \
                                                           c_8[:], \
                                                           c_0[:]
    _coords = [_c_1, _c_2, _c_3, _c_4, _c_5, _c_6, _c_7, _c_8, _c_0]
    res_low = 0
    res_up = 0
    for z in range(8 ** (n + 1)):  # 32k iterations for n = 4
        for y in range(2 ** (n + 1)):
            for x in range(2 ** (n + 1)):
                for i in coords:
                    i[0] -= tmp
                ktp_1 = [func_1(x) for x in coords]
                ktp_2 = [func_2(x) for x in coords]
                if all(ktp_1) and all(ktp_2):
                    res_low += tmp ** 3
                if any(ktp_1) and any(ktp_2):
                    res_up += tmp ** 3
            for i in range(len(coords)):
                coords[i][0] = _coords[i][0]
                coords[i][1] += tmp
        for i in range(len(coords)):
            coords[i][0] = _coords[i][0]
            coords[i][1] = _coords[i][1]
            coords[i][2] -= tmp

    return res_low, res_up


# ------------------------------------------------- Task 2 -------------------------------------------------------------

def task_2(n):
    func = lambda x: x[0] ** 4 + x[1] ** 4 <= 1
    tmp = 1 / 2 ** n
    f = lambda x: np.sin(np.e ** (x[0] - x[1]))
    c_1, c_2, c_3, c_4, c_0 = [-1, 1], [-1 + tmp, 1], [-1 + tmp, 1 - tmp], [-1, 1 - tmp], [-1 + tmp / 2, 1 - tmp / 2]
    _c_1, _c_2, _c_3, _c_4, _c_0 = c_1[:], c_2[:], c_3[:], c_4[:], c_0[:]
    res_low = 0
    res_up = 0
    for i in range(2 ** (n + 1)):
        for j in range(2 ** (n + 1)):
            c_1[0] = c_1[0] + tmp
            c_2[0] = c_2[0] + tmp
            c_3[0] = c_3[0] + tmp
            c_4[0] = c_4[0] + tmp
            c_0[0] = c_0[0] + tmp
            ktp = [func(i) for i in [c_1, c_2, c_3, c_4, c_0]]
            if all(ktp):
                res_low += f(c_0) * tmp ** 2
            if any(ktp):
                res_up += f(c_0) * tmp ** 2

        c_1 = [_c_1[0], c_1[1] - tmp]
        c_2 = [_c_2[0], c_2[1] - tmp]
        c_3 = [_c_3[0], c_3[1] - tmp]
        c_4 = [_c_4[0], c_4[1] - tmp]
        c_0 = [_c_0[0], c_4[1] - tmp]

    return res_low, res_up


# ------------------------------------------------- Task 3 -------------------------------------------------------------
def task_3(m, func):
    return monte_carlo([func], [1] * m, 10000)


def f(x):
    res = 0
    for i in x:
        res += i ** 2
    if res < 0.25:
        return True
    return False


if __name__ == '__main__':
    print('Task 1.1')
    print('Variant 1: ', task_1_1(8))
    test_f = lambda x: x[0] ** 4 + x[1] ** 4 <= 1
    print('Variant 2: ', monte_carlo([test_f], [2, 2], 10000))

    print('\nTask 1.2')
    # print('Variant 1: ', task_1_2(4))  # you can check it by yourself, but it will take 3-5 minutes (n=4)
    print('Variant 1:  (12.868896484375, 15.29052734375)')
    test_func_1 = lambda x: x[0] ** 2 + x[1] ** 2 <= 1
    test_func_2 = lambda x: x[0] + x[1] <= x[2]
    test_func_3 = lambda x: x[2] <= 2 * x[1] + 3 * x[2]
    test_func = [test_func_1, test_func_2, test_func_3]
    print('Variant 2: ', monte_carlo(test_func, [2, 2, 10], 10000))

    print('\nTask 2')
    print('Variant 1: ', task_2(8))
    test_func = lambda x: x[0] ** 4 + x[1] ** 4 <= 1
    test_f = lambda x: np.sin(np.e ** (x[0] - x[1]))
    print('Variant 2: ', monte_carlo_integral(test_f, [test_func], [2, 2], 10000))

    print('\nTask 3')
    m = int(input('Input m: '))
    test_func = test_f
    print('Monte-carlo res: ', task_3(m, test_func))
