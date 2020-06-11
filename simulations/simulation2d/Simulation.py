#!/usr/bin/python3.8
from rich.progress import Progress
from rich.table import Table


from simulations.logger import Logger
from simulations.simulation2d.NumpyGrid import Grid


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
        self.logger = Logger().getInstance()
        self.schemas = schema
        self.grid = grid
        self.power = power
        self.speed = speed
        if spot_size & 1 != 1:
            spot_size += 1
        self.spot_size = spot_size

    def simulate(self) -> None:
        """
        lance la simulation (peut prendre du temps)
        """
        self.logger.info("Démarrage de la simulation")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Paramètre", style="dim", width=12)
        table.add_column("Valeur")
        params = self.get_params()
        for p in params:
            table.add_row(
                p, str(params[p])
            )

        self.logger.log_table(table, "Paramètres de la simulation")
        with Progress() as progress:
            simulation_progress = progress.add_task("[blue]Simulation en cours  ...", total=len(self.schemas))
            for i in range(len(self.schemas)):
                # Logger().getInstance().debug("%d/%d" % (i, len(self.schemas)))
                progress.update(simulation_progress, advance=1)
                schema = []
                schema.extend(self.schemas[i])
                last_position = schema.pop(0)
                while len(schema) > 0:
                    next_position = schema.pop(0)
                    self.go_through(last_position, next_position, len(schema) == 0)
                    last_position = next_position
        self.logger.info("Fin de la simulation")

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
            self.spot(int(point[0]), int(point[1]))

    def spo_t(self, i, j) -> None:
        """
        implementation of the laser spot
        """
        spot_size = self.spot_size
        offset = (spot_size - 1) / 2

        for n in range(spot_size):
            for k in range(spot_size):
                x = i + n - offset
                y = j + k - offset
                if ((x - i) ** 2) + ((y - j) ** 2) < (spot_size / 2) ** 2:
                    self.apply(x, y)

    def spot(self, x, y) -> None:
        """
        Amélioration du laser spot (gain de perf ultra impressionnant ->
        l'autre implémentation est + lente et bug avec PyPy (je la soupçonne de bloquer la JIT)
        Pour un spot_size de 65 et un grid de 1000 sur diamant :
        autre implémentation avec CPyton (plus rapide que PyPy dans ce cas là) : 260 sec
        cette implémentation + PyPy (plus rapide que CPython) : 36 sec

        En gros on divise par 4 le travail (ce qui explique le gain de perf CPython) et un miracle se produit pour PyPy
        :param x:
        :param y:
        :return:
        """
        spot_size = self.spot_size
        offset = round((spot_size - 1) / 2)
        for i in range(x - offset, x, 1):
            for j in range(y - offset, y, 1):
                if (i - x) ** 2 + (j - y) ** 2 < (spot_size / 2) ** 2:
                    xSym = x - (i - x)
                    ySim = y - (j - y)
                    self.apply(i, j)
                    self.apply(xSym, j)
                    self.apply(i, ySim)
                    self.apply(xSym, ySim)
        for i in range(offset):
            self.apply(x+i, y)
            self.apply(x, y+i)
            self.apply(x-i, y)
            self.apply(x, y-i)
        self.apply(x, y)

    def apply(self, i, j):
        grid_size = self.grid.size
        if 0 <= i < grid_size and 0 <= j < grid_size:
            self.grid.particle_at(i, j).accept(self.power, self.speed)

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

    def get_params(self, param=None):
        if param is None:
            return {'grid_size': self.grid.size, 'spot_size': self.spot_size, 'speed': self.speed, 'power': self.power}
        else:
            return getattr(self, param, None)



