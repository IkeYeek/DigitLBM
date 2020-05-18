#!/usr/bin/python3.8
"""
1ere méthode à tester :
on fait un grid de nxn, représentant un espace de n microns par n microns
sur chaque micron, il y a une référence a une particule ou non
une particule peut s'étendre sur +eurs microns
"""
import time

from simulations.simulation2d.Grid import Grid
from simulations.simulation2d.Simulation import Simulation

if __name__ == '__main__':
    grid = Grid(10)
    t1 = time.time()

    grid.populate(1, 1)
    mooves = [
        (0, 0), (9, 9)
    ]
    simulation = Simulation(mooves, grid, 1, 1, 5)
    simulation.simulate()
    t2 = time.time()
    print("Time=%s" % (t2 - t1))
    grid.show_grid()
