#!/usr/bin/python3.8
import random

from autre.bench.benchmark import benchmark


def pow():
    for i in range (999999):
        n = random.random()
        k = n ** 2


def pow_lazy():
    for i in range (999999):
        n = random.random()
        k = n * n


if __name__ == '__main__':
    benchmark(pow, "n**2", 1000)
    benchmark(pow_lazy, "n*n", 1000)