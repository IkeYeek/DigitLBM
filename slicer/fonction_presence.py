# coding:latin-1

from slicer.fonction_vecteur import *

def if_facette_traverse_couche(sommets_facette,couche,axe) :
    '''
    # cette fonction vérifie si une facette possède une intersection avec une couche

    ##########################

    ##########
    # entrée #
    ##########

    # sommets_facette (type list) : liste des coordonnées des trois sommets d'une facette sous le format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]

    # couche (type list) : liste comportant comme premier item la coordonnée minimale selon la direction de l'entrée axe et comme second item la coordonnée maximale selon la direction de l'entrée axe

    # axe (type str) : correspond à l'axe orthogonal au plan défini par la couche

    ##########
    # sortie #
    ##########

    # boléen

    ##########################'''
    
    if axe == "x" :
        coordonnees = 0

    if axe == "y" :
        coordonnees = 1

    if axe == "z" :
        coordonnees = 2
        
    if sommets_facette[0][coordonnees] > couche[1] and sommets_facette[1][coordonnees] > couche[1] and  sommets_facette[2][coordonnees] > couche[1] :
        return False

    if sommets_facette[0][coordonnees] < couche[0] and sommets_facette[1][coordonnees] < couche[0] and  sommets_facette[2][coordonnees] < couche[0] :
        return False

    return True

def if_droite_traverse_couche(point1,point2,couche,axe) :
    '''
    # cette fonction vérifie si un segment possède une intersection avec une couche

    ##########################

    ##########
    # entrée #
    ##########

    # point1 (type list) : liste des coordonnées du point sous le format [x,y,z]

    # point2 (type list) : liste des coordonnées du point sous le format [x,y,z]

    # couche (type list) : liste comportant comme premier item la coordonnée minimale selon la direction de l'entrée axe et comme second item la coordonnée maximale selon la direction de l'entrée axe

    # axe (type str) : correspond à l'axe orthogonal au plan défini par la couche

    ##########
    # sortie #
    ##########

    # boléen

    ##########################'''

    if axe == "x" :
        coordonnees = 0

    if axe == "y" :
        coordonnees = 1

    if axe == "z" :
        coordonnees = 2

    if point1[coordonnees] > couche[1] and point2[coordonnees] > couche[1] :
        return False

    if point1[coordonnees] < couche[0] and point2[coordonnees] < couche[0] :
        return False

    return True

def if_not_deux_points_in_couche(point1,point2,couche,axe) :
    '''
    # cette fonction vérifie si les deux points sont tous deux hors de la couche

    ##########################

    ##########
    # entrée #
    ##########

    # point1 (type list) : liste des coordonnées du point sous le format [x,y,z]

    # point2 (type list) : liste des coordonnées du point sous le format [x,y,z]

    # couche (type list) : liste comportant comme premier item la coordonnée minimale selon la direction de l'entrée axe et comme second item la coordonnée maximale selon la direction de l'entrée axe

    # axe (type str) : correspond à l'axe orthogonal au plan défini par la couche

    ##########
    # sortie #
    ##########

    # boléen

    ##########################'''

    if axe == "x" :
        coordonnees = 0

    if axe == "y" :
        coordonnees = 1

    if axe == "z" :
        coordonnees = 2

    if point1[coordonnees] <= couche[1] and point1[coordonnees] >= couche[0] and point2[coordonnees] <= couche[1] and point2[coordonnees] >= couche[0] :
        return False

    return True

def if_deux_points_in_couche(point1,point2,couche,axe) :
    '''
    # cette fonction vérifie si les deux points sont tous deux inclus dans la couche

    ##########################

    ##########
    # entrée #
    ##########

    # point1 (type list) : liste des coordonnées du point sous le format [x,y,z]

    # point2 (type list) : liste des coordonnées du point sous le format [x,y,z]

    # couche (type list) : liste comportant comme premier item la coordonnée minimale selon la direction de l'entrée axe et comme second item la coordonnée maximale selon la direction de l'entrée axe

    # axe (type str) : correspond à l'axe orthogonal au plan défini par la couche

    ##########
    # sortie #
    ##########

    # boléen

    ##########################'''

    if axe == "x" :
        coordonnees = 0

    if axe == "y" :
        coordonnees = 1

    if axe == "z" :
        coordonnees = 2

    if point1[coordonnees] <= couche[1] and point1[coordonnees] >= couche[0] and point2[coordonnees] <= couche[1] and point2[coordonnees] >= couche[0] :
        return True

    return False

def if_point_in_couche(point,couche,axe) :
    '''
    # cette fonction vérifie si un point est inclus dans la couche

    ##########################

    ##########
    # entrée #
    ##########

    # point (type list) : liste des coordonnées du point sous le format [x,y,z]

    # couche (type list) : liste comportant comme premier item la coordonnée minimale selon la direction de l'entrée axe et comme second item la coordonnée maximale selon la direction de l'entrée axe

    # axe (type str) : correspond à l'axe orthogonal au plan défini par la couche

    ##########
    # sortie #
    ##########

    # boléen

    ##########################'''

    if axe == "x" :
        coordonnees = 0

    if axe == "y" :
        coordonnees = 1

    if axe == "z" :
        coordonnees = 2

    if point[coordonnees] <= couche[1] and point[coordonnees] >= couche[0] :
        return True

    return False

def if_point_in_facette(point,facette,precision) :
    '''
    # cette fonction vérifie si le point est un sommet de la facette

    ##########################

    ##########
    # entrée #
    ##########

    # point (type list) : liste des coordonnées du point sous le format [x,y,z]

    # facette (type list) :  liste des coordonnées des trois sommets d'une facette sous le format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]

    # precision (type float ou int) : correspond à la précision souhaitée

    ##########
    # sortie #
    ##########

    # boléen

    ##########################'''

    for i in range(len(facette)) :

        if comparaison_vecteur(point,facette[i],precision) :

            return True

    return False

def de_part_et_autre(facette,couche,axe) :
    '''
    # cette fonction vérifie si un segment possède deux intersections avec une couche

    ##########################

    ##########
    # entrée #
    ##########

    # facette (type list) : liste  des points à vérifier dont les coordonnées sont sous le format [x,y,z]

    # couche (type list) : liste comportant comme premier item la coordonnée minimale selon la direction de l'entrée axe et comme second item la coordonnée maximale selon la direction de l'entrée axe

    # axe (type str) : correspond à l'axe orthogonal au plan défini par la couche

    ##########
    # sortie #
    ##########

    # boléen

    ##########################'''

    if axe == "x" :
        coordonnees = 0

    if axe == "y" :
        coordonnees = 1

    if axe == "z" :
        coordonnees = 2

    check_ = []

    for i in range(len(facette)) :

        if facette[i][coordonnees] > couche[1] :

            check_.append("sup")

        if facette[i][coordonnees] < couche[0] :

            check_.append("inf")

    if check_.count("sup") !=0 and check_.count("inf") != 0 :

        return True

    return False


    

    

