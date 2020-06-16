# coding:latin-1

from slicer.fonction_vecteur import *

def Calcul_centre_gravite(liste_coord_cordon) :
    '''
    # cette fonction permet de déterminer le centre de gravité d'un objet à partir des cordons qui le composent

    ##########################

    ##########
    # entrée #
    ##########

    # liste_coord_cordon (type list) : liste des coordonnées des cordons

    ##########
    # sortie #
    ##########

    # point_centre_gravite (type list) : coordonnées du centre de gravité de l'objet sous le format [x,y,z]

    ##########################'''

    coord_x = 0

    coord_y = 0

    coord_z = 0
    
    masse_totale = 0

    for i in range(len(liste_coord_cordon)) :

        for k in range(2) :

            for j in range(len(liste_coord_cordon[i][k])) :

                vecteur_directeur = operation_vecteur(liste_coord_cordon[i][k][j][1],liste_coord_cordon[i][k][j][0],"-")

                norme_vecteur_directeur = norme_vecteur(vecteur_directeur)

                vecteur_directeur_chemin = operation_vecteur(vecteur_directeur,2,"/")

                point_gravite = operation_vecteur(liste_coord_cordon[i][j][0],vecteur_directeur_chemin,"+")

                coord_x += point_gravite[0]*norme_vecteur_directeur

                coord_y += point_gravite[1]*norme_vecteur_directeur

                coord_z += point_gravite[2]*norme_vecteur_directeur

                masse_totale += norme_vecteur_directeur

    x_centre_gravite = float(coord_x)/masse_totale

    y_centre_gravite = float(coord_y)/masse_totale

    z_centre_gravite = float(coord_z)/masse_totale

    point_centre_gravite = [x_centre_gravite,y_centre_gravite,z_centre_gravite]

    return point_centre_gravite


    

                   
