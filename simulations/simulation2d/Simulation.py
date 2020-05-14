#!/usr/bin/python3.8
from simulations.simulation2d.Grid import Grid


class Simulation:
    def __init__(self, schema: list, grid: Grid, power: int, speed: int, spot_size: int):
        self.schema = schema
        self.grid = grid
        self.power = power
        self.speed = speed
        self.spot_size = spot_size

    def simulate(self) -> None:
        schema = []
        schema.extend(self.schema)
        last_position = schema.pop(0)
        while len(schema) > 0:
            next_position = schema.pop(0)
            self.go_through(last_position, next_position)
            last_position = next_position

    def go_through(self, origin: tuple, destination: tuple) -> None:
        points = Simulation.decompose_vector(origin, destination)
        for point in points:
            self.grid.particle_at(point[0], point[1]).accept(self.power, self.speed)
            for i in range(1, self.spot_size):
                pass

    @staticmethod
    def decompose_vector(origin: tuple, destination: tuple) -> list:
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

        points.append(destination)
        return points




