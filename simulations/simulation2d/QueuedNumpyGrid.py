#!/usr/bin/python3.8
import collections
import ctypes
import faulthandler
import multiprocessing
import sys
from multiprocessing.connection import Connection
from random import randint
import numpy as np
from simulations.logger import Logger
from simulations.simulation2d.Particle import Particle
from multiprocessing import Process, Queue


class Grid(object):
    """
    Classe représentant le "grid" 2D, c'est-à-dire un damier de x*x qui contient tous les grains
    Il est possible de retrouver les coordonnées d'une particule à partir de cette dernière (i, j du point le plus au nord ouest)
        et également de retrouver une particule a partir d'une coordonnée du grid
    """
    def __init__(self, size: int):
        """
        Initialise le grid
        :param size: la taille du grid (x pour x*x)
        """
        self.logger = Logger().getInstance()
        self.grid = np.empty(size ** 2, dtype=Particle)
        self.size = size
        self.logger.info("Initialisation du nid de poussière")
        self.logger.info("Nid de poussière terminé")
        self.processes = []
        self.queues = []

    def show_grid(self) -> str:
        """
        Utile uniquement pour debug des petits grid, sous peine de surement faire planter le PC étant donné la taile supposée de ce dernier
        Affich le grid dans la console
        :return: the grid as a string
        """
        last_i = -1
        string = str()
        for i in range(self.size):
            for j in range(self.size):
                if i != last_i:
                    last_i = i
                    string += '\n'
                if self.grid[i * self.size + j] is None:
                    string += " x "
                else:
                    string += " %s " % self.grid[i * self.size + j]
        string += "\n"
        return string

    @staticmethod
    def can_fit(grid, size, particle: Particle) -> bool:
        """
        Vérifie qu'une particule de taille n aux coordonnées (i, j) peut rentrer
        :param particle: la particule a tester, déjà paramétrée
        :return: True si oui, False si non
        """
        fits = True
        for i in range(particle.size):
            for j in range(particle.size):
                if particle.i + particle.size > size or particle.j + particle.size > size:
                    fits = False
                elif grid[(particle.i + i) * size + particle.j + j] is not None:
                    fits = False
            return fits

    @staticmethod
    def fit(grid, size, particle: Particle) -> None:
        """
        Place une particule sur le grid
        :param size:
        :param grid:
        :param particle: la particule a placer
        """
        for i in range(particle.size):
            for j in range(particle.size):
                grid[(particle.i + i) * size + particle.j + j] = particle

    @staticmethod
    def populate_process(size_grid, min_size, max_size, start, stop, queue: Queue):
        grid_local = queue.get()
        for y in range(start, stop, 1):
            for x in range(size_grid):
                size_particle = randint(min_size, max_size)
                curr_p = Particle(size_particle, y, x)
                fitted = False
                while not fitted and curr_p.size >= 1:
                    if Grid.can_fit(grid_local, size_grid, curr_p):
                        Grid.fit(grid_local, size_grid, curr_p)
                        fitted = True
                    else:
                        curr_p.size -= 1
                if not fitted:
                    Particle.avoid()
        grid_local = list(filter(lambda x: x is not None, grid_local))
        # print(sys.getsizeof(grid_local))
        queue.put(grid_local)

    def populate(self, min_size=1, max_size=1) -> None:
        self.logger.info("Démarrage de la simuation d'étalement multiprocessus")

        nb_core = 4
        if nb_core > self.size:
            nb_core = self.size
        batch_size = np.math.ceil(self.size / nb_core)
        for i in range(nb_core):
            starting_line = i * batch_size
            ending_line = i * batch_size + batch_size
            if ending_line >= self.size:
                ending_line = self.size
            q = Queue()
            p = Process(target=Grid.populate_process, args=(self.size, min_size, max_size, starting_line, ending_line, q))
            p.start()
            q.put(self.grid)
            self.processes.append(p)
            self.queues.append(q)

        last_index = 0
        for queue in self.queues:
            while queue.empty():
                pass
            curr = queue.get_nowait()
            for val in curr:
                if last_index < self.size ** 2:
                    self.grid[last_index] = val
                last_index += 1

        for process in self.processes:
            process.join()
        self.logger.info("Étalement du nid de poussière terminé")

    def particle_at(self, ij: tuple) -> Particle:
        """
        renvoie la particule aux coordonnées (i, j) si elle existe
        """
        if 0 <= ij[0] < self.size and 0 <= ij[1] < self.size:
            return self.grid[int((ij[0] * self.size) + ij[1])]
        else:
            raise Exception('Coordonnée impossible (%d, %d)' % ij)

