#!/usr/bin/python3.8
"""
1ere méthode à tester :
on fait un grid de nxn, représentant un espace de n microns par n microns
sur chaque micron, il y a une référence a une particule ou non
une particule peut s'étendre sur +eurs microns
"""
import time
from rich.table import Table

from simulations.logger import Logger
from simulations.simulation2d.NumpyGrid import Grid
from simulations.simulation2d.Simulation import Simulation


def benchmark(func, msg):
    t1 = time.time()
    func()
    t2 = time.time()
    Logger.getInstance().info('Time in total : %f for %s' % (t2-t1, msg))


def main():
    grid = Grid(5000)
    benchmark(lambda: grid.populate(1, 10), "populating grid")
    mooves = [
        (0, 0), (4999, 4999),
        (4999, 0), (0, 4999)
    ]

    simulation = Simulation(mooves, grid, 1, 1, 30)
    benchmark(lambda: simulation.simulate(), "simulating the laser")
    # plat = grid.show_grid()
    # Logger().getInstance().log_table(plat, 'Etat final du plateau :')


if __name__ == '__main__':
    benchmark(main, "total execution")
