#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


def build_all_partions(n, m):
    """
    Builds all possible fills of len M array with total sum n
    (all ways to find n-th derivative on func with m variables)
    """

    def _build_all_partions(n: int, m: int, current_arr: list, res):
        if sum(current_arr) == n and current_arr not in res:
            res.append(current_arr)
        elif sum(current_arr) == n and current_arr in res:
            return
        else:
            for i in range(len(current_arr)):
                new_arr = current_arr[:i] + [current_arr[i] + 1] + current_arr[i + 1:]
                _build_all_partions(n, m, new_arr, res)

    current = [0]*m
    res = []
    _build_all_partions(n, m, current, res)
    return res


if __name__ == '__main__':
    print(build_all_partions(5, 3))
