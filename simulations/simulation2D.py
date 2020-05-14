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
    grid = Grid(2000)

    grid.populate(1, 10)
    mooves = [
        (0, 0),
        (0, 3),
        (3, 3),
        (3, 0),
        (0, 0),
        (5, 456)
    ]
    simulation = Simulation(mooves, grid, 1, 1, 1)
    # simulation.simulate()
    # grid.show_grid()
