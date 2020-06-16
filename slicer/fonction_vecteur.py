# coding:latin-1

from math import sqrt

def vecteur_droite(point1,point2) :
    '''
    # cette fonction retourne un vecteur directeur de la
    # droite passant par point1 et point2

    ##########################

    ##########
    # entr�e #
    ##########

    # point1 (type list) : liste des coordonn�es du point sous le format [x,y,z]

    # point2 (type list) : liste des coordonn�es du point sous le format [x,y,z]

    ##########
    # sortie #
    ##########

    # vecteur_directeur (type list) : liste des coordonn�es du vecteur directeur de la droite sous le format [x,y,z]

    ##########################'''

    vecteur_directeur = [point2[0]-point1[0],point2[1]-point1[1],point2[2]-point1[2]]

    return vecteur_directeur

def distance_points(point_1,point_2) :
    '''
    # cette fonction retourne la distance entre deux points dans un espace de dimension N

    ##########################

    ##########
    # entr�e #
    ##########

    # point_1 (type list) : liste des coordonn�es du point sous le format [x,y,z]

    # point_2 (type list) : liste des coordonn�es du point sous le format [x,y,z]

    ##########
    # sortie #
    ##########

    # distance (type float) : correspond � la distance entre point_1 et point_2

    ##########################'''

    vecteur = operation_vecteur(point_1,point_2,"-")

    distance = norme_vecteur(vecteur)

    return distance

def norme_vecteur(vecteur) :
    '''
    # cette fonction retourne la norme d'un vecteur

    ##########################

    ##########
    # entr�e #
    ##########

    # vecteur (type list) : liste des coordonn�es du vecteur sous le format [x,y,z]

    ##########
    # sortie #
    ##########

    # norme (type float) : correspond � la norme du vecteur

    ##########################'''

    norme_au_carre = 0

    for  i in range(len(vecteur)) :

        norme_au_carre += vecteur[i]**2

    norme = sqrt(norme_au_carre)

    return norme                    

def operation_vecteur(vecteur1,vecteur2,signe):
    '''
    # cette fonction permet diff�rentes op�rations entre deux vecteurs ou entre un vecteur et un coefficient

    ##########################

    ##########
    # entr�e #
    ##########

    # vecteur1 (type list) : liste des coordonn�es du vecteur sous le format [x,y,z]
    
    # vecteur2 (type list ou float selon l'op�ration)

    # signe (type str) : correspond au signe de l'op�ration ("+","-","*","/","vec")

    ##########
    # sortie #
    ##########

    # vecteur (type list) : correspond au r�sultat de l'op�ration entre vecteur1 et vecteur2

    ##########################'''

    if signe != "vec" :

        vecteur = []

        for i in range(len(vecteur1)):

            ############################ addition #######################

            if signe == "+" :

                vecteur.append(vecteur1[i]+vecteur2[i])

            #############################################################

            ############################ diff�rence ###########################

            if signe == "-" :

                vecteur.append(vecteur1[i]-vecteur2[i])

            ####################################################################

            ############################ multiplication par un coefficient #####
                
            if signe == "*" :

                # ici vecteur2 sera un coefficient

                vecteur.append(vecteur1[i]*vecteur2)

            ####################################################################

            ########################### Division par un coefficient ############

            if signe == "/" :

                # ici vecteur2 sera un coefficient
                
                

                vecteur.append(vecteur1[i]/float(vecteur2))

            ####################################################################

    ############################# produit vectoriel ############################

    if signe == "vec" :

        vecteur_x = vecteur1[1]*vecteur2[2]-vecteur1[2]*vecteur2[1]
        vecteur_y = -(vecteur1[0]*vecteur2[2]-vecteur1[2]*vecteur2[0])
        vecteur_z = vecteur1[0]*vecteur2[1]-vecteur1[1]*vecteur2[0]

        vecteur = [vecteur_x,vecteur_y,vecteur_z]

    #############################################################################

    ############################ produit scalaire ( mis en commentaire car il ne servait que lors de la phase de tests sur une fonction particuli�re ) ###############################

    #if signe == "sca" :

                #vecteur = vecteur1[0]*vecteur2[0]+vecteur1[1]*vecteur2[1]+vecteur1[2]*vecteur2[2]

    ################################################################################

    return vecteur

def comparaison_vecteur(vecteur1,vecteur2,approximation) :
    '''
    # cette fonction compare deux vecteurs et si leur diff�rence est inf�rieure � l'approximation cela retourne True, sinon False

    ##########################

    ##########
    # entr�e #
    ##########

    # vecteur1 (type list) : liste des coordonn�es du vecteur sous le format [x,y,z]

    # vecteur2 (type list) : liste des coordonn�es du vecteur sous le format [x,y,z]

    # approximation (type float ou int) : correspond � l'approximation

    ##########
    # sortie #
    ##########

    # bol�en

    ##########################'''

    vecteur = operation_vecteur(vecteur1,vecteur2,"-")

    check = []

    for i in range(len(vecteur)) :

        check.append(0)

    for i in range(len(vecteur)) :

        if abs(vecteur[i]) <= approximation :

            check[i] = "OK"

    if check.count("OK") == 3 :

        return True

    return False

def normale_face(facette) :
    '''
    # cette fonction retourne la normale d'une facette

    ##########################

    ##########
    # entr�e #
    ##########

    # facette (type list) : liste des coordonn�es des sommets de la facette sous le format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]

    ##########
    # sortie #
    ##########

    # vecteur_normal (type list) : retourne les coordonn�es du vecteur normal � la facette sous le format [x,y,z]

    ##########################'''

    vecteur_directeur_1 = operation_vecteur(facette[0],facette[1],"-")
    vecteur_directeur_2 = operation_vecteur(facette[1],facette[2],"-")
            

    vecteur_normal = operation_vecteur(vecteur_directeur_1,vecteur_directeur_2,"vec")

    return vecteur_normal
