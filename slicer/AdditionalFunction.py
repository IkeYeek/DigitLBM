# coding:latin-1

from slicer.fonction_vertices_face import *
import numpy as np

def extremum_layer(layer,indice_coordonnees) :
    '''
    # cette fonction retourne les extremums d'un contour

    ##########################

    ##########
    # entrée #
    ##########

    # layer (type list) : liste de couples de coordonnées de points consécutifs du contour, ainsi que de la normale dirigée vers l'extérieur sous le format [([x1,y1,z1],[x2,y2,z2],[nx,ny,nz]),...]

    # indice_coordonnees (type list) : liste des indices correspondants aux coordonnées pour lesquelles on veut les extremums

    ##########
    # sortie #
    ##########

    # xMax (type int ou float) : valeur maximale observée pour les coordonnées d'indice "indice_coordonnees[0]"

    # xMin (type int ou float) : valeur minimale observée pour les coordonnées d'indice "indice_coordonnees[0]"

    # yMax (type int ou float) : valeur maximale observée pour les coordonnées d'indice "indice_coordonnees[1]"

    # yMin (type int ou float) : valeur minimale observée pour les coordonnées d'indice "indice_coordonnees[1]"

    # zMax (type int ou float) : valeur maximale observée pour les coordonnées d'indice "indice_coordonnees[2]"

    # zMin (type int ou float) : valeur minimale observée pour les coordonnées d'indice "indice_coordonnees[2]"

    ##########################'''

    xMax,xMin = layer[0][0][indice_coordonnees[0]],layer[0][0][indice_coordonnees[0]]
    yMax,yMin = layer[0][0][indice_coordonnees[1]],layer[0][0][indice_coordonnees[1]]
    zMax,zMin = layer[0][0][indice_coordonnees[2]],layer[0][0][indice_coordonnees[2]]
    

    for i in range(len(layer)) :

        for j in range(2) :

            if layer[i][j][indice_coordonnees[0]] >= xMax :

                xMax = layer[i][j][indice_coordonnees[0]]

            elif layer[i][j][indice_coordonnees[0]] <= xMin :

                xMin = layer[i][j][indice_coordonnees[0]]

            if layer[i][j][indice_coordonnees[1]] >= yMax :

                yMax = layer[i][j][indice_coordonnees[1]]

            elif layer[i][j][indice_coordonnees[1]] <= yMin :

                yMin = layer[i][j][indice_coordonnees[1]]

            if layer[i][j][indice_coordonnees[2]] >= zMax :

                zMax = layer[i][j][indice_coordonnees[2]]

            elif layer[i][j][indice_coordonnees[2]] <= zMin :

                zMin = layer[i][j][indice_coordonnees[2]]

    return xMax,xMin,yMax,yMin,zMax,zMin

            
#############################################################################################
#############################################################################################
#############################################################################################

# fonctions codées par Thibaud Rigondaud et adaptées pour être utilisées par le format de liste défini par la fonction load_mesh          

def Extremum (mesh):
    '''
    Returns the maximum and the minimum for each direction
    '''
    xMax,xMin = vertices(mesh)[0][0],vertices(mesh)[0][0]
    yMin,yMax = vertices(mesh)[0][1],vertices(mesh)[0][1]
    zMin,zMax = vertices(mesh)[0][2],vertices(mesh)[0][2]
    for points in vertices(mesh):
        if points[0] >= xMax:
            xMax = points[0]
        elif points[0] <= xMin:
            xMin = points[0]
        if points[1] >= yMax:
            yMax = points[1]
        elif points[1] <= yMin:
            yMin = points[1]
        if points[2] >= zMax:
            zMax = points[2]
        elif points[2] <= zMin:
            zMin = points[2]
    return xMax,xMin,yMax,yMin,zMax,zMin

def rad(AngleDeg):
    '''
    Convert an angle from degree to radian
    '''
    AngleRad = AngleDeg*(np.pi/180)
    return AngleRad
