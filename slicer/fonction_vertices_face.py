# coding:latin-1

import numpy as np

from slicer.fonction_vecteur import *

def vertices(mesh) :
    '''
    # cette fonction retourne toutes les coordonnées
    # des sommets sous forme [x,y,z] d'un objet défini
    # comme "mesh" par la fonction "load_mesh"
    
    ##########################

    ##########
    # entrée #
    ##########

    # mesh (type list sous un format particulier défini par la fonction load_mesh)

    ##########
    # sortie #
    ##########

    # tableau (type list) : tableau listant les sommets des facettes

    ##########################'''

    tableau=[]

    for i in range(len(mesh)) :
        tableau.append(mesh[i][1][0])
        tableau.append(mesh[i][1][1])
        tableau.append(mesh[i][1][2])

    return tableau

def face(mesh):
    '''
    # cette fonction retourne les indices des sommets
    # du tableau en sortie de la fonction vertices formant une facette

    ##########################

    ##########
    # entrée #
    ##########

    # mesh (type list sous un format particulier défini par la fonction load_mesh)

    ##########
    # sortie #
    ##########

    # matrice (type list) : liste des indices des sommets

    ##########################'''

    tableau = vertices(mesh)
    ligne = []
    matrice = []

    for i in range(len(tableau)) :
        ligne.append(i)
        
        if i != 0 and (i+1) % 3 == 0:
            matrice.append(ligne)
            ligne = []

    return matrice

def normale(mesh):
    '''
    # cette fonction retourne la
    # normale de chaque facette

    ##########################

    ##########
    # entrée #
    ##########

    # mesh (type list sous un format particulier défini par la fonction load_mesh)

    ##########
    # sortie #
    ##########

    # tableau (type list) : liste des normales

    ##########################'''

    tableau = []

    for i in range(len(mesh)):
        tableau.append(mesh[i][0])

    return tableau

def get_face_adjacent_faces(mesh,facette_index):
    '''
    # cette fonction retourne les facettes
    # qui sont adjacentes à la facette demandée pour
    # un mesh 2D donné. Le principe repose
    # sur le fait que deux facettes sont adjacentes
    # si elles partagent deux sommets en commun

    ##########################

    ##########
    # entrée #
    ##########

    # mesh (type list sous un format particulier défini par la fonction load_mesh)

    # facette_index (type list) : correspond à une liste de trois items, chacun étant un indice correspondant à un sommet appartenant à la facette

    ##########
    # sortie #
    ##########

    # N_face_adjacente (type list) : correspond à une liste dont chaque item est une facette adjacente à facette_index

    ##########################'''

    sommet_mesh = vertices(mesh)
    sommet_facette = []
    face_mesh = face(mesh)
    facette = face_mesh[facette_index]
    N_face_adjacente = []

    ######################################## on récupère les sommets appartenant à facette_index ###############################################

    for i in range(3) :
        
        sommet_facette.append(sommet_mesh[facette[i]])

    ############################################################################################################################################

    for faces in face_mesh :

        if faces != facette :
            sommet = []

            ############################### on récupère les sommets appartenant à la facette que l'on va comparer ##############################
            
            for j in range(3) :
                sommet.append(sommet_mesh[faces[j]])

            ####################################################################################################################################

            point_commun_1 = 0
            point_commun_2 = 0
            point_commun_3 = 0

            ############################## on compte le nombre de points en communs avec un certain degré de précision ###########################

            for k in range(3) :

                    if comparaison_vecteur(sommet_facette[k],sommet[0],0.001) :

                        point_commun_1 = 1

            for k in range(3) :

                    if comparaison_vecteur(sommet_facette[k],sommet[1],0.001) :

                        point_commun_2 = 1

            for k in range(3) :

                    if comparaison_vecteur(sommet_facette[k],sommet[2],0.001) :

                        point_commun_3 = 1

            point_commun_total=point_commun_1+point_commun_2+point_commun_3

            ########################################################################################################################################

            ############################################ si on a exactement deux points en commun alors les facettes sont adjacentes ###############

            if point_commun_total >=2 :
                
                N_face_adjacente.append(faces)

    return N_face_adjacente
            
def sommet_de_face(mesh,facette):
    '''
    # cette fonction retourne les sommets
    # d'une facette

    ##########################

    ##########
    # entrée #
    ##########

    # mesh (type list sous un format particulier défini par la fonction load_mesh)

    # facette (type list) : correspond à une liste de trois items, chacun étant un indice correspondant à un sommet appartenant à la facette

    ##########
    # sortie #
    ##########

    # liste_sommets (type list) : correspond à une liste dont chaque item est un sommet de la facette

    ##########################'''

    sommet = vertices(mesh)
    liste_sommets = []

    for i in range(3):
        liste_sommets.append(sommet[facette[i]])

    return liste_sommets
