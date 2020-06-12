#!/usr/bin/python3.8
import collections
from random import randint
from simulations.logger import Logger
from simulations.simulation2d.Particle import Particle


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
        self.grid = [None] * size ** 2
        self.size = size

    def show_grid(self) -> str:
        """
        Utile uniquement pour debug des petits grid, sous peine de surement faire planter le PC étant donné la taile supposée de ce dernier
        Affich le grid dans la console
        :return:
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

    def can_fit(self, particle: Particle) -> bool:
        """
        Vérifie qu'une particule de taille n aux coordonnées (i, j) peut rentrer
        :param particle: la particule a tester, déjà paramétrée
        :return: True si oui, False si non
        """
        fits = True
        for i in range(particle.size):
            for j in range(particle.size):
                if particle.i + particle.size > self.size or particle.j + particle.size > self.size:
                    fits = False
                elif self.grid[(particle.i + i) * self.size + particle.j + j] is not None:
                    fits = False
            return fits

    def fit(self, particle: Particle) -> None:
        """
        Place une particule sur le grid
        :param particle: la particule a placer
        """
        for i in range(particle.size):
            for j in range(particle.size):
                self.grid[(particle.i + i) * self.size + particle.j + j] = particle

    def populate(self, min_size=1, max_size=1) -> None:
        """
        Cette méthode sert à remplir le grid, elle est amenée à évoluer vers une simulation + réaliste
        Pour le moment, elle place des particules de taille min_size <= size <= max_size sans laisser de trous
        une particule qui ne fit pas est réduite jusqu'à fit
        :param min_size: la taille minimale des particules
        :param max_size: la taille maximale des particules
        """
        self.logger.info("Démarrage de la simulation d'étalement")
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
        self.logger.info("Étalement du nid de poudre terminé")

    def particle_at(self, i: int, j: int) -> Particle:
        """
        renvoie la particule aux coordonnées (i, j) si elle existe
        """
        return self.grid[int((i * self.size) + j)]


