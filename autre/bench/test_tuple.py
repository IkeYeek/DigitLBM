#!/usr/bin/python3.8
import time
import numpy as np


size = 14


def benchmark(func, msg, rpt):
    all_times = np.empty(rpt, dtype=np.float64)
    for i in range(rpt):
        t1 = time.time()
        func()
        t2 = time.time()
        all_times[i] = t2-t1
    print(('%fs pour %s' % (np.mean(all_times), msg)))


def fun_dummy(ij: tuple) -> int:
    return int((ij[0] * size) + ij[1])


def fun_dummy2(i: int, j: int) -> int:
    return int((i * size) + j)


def fun_bm_1():
    for i in range(34216664):
        test = fun_dummy((i, i))


def fun_bm_2():
    for i in range(34216664):
        test = fun_dummy2(i, i)


if __name__ == '__main__':
    benchmark(fun_bm_1, "avec tuple :", 10)
    benchmark(fun_bm_2, "sans tuple :", 10)