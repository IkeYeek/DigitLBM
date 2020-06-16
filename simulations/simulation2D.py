#!/usr/bin/python3.8
"""
1ere méthode à tester :
on fait un grid de nxn, représentant un espace de n microns par n microns
sur chaque micron, il y a une référence a une particule ou non
une particule peut s'étendre sur +eurs microns
UPDATE: nxn microns devient vite ingérable, à voir trouver mieux
"""
import time

from simulations.logger import Logger
from simulations.simulation2d.ImageRenderer import ImageRenderer
from simulations.simulation2d.LaserMoovesBridge import LaserMoovesBridge
from simulations.simulation2d.NoNumpyTest import Grid
from simulations.simulation2d.Simulation import Simulation


def benchmark(func, msg):
    t1 = time.time()
    func()
    t2 = time.time()
    Logger.getInstance().info('%fs pour %s' % (t2-t1, msg))


def main():
    # On instancie le grid avec sa taille
    grid = Grid(2000)
    # On génère le lit de poudre en précisant (pour cette implémentation) les tailles
    benchmark(lambda: grid.populate(1, 3), "générer le nid de poudre")

    # On instancie le bridge qui permet de récupérer les fichiers .csv et de les convertir en mouvements
    lmb = LaserMoovesBridge('./autre/diamant.csv', grid)
    mooves = lmb.get_moves()

    # On prépare et lance la simulation
    simulation = Simulation(mooves, grid, 1, 1, 64)
    benchmark(lambda: simulation.simulate(), "simuler le laser")

    # On rend l'image
    img = ImageRenderer(grid, simulation.get_params())
    benchmark(lambda: img.POC(), "rendre l'image finale")
    img.save()
    # img.show()
    ##########
    def show_grid():
        grid_representation = grid.show_grid()
        Logger().getInstance().debug('Etat final du plateau :')
        Logger().getInstance().debug(grid_representation)

    # show_grid()
    ##########


if __name__ == '__main__':
    benchmark(main, "l'exécution totale")
