#!/usr/bin/python3.8
"""
1ere méthode à tester :
on fait un grid de nxn, représentant un espace de n microns par n microns
sur chaque micron, il y a une référence a une particule ou non
une particule peut s'étendre sur +eurs microns
"""
import os
import time

from simulations.logger import Logger
from simulations.simulation2d.ImageRenderer import ImageRenderer
from simulations.simulation2d.NumpyGrid import Grid
from simulations.simulation2d.Simulation import Simulation
from sklearn.preprocessing import MinMaxScaler


import numpy as np


def benchmark(func, msg):
    t1 = time.time()
    func()
    t2 = time.time()
    Logger.getInstance().info('%fs pour %s' % (t2-t1, msg))


def main():
    grid = Grid(5000)
    benchmark(lambda: grid.populate(1, 10), "générer le nid de poudre")

    ##########
    f_path = os.path.normpath('./autre/cylindre.csv')
    temp = []
    with open(f_path) as carre:
        for l in carre:
            temp.append(l.replace('\n', '').replace('[', '').replace(']', '').replace(';', ',').split(','))
    temp_np = np.asarray(temp)
    mms = MinMaxScaler(feature_range=(0, grid.size - 1))
    temp_np = mms.fit_transform(temp_np)
    temp_np = temp_np.astype('int')
    mooves = []

    for t in temp_np:
        mooves.append(
            [
                (round(t[0]), round(t[1])), (round(t[3]), round(t[4]))])
    ##########
    mooves = [
        [(0, 0), (999, 999), (0, 999), (500, 500), (999, 999), (0, 500), (0, 0)]
    ]
    simulation = Simulation(mooves, grid, 1, 1, 30)
    benchmark(lambda: simulation.simulate(), "simuler le laser")
    img = ImageRenderer(grid);
    img.POC()

    def show_grid():
        grid_representation = grid.show_grid()
        Logger().getInstance().debug('Etat final du plateau :')
        Logger().getInstance().debug(grid_representation)

    # show_grid()


if __name__ == '__main__':
    benchmark(main, "l'exécution totale")
