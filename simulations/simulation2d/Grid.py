#!/usr/bin/python3.8
import collections
from random import randint

from simulations.simulation2d.Particle import Particle


class Grid:
    def __init__(self, size: int):
        self.grid = {}
        self.size = size
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i, j] = None

    def show_grid(self):
        last_i = -1
        for i, j in self.grid:
            if i != last_i:
                last_i = i
                print()
            if self.grid[i, j] is None:
                print(" x ", end='')
            else:
                print(" %s " % self.grid[i, j], end='')

    def can_fit(self, particle: Particle) -> bool:
        fits = True
        for i in range(particle.size):
            for j in range(particle.size):
                if particle.i + particle.size > self.size or particle.j + particle.size > self.size:
                    fits = False
                elif self.grid[particle.i + i, particle.j + j] is not None:
                    fits = False
            return fits

    def fit(self, particle: Particle) -> None:
        for i in range(particle.size):
            for j in range(particle.size):
                self.grid[particle.i + i, particle.j + j] = particle

    def populate(self, min_size=1, max_size=1) -> None:
        for i in range(self.size):
            for j in range(self.size):
                size = randint(min_size, max_size)
                curr_p = Particle(size, i, j)
                fitted = False
                while not fitted and curr_p.size >= 1:
                    if self.can_fit(curr_p):
                        self.fit(curr_p)
                        fitted = True
                    else:
                        curr_p.size -= 1
                if not fitted:
                    Particle.avoid()

    def particle_at(self, i: int, j: int) -> Particle:
        if 0 <= i < self.size and 0 <= j < self.size:
            return self.grid[(i, j)]



"""
class Grid:
    def __init__(self, size: int):
        self.grid = {}
        self.default_grid = []
        self.size = size
        for i in range(size):
            for j in range(size):
                self.default_grid.append((i, j))

    def populate(self, min_size=1, max_size=1) -> None:
        while len(self.default_grid) > 0:
            curr_point = self.default_grid[0]
            size = randint(min_size, max_size)
            curr_particle = Particle(size, curr_point[0], curr_point[1])
            fitted = False
            while not fitted:
                if self.can_fit(curr_particle):
                    self.fit(curr_particle)
                    fitted = True
                else:
                    curr_particle.size -= 1
        # self.grid = collections.OrderedDict(sorted(self.grid.items()))

    def can_fit(self, particle: Particle) -> bool:
        if particle.i + particle.size > self.size or particle.j + particle.size > self.size:
            return False
        else:
            for i in range(particle.size):
                for j in range(particle.size):
                    if (particle.i + i, particle.j + j) not in self.default_grid:
                        return False

        return True

    def fit(self, particle):
        for i in range(particle.size):
            for j in range(particle.size):
                coords = particle.i + i, particle.j + j
                self.default_grid.remove(coords)
                self.grid[coords] = particle

    def show_ascii_grid(self):
        last_i = -1
        for i, j in self.grid:
            if i != last_i:
                last_i = i
                print()
            if self.grid[i, j] is None:
                print(" x ", end='')
            else:
                print(" %s " % self.grid[i, j], end='')
"""