#!/usr/bin/python3.8
import numpy as np
import time
import random


def benchmark(func, msg, rpt):
    all_times = np.empty(rpt, dtype=np.float64)
    for i in range(rpt):
        t1 = time.time()
        func()
        t2 = time.time()
        all_times[i] = t2-t1
    print(('%fs pour %s' % (np.mean(all_times), msg)))


def f1():
    for i in range(999999):
        test = round(random.random())


def f2():
    for i in range(999999):
        test = np.round(random.random())


if __name__ == '__main__':
    benchmark(f1, "buitin", 10)
    benchmark(f2, "numpy", 10)