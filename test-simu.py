#!/usr/bin/python3.8

from slicer.load import load_mesh
from slicer.CuttingTools import slice_objet, regeneration_cordon
from slicer.fonction_generation_fichier_stl import Create_fichier_csv

if __name__ == '__main__':
    mesh = load_mesh("./autre/diamant.stl", "binaire")

    resultat, liste_gen_cordon = slice_objet(mesh, 0.1, False, "z",
                                             30, 12, 0.1, 0, 0, "cylindrique",
                                             True, ["lineaire", "decroisse"],                                             1, False, 1)
    Create_fichier_csv('test.csv', resultat)