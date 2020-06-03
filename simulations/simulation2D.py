#!/usr/bin/python3.8
"""
1ere méthode à tester :
on fait un grid de nxn, représentant un espace de n microns par n microns
sur chaque micron, il y a une référence a une particule ou non
une particule peut s'étendre sur +eurs microns
"""
import time

from simulations.logger import Logger
from simulations.simulation2d.MultiprocessThreadedNumpyGrid import Grid
from simulations.simulation2d.Simulation import Simulation


def benchmark(func, msg):
    t1 = time.time()
    func()
    t2 = time.time()
    Logger.getInstance().info('%fs pour %s' % (t2-t1, msg))


def main():
    grid = Grid(2000)
    benchmark(lambda: grid.populate(1, 1), "générer le nid de poudre")
    mooves = [
        (0, 0), (9, 9), (9, 0)
    ]
    simulation = Simulation(mooves, grid, 1, 1, 1)
    benchmark(lambda: simulation.simulate(), "simuler le laser")
    # grid_representation = grid.show_grid()
    # Logger().getInstance().debug('Etat final du plateau :')
    # Logger().getInstance().debug(grid_representation)


if __name__ == '__main__':
    benchmark(main, "l'exécution totale")
