#!/usr/bin/python3.8
import math

from simulations.simulation2d.Grid import Grid


class Simulation(object):

    def __init__(self, schema: list, grid: Grid, power: int, speed: int, spot_size: int):
        """
        initialise les paramètres de la simulation
        :param schema: le schéma de laser à suivre
        :param grid: la grid sur laquelle on applique la simulation
        :param power: la puissance du laser dans la simulation
        :param speed: la vitesse du laser dans la simulation
        :param spot_size: la taille du spot du laser
        """
        self.schema = schema
        self.grid = grid
        self.power = power
        self.speed = speed
        self.step = 0
        if spot_size&1 != 1:
            spot_size += 1
        self.spot_size = spot_size

    def simulate(self) -> None:
        """
        lance la simulation (peut prendre du temps)
        """
        schema = []
        schema.extend(self.schema)
        last_position = schema.pop(0)
        while len(schema) > 0:
            next_position = schema.pop(0)
            self.go_through(last_position, next_position, len(schema) == 0)
            last_position = next_position
        print("simulation done in %d steps" % (self.step, ))

    def go_through(self, origin: tuple, destination: tuple, last=False) -> None:
        """
        lance les calculs pour tous les points entre origin (compris) et destination (compris si dernier du schema)
            en comptant le spot_size
        :param origin: le point de départ
        :param destination: le point d'arrivé
        :param last: si dernier trajet du schéma
        """
        points = Simulation.get_traveled_points(origin, destination, last)
        for point in points:
            self.spot(point)

    def spot(self, point) -> None:
        """
        implementation of the laser spot
        :param point: the point
        """
        i, j = point[0], point[1]
        offset = (self.spot_size-1) / 2

        for n in range(self.spot_size):
            for k in range(self.spot_size):
                self.step += 1
                if self.step % 100000 == 0:
                    print("step %d for %d;%d" % (self.step, i, j))
                x = i + n - offset
                y = j + k - offset
                if ((x - i) ** 2) + ((y - j) ** 2) < (self.spot_size/2) ** 2:
                    self.apply(x, y)

    def apply(self, i, j):
        if 0 <= i < self.grid.size and 0 <= j < self.grid.size:
            self.grid.particle_at((i, j)).accept(self.power, self.speed)

    @staticmethod
    def get_traveled_points(origin: tuple, destination: tuple, last) -> list:
        """
        renvoie la liste de tous les points (avec à peu près les bonnes coordonnées étant donné
            que la méthode utilisée ne donne pas que des entiers) traversés entre origin et destination
        :param origin: le point de départ
        :param destination: le point d'arrivé
        :param last: si dernier trajet du schéma
        """
        points = []
        if destination[1] - origin[1] != 0:
            m = (destination[0] - origin[0]) / (destination[1] - origin[1])
            p = origin[0] - (m * origin[1])
            step = 1 if origin[1] < destination[1] else -1
            for i in range(origin[1], destination[1], step):
                points.append((round((m * i + p)), i))
        else:  # cas d'une droite parralèle à l'axe des ordonnées
            step = 1 if origin[0] < destination[0] else -1
            for i in range(origin[0], destination[0], step):
                points.append((i, origin[1]))
        if last:
            points.append(destination)
        return points




