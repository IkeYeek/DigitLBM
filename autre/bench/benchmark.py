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
import numpy as np
import time


def benchmark(func, msg, rpt):
    all_times = np.empty(rpt, dtype=np.float64)
    for i in range(rpt):
        t1 = time.time()
        func()
        t2 = time.time()
        all_times[i] = t2-t1
    print(('%fs pour %s' % (np.mean(all_times), msg)))