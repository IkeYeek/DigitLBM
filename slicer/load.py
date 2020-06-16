# coding:latin-1
"""
Created on Wed Apr 29 14:13:22 2020

@author: leogu
"""

from stl import mesh

def facet_normal(line) :

    '''

    # cette fonction teste si on est en train de lire
    # une ligne qui définit la normale d'une facette

    ##########################

    ##########
    # entrée #
    ##########

    # line (type str) : correspond à la ligne d'un fichier

    ##########
    # sortie #
    ##########

    # boléen

    ########################## '''
    
    if line[2:14] == "facet normal" :
        return True
    
    return False

def indent(line) :
    '''
    # cette fonction teste si on est en train de lire
    # une ligne comprise dans la définition d'une facette
    # pour une certaine normale

    ##########################

    ##########
    # entrée #
    ##########

    # line (type str) : correspond à la ligne d'un fichier

    ##########
    # sortie #
    ##########

    # boléen

    ##########################'''
    
    if line[0:4] == "    " :
        return True
    
    return False

def si_vertex(line) :
    '''
    # cette fonction teste si on est en train de lire
    # une ligne définissant un point d'une facette

    ##########################

    ##########
    # entrée #
    ##########

    # line (type str) : correspond à la ligne d'un fichier

    ##########
    # sortie #
    ##########

    # boléen

    ##########################'''
    
    if line[6:12] == "vertex" :
        return True
    
    return False

def str_to_float(liste) :
    '''
    # cette fonction crée la copie d'une liste
    # où les items, qui étaient de type "str" dans
    # la liste d'origine, sont de type "float"

    ##########################

    ##########
    # entrée #
    ##########

    # liste (type list, type item str) 

    ##########
    # sortie #
    ##########

    # liste (type list, type item float)

    ##########################'''

    liste_float = []

    for i in range(len(liste)):
        liste_float.append(float(liste[i]))

    return liste_float
    
def load_mesh(fichier,type_fichier) :
    '''
    # cette fonction lit un fichier au format .stl
    # et construit un tableau de données facilement
    # exploitable en fonction des données du fichier
    # le tableau renvoyé est sous le format :
    # [[[n1x,n1y,n1z],[[p1x,p1y,p1z],[p2x,p2y,p2z],[p3x,p3y,p3z]],...]
    # n1x,n1y,n1z désignent les coordonnées de la normale 1 et p1x,p1y,p1z
    # désignent les coordonnées du premier sommet de la facette
    # Dans le cas d'un nombre important d'informations il est préférable
    # de charger le mesh en binaire même si le fichier est en ASCII

    ##########################

    ##########
    # entrée #
    ##########

    # fichier (type .stl)
    
    # type_fichier (type str)

    ##########
    # sortie #
    ##########

    # liste (type list, type item float)

    ##########################'''
    
    mesh_ = []

    ##############################
    # traitement fichier en ASCII#
    ##############################

    if type_fichier == "ASCII" :
    
        with open(str(fichier),"r") as fich :
            line = fich.readline()
            
            while line :
                line = line.replace("\n","")
                
                if facet_normal(line) :
                    part1 = str_to_float(line[15:].split(" "))
                    part2 = []
                    line = fich.readline()
                    line = line.replace("\n","")
                    
                    while indent(line) :
                        
                        if si_vertex(line) :
                            part2.append(str_to_float(line[13:].split(" ")))
                            
                        line = fich.readline()
                        line = line.replace("\n","")
                        
                    part3 = [part1,part2]
                    mesh_.append(part3)
                    
                line = fich.readline()

    ################################
    # traitement fichier en binaire#
    ################################

    if type_fichier == "binaire" :

        my_mesh = mesh.Mesh.from_file(fichier)

        for i in range(len(my_mesh.normals)) :

            part1 = list(my_mesh.normals[i])
            part2 = list(my_mesh.v0[i])
            part3 = list(my_mesh.v1[i])
            part4 = list(my_mesh.v2[i])

            mesh_.append([part1,[part2,part3,part4]])
            
    return mesh_
    
