# coding:latin-1

from slicer.fonction_vecteur import *

def if_facette_traverse_couche(sommets_facette,couche,axe) :
    '''
    # cette fonction v�rifie si une facette poss�de une intersection avec une couche

    ##########################

    ##########
    # entr�e #
    ##########

    # sommets_facette (type list) : liste des coordonn�es des trois sommets d'une facette sous le format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]

    # couche (type list) : liste comportant comme premier item la coordonn�e minimale selon la direction de l'entr�e axe et comme second item la coordonn�e maximale selon la direction de l'entr�e axe

    # axe (type str) : correspond � l'axe orthogonal au plan d�fini par la couche

    ##########
    # sortie #
    ##########

    # bol�en

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
    # cette fonction v�rifie si un segment poss�de une intersection avec une couche

    ##########################

    ##########
    # entr�e #
    ##########

    # point1 (type list) : liste des coordonn�es du point sous le format [x,y,z]

    # point2 (type list) : liste des coordonn�es du point sous le format [x,y,z]

    # couche (type list) : liste comportant comme premier item la coordonn�e minimale selon la direction de l'entr�e axe et comme second item la coordonn�e maximale selon la direction de l'entr�e axe

    # axe (type str) : correspond � l'axe orthogonal au plan d�fini par la couche

    ##########
    # sortie #
    ##########

    # bol�en

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
    # cette fonction v�rifie si les deux points sont tous deux hors de la couche

    ##########################

    ##########
    # entr�e #
    ##########

    # point1 (type list) : liste des coordonn�es du point sous le format [x,y,z]

    # point2 (type list) : liste des coordonn�es du point sous le format [x,y,z]

    # couche (type list) : liste comportant comme premier item la coordonn�e minimale selon la direction de l'entr�e axe et comme second item la coordonn�e maximale selon la direction de l'entr�e axe

    # axe (type str) : correspond � l'axe orthogonal au plan d�fini par la couche

    ##########
    # sortie #
    ##########

    # bol�en

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
    # cette fonction v�rifie si les deux points sont tous deux inclus dans la couche

    ##########################

    ##########
    # entr�e #
    ##########

    # point1 (type list) : liste des coordonn�es du point sous le format [x,y,z]

    # point2 (type list) : liste des coordonn�es du point sous le format [x,y,z]

    # couche (type list) : liste comportant comme premier item la coordonn�e minimale selon la direction de l'entr�e axe et comme second item la coordonn�e maximale selon la direction de l'entr�e axe

    # axe (type str) : correspond � l'axe orthogonal au plan d�fini par la couche

    ##########
    # sortie #
    ##########

    # bol�en

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
    # cette fonction v�rifie si un point est inclus dans la couche

    ##########################

    ##########
    # entr�e #
    ##########

    # point (type list) : liste des coordonn�es du point sous le format [x,y,z]

    # couche (type list) : liste comportant comme premier item la coordonn�e minimale selon la direction de l'entr�e axe et comme second item la coordonn�e maximale selon la direction de l'entr�e axe

    # axe (type str) : correspond � l'axe orthogonal au plan d�fini par la couche

    ##########
    # sortie #
    ##########

    # bol�en

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
    # cette fonction v�rifie si le point est un sommet de la facette

    ##########################

    ##########
    # entr�e #
    ##########

    # point (type list) : liste des coordonn�es du point sous le format [x,y,z]

    # facette (type list) :  liste des coordonn�es des trois sommets d'une facette sous le format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]

    # precision (type float ou int) : correspond � la pr�cision souhait�e

    ##########
    # sortie #
    ##########

    # bol�en

    ##########################'''

    for i in range(len(facette)) :

        if comparaison_vecteur(point,facette[i],precision) :

            return True

    return False

def de_part_et_autre(facette,couche,axe) :
    '''
    # cette fonction v�rifie si un segment poss�de deux intersections avec une couche

    ##########################

    ##########
    # entr�e #
    ##########

    # facette (type list) : liste  des points � v�rifier dont les coordonn�es sont sous le format [x,y,z]

    # couche (type list) : liste comportant comme premier item la coordonn�e minimale selon la direction de l'entr�e axe et comme second item la coordonn�e maximale selon la direction de l'entr�e axe

    # axe (type str) : correspond � l'axe orthogonal au plan d�fini par la couche

    ##########
    # sortie #
    ##########

    # bol�en

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


    

    

