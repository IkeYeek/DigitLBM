#!/usr/bin/python3.8
"""
* Copyright 2019 Lucas <IkeYeek> Marques - lucasmarques.ninja
*
*               GNU GENERAL PUBLIC LICENSE
*                       Version 3, 29 June 2007
*
* Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
* Everyone is permitted to copy and distribute verbatim copies
* of this license document, but changing it is not allowed.
"""
from PIL import Image

from autre.bench.benchmark import benchmark


def spot(i, j) -> list:
    """
    implementation of the laser spot
    """
    spot_size = 65
    offset = round((spot_size - 1) / 2)
    pts = []

    for n in range(spot_size):
        for k in range(spot_size):
            x = i + n - offset
            y = j + k - offset
            if ((x - i) ** 2) + ((y - j) ** 2) < (spot_size / 2) ** 2:
                pts.append((x, y))
    return pts


def spot_2(x, y):
    spot_size = 65
    offset = round((spot_size - 1) / 2)
    pts = []
    for i in range(x - offset, x, 1):
        for j in range(y - offset, y, 1):
            if (i - x) ** 2 + (j - y) ** 2 < (spot_size / 2) ** 2:
                xSym = x - (i - x)
                ySim = y - (j - y)
                pts.append((i, j))
                pts.append((xSym, j))
                pts.append((i, ySim))
                pts.append((xSym, ySim))
    for i in range(offset):
        pts.append((x+i, y))
        pts.append((x, y+i))
        pts.append((x-i, y))
        pts.append((x, y-i))
    pts.append((x, y))
    return pts


if __name__ == '__main__':
    benchmark(lambda: spot(10, 10), "first version", 2000)
    benchmark(lambda: spot_2(10, 10), "first version", 2000)

    s1 = spot(250, 250)
    s2 = spot_2(250, 250)

    print(len(s1))
    print(len(s2))
    im1 = Image.new("RGB", (500, 500), "#FFFFFF")
    im2 = Image.new("RGB", (500, 500), "#FFFFFF")

    pixels1 = im1.load()
    pixels2 = im2.load()

    for p in s1:
        pixels1[p] = (255, 0, 0)
    for p in s2:
        pixels2[p] = (255, 0, 0)
    im1.show()
    # im2.show()

