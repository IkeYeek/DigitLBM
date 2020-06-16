# coding:latin-1

from slicer.fonction_vertices_face import *

from slicer.AdditionalFunction import Extremum,rad,extremum_layer

from slicer.fonction_presence import *

from slicer.fonction_vecteur import *

from math import ceil,cos,sin

from slicer.fonction_tri import tri

from slicer.fonction_generation_cordons import *

import copy

def regeneration_cordon(coord_cordon,cordon_contour,cordon_interieur,couche_min,couche_max,rayon,axe) :

    '''
    # cette fonction permet de v�rifier si les informations envoy�es � Monsieur JOURDAIN sont correctes; cette fonction reproduit le mesh correspondant � l'objet � partir des coordonn�es de cordons

    ##########################

    ##########
    # entr�e #
    ##########

    # coord_cordon (type list) : liste des coordon�es des cordons

    # cordon_contour (type bool) : si on veut faire appara�tre les cordons formant le contour

    # cordon_interieur (type bool) : si on veut faire appara�tre les cordons qui sont � l'int�rieur de la couche

    # couche_min (type int ou str) : num�ro de la premi�re couche prise ou "tout" dans le cas o� l'on veut l'int�gralit� de l'objet

    # couche_max (type int ou str) : num�ro de la derni�re couche prise ou "tout" dans le cas o� l'on veut l'int�gralit� de l'objet

    # rayon (type int ou float) : rayon des cordons

    # axe (type str) : axe orthogonal � la surface d�finie par le remplissage

    ##########
    # sortie #
    ##########

    # mesh (type list) : mesh correspondant � l'objet constitu� des cordons donn�s en entr�e

    ##########################'''

    mesh = []

    if couche_min == "tout" or couche_max == "tout" :

        couche_min = -1
        couche_max = len(coord_cordon)+1

    for i in range(len(coord_cordon)) :

        if cordon_contour :

            for j in range(len(coord_cordon[i][0])) :

                vecteur_directeur = operation_vecteur(coord_cordon[i][0][j][1],coord_cordon[i][0][j][0],"-")
                hauteur = norme_vecteur(vecteur_directeur)

                if hauteur != 0 and i >= couche_min and i <= couche_max :

                    cordon,coord = generer_cylindre_mesh(axe,rayon,hauteur,coord_cordon[i][0][j][0],vecteur_directeur,5,"cylindrique",False,"lineaire",1,"+",[0,0,0])

                    mesh += cordon

        if cordon_interieur :

            for j in range(len(coord_cordon[i][1])) :

                vecteur_directeur = operation_vecteur(coord_cordon[i][1][j][1],coord_cordon[i][1][j][0],"-")
                hauteur = norme_vecteur(vecteur_directeur)

                if hauteur != 0 and i >= couche_min and i <= couche_max :

                    cordon,coord = generer_cylindre_mesh(axe,rayon,hauteur,coord_cordon[i][1][j][0],vecteur_directeur,5,"cylindrique",False,"lineaire",1,"+",[0,0,0])

                    mesh += cordon


    return mesh

def maille_holographique(coord_cordon_1,coord_cordon_2,axe,parametre,trait_cordon,orthogonal_trait_cordon,rayon_cordon) :

    '''
    # cette fonction permet de g�n�rer des coordonn�es de cordons de mani�re � obtenir une surface holographique

    ##########################

    ##########
    # entr�e #
    ##########

    # coord_cordon_1 (type list) : liste des coordonn�es des cordons pour un remplissage dans une certaine direction

    # coord_cordon_2 (type list) : liste des coordonn�es des cordons pour un remplissage dans une certaine direction

    # axe (type str) : axe orthogonal � la surface d�finie par le remplissage

    # parametre (type int ou float) : param�tre de la maille holographique

    # trait_cordon (type list) : coordonn�es d'un vecteur colin�aire � la premi�re direction de remplissage sous le format [x,y,z]

    # orthogonal_trait_cordon (type list) : coordonn�es d'un vecteur colin�aire � la seconde direction de remplissage sous le format [x,y,z]

    # rayon_cordon (type int ou float) : rayon des cordons

    ##########
    # sortie #
    ##########

    # coord_cordon_origine (type list) : liste des coordonn�es des cordons pour un maillage holographique

    ##########################'''

    if axe == "x" :

        coordonnees = [1,2,0]
        unitaire = [1,0,0]
        axes = ["y","z"]
        direction_orthogonale = operation_vecteur(unitaire,trait_cordon,"vec")
        matrice_origine = mise_en_base(trait_cordon,unitaire,orthogonal_trait_cordon)
        matrice = inverse_matrice(matrice_origine)

    if axe == "y" :

        coordonnees = [2,0,1]
        unitaire = [0,1,0]
        axes = ["z","x"]
        direction_orthogonale = operation_vecteur(unitaire,trait_cordon,"vec")
        matrice_origine = mise_en_base(trait_cordon,unitaire,orthogonal_trait_cordon)
        matrice = inverse_matrice(matrice_origine)

    if axe == "z" :

        coordonnees = [0,1,2]
        unitaire = [0,0,1]
        axes = ["x","y"]
        direction_orthogonale = operation_vecteur(unitaire,trait_cordon,"vec")
        matrice_origine = mise_en_base(trait_cordon,unitaire,orthogonal_trait_cordon)
        matrice = inverse_matrice(matrice_origine)
    
    coord_cordon_nouvelle_base = []
    coord_cordon_nouvelle_base_2 = []

    for i in range(len(coord_cordon_1)) :

        coord_1 = prod_matriciel(matrice,coord_cordon_1[i][0])
        coord_2 = prod_matriciel(matrice,coord_cordon_1[i][1])
        
        
        if coord_1[0] <= coord_2[0] :
            coord_cordon_nouvelle_base.append([coord_1,coord_2])

        else :
            coord_cordon_nouvelle_base.append([coord_2,coord_1])

    for i in range(len(coord_cordon_2)) :

        coord_1_2 = prod_matriciel(matrice,coord_cordon_2[i][0])
        coord_2_2 = prod_matriciel(matrice,coord_cordon_2[i][1])

        if coord_1_2[2] <= coord_2_2[2] :
            coord_cordon_nouvelle_base_2.append([coord_1_2,coord_2_2])

        else :
            coord_cordon_nouvelle_base_2.append([coord_2_2,coord_1_2])

    extremum_mesh = extremum_layer(coord_cordon_nouvelle_base,[0,1,2])
    
    liste_point_relie = []
    liste_point_relie_2 = []

    for i in range(len(coord_cordon_nouvelle_base)):

        indice_min = extremum_mesh[1]
        indice_max = extremum_mesh[0]
        point = [coord_cordon_nouvelle_base[i][0]]

        while indice_min < indice_max :

            vecteur_directeur = operation_vecteur(coord_cordon_nouvelle_base[i][1],coord_cordon_nouvelle_base[i][0],"-")
            
            if vecteur_directeur[0] == 0 :
                coefficient = 0

            if vecteur_directeur[0] != 0 :
                coefficient = float(indice_min-coord_cordon_nouvelle_base[i][0][0])/vecteur_directeur[0]

            if indice_min > coord_cordon_nouvelle_base[i][0][0] and indice_min < coord_cordon_nouvelle_base[i][1][0] and coefficient != 0 :

                if len(point) == 2 :

                    liste_point_relie.append(point)
                    point = [liste_point_relie[-1][1]]

                if len(point)< 2 :

                    chemin = operation_vecteur(vecteur_directeur,coefficient,"*")
                    point_2 = operation_vecteur(coord_cordon_nouvelle_base[i][0],chemin,"+")

                    if not comparaison_vecteur(point_2,point[0],0.01) :

                        point.append(operation_vecteur(coord_cordon_nouvelle_base[i][0],chemin,"+"))

            indice_min += parametre

        if len(point) == 1 :

            point.append(coord_cordon_nouvelle_base[i][1])
            liste_point_relie.append(point)

        if len(point) == 0 :
            
            liste_point_relie.append([liste_point_relie[-1][1],coord_cordon_nouvelle_base[i][1]])

        if len(point) == 2 :
            
            point_2 = [point[1],coord_cordon_nouvelle_base[i][1]]
            liste_point_relie.append(point)
            liste_point_relie.append(point_2)

    for i in range(len(coord_cordon_nouvelle_base_2)):

        indice_min = extremum_mesh[5]
        indice_max = extremum_mesh[4]
        point = [coord_cordon_nouvelle_base_2[i][0]]

        while indice_min < indice_max :

            vecteur_directeur = operation_vecteur(coord_cordon_nouvelle_base_2[i][1],coord_cordon_nouvelle_base_2[i][0],"-")

            if vecteur_directeur[2] == 0 :
                coefficient = 0

            if vecteur_directeur[2] != 0 :
                coefficient = float(indice_min-coord_cordon_nouvelle_base_2[i][0][2])/vecteur_directeur[2]

            if indice_min > coord_cordon_nouvelle_base_2[i][0][2] and indice_min < coord_cordon_nouvelle_base_2[i][1][2] and coefficient != 0 :
                
                if len(point) == 2 :

                    liste_point_relie_2.append(point)
                    point = [liste_point_relie_2[-1][1]]

                if len(point)< 2 :

                    chemin = operation_vecteur(vecteur_directeur,coefficient,"*")
                    point_2 = operation_vecteur(coord_cordon_nouvelle_base_2[i][0],chemin,"+")

                    if not comparaison_vecteur(point_2,point[0],0.01) :

                        point.append(point_2)
                    
            indice_min += parametre

        if len(point) == 1 :

            point.append(coord_cordon_nouvelle_base_2[i][1])
            liste_point_relie_2.append(point)

        if len(point) == 0 :
            
            liste_point_relie_2.append([liste_point_relie_2[-1][1],coord_cordon_nouvelle_base_2[i][1]])

        if len(point) == 2 :
            
            point_2 = [point[1],coord_cordon_nouvelle_base_2[i][1]]
            liste_point_relie_2.append(point)
            liste_point_relie_2.append(point_2)

    indice_min_1 = extremum_mesh[1]
    indice_max_1 = extremum_mesh[0]
    indice_min_2 = extremum_mesh[5]
    indice_max_2 = extremum_mesh[4]

    j = 0

    coord_cordon = []

    while indice_min_1 <= indice_max_1 :
        
        indice_min_22 = indice_min_2
        
        while indice_min_22 <= indice_max_2 :

            if j%2 == 0 :

                for i in range(len(liste_point_relie)) :

                    if liste_point_relie[i][0][0] >= indice_min_1-float(rayon_cordon)/3 and liste_point_relie[i][0][0] < indice_min_1+parametre-float(rayon_cordon)/3 and liste_point_relie[i][0][2] >= indice_min_22-float(rayon_cordon)/3 and liste_point_relie[i][0][2] < indice_min_22+parametre-float(rayon_cordon)/3 :

                        coord_cordon.append(liste_point_relie[i])

            if j%2 != 0 :

                for i in range(len(liste_point_relie_2)) :

                    if liste_point_relie_2[i][0][0] >= indice_min_1-float(rayon_cordon)/3 and liste_point_relie_2[i][0][0] < indice_min_1+parametre-float(rayon_cordon)/3 and  liste_point_relie_2[i][0][2] >= indice_min_22-float(rayon_cordon)/3 and liste_point_relie_2[i][0][2] < indice_min_22+parametre-float(rayon_cordon)/3 :

                        coord_cordon.append(liste_point_relie_2[i])

            indice_min_22 += parametre
            j += 1
            
        indice_min_1 += parametre
        j += 1

    coord_cordon_origine = []

    for i in range(len(coord_cordon)):

        coord_x = prod_matriciel(matrice_origine,coord_cordon[i][0])
        coord_y = prod_matriciel(matrice_origine,coord_cordon[i][1])
        vecteur_directeur = operation_vecteur(coord_x,coord_y,"-")
        

        if not comparaison_vecteur(vecteur_directeur,[0,0,0],0.0001) :

            coord_cordon_origine.append([coord_x,coord_y])                   

    return coord_cordon_origine




def recuperation_layer_niveau(mesh,axe,niveau,signe,precision) :
    '''
    # cette fonction permet de r�cup�rer les coordonn�es des points appartenant � un certain niveau

    ##########################

    ##########
    # entr�e #
    ##########

    # mesh (type list) : liste sous le format d�fini par la fonction load_mesh

    # axe (type str) : correspond � la direction selon laquelle le niveau est d�fini

    # niveau (type int ou float) : coorespond � la coordonn�e "niveau" selon l'entr�e axe 

    # precision (type int ou float) : pr�cision souhait�e

    ##########
    # sortie #
    ##########

    # diamant_mesh (type list) : liste de couples de coordonn�es de points cons�cutifs du contour, ainsi que de la normale dirig�e vers l'ext�rieur sous le format [([x1,y1,z1],[x2,y2,z2],[nx,ny,nz]),...]

    ##########################'''
    
    xmax,xmin,ymax,ymin,zmax,zmin=Extremum(mesh)

    if axe == "x" :

        coordonnees = [1,2,0]
        
        if signe == "-" :
            x = niveau-10
        else :
            x = niveau+10

        point = [x,(ymax+ymin)/2.0,(zmax+zmin)/2.0]

    if axe == "y" :
        
        coordonnees = [0,2,1]

        if signe == "-" :
            y = niveau-10
        else :
            y = niveau+10

        point = [(xmax+xmin)/2.0,y,(zmax+zmin)/2.0]

    if axe == "z" :
        
        coordonnees = [0,1,2]

        if signe == "-" :
            z = niveau-10
        else :
            z = niveau+10

        point = [(xmax+xmin)/2.0,(ymax+ymin)/2.0,z]
        
    diamant_mesh = []

    for i in range(len(mesh)) :
        
        num_point_niveau,point_niveau = compte_point_niveau(mesh[i][1],coordonnees[2],niveau,precision)
        
        if num_point_niveau == 2 :

            ######################## dans le cas d'un mauvais arrondi mais acceptable pour la pr�cision donn�e ###########################

            if point_niveau[0][coordonnees[2]] != niveau :
    
                point_niveau[0][coordonnees[2]] = niveau

            if point_niveau[1][coordonnees[2]] != niveau :

                point_niveau[1][coordonnees[2]] = niveau

            ######################################################################################

            vecteur_normal_2 = mesh[i][0]
            vecteur_normal_2[coordonnees[2]] = 0
                
            diamant_mesh.append((point_niveau[0],point_niveau[1],vecteur_normal_2))

    return diamant_mesh

def Create_contour_cordon(layer,N_facette_cordon,axe,rayon_cordon,type_cordon,avec_extremite) :
    '''
    # cette fonction permet de cr�er un objet mesh qui repr�sentera un cordon cylindrique passant par tous les points du contour "layer"

    ##########################

    ##########
    # entr�e #
    ##########

    # layer (type list) : liste de couples de coordonn�es de points cons�cutifs du contour, ainsi que de la normale dirig�e vers l'ext�rieur sous le format [([x1,y1,z1],[x2,y2,z2],[nx,ny,nz]),...]

    # N_facette_cordon (type int) : le nombre de sommets du polygone r�gulier d�finissant la base du "cylindre" repr�sentant le cordon

    # axe (type str) : correspond � la direction colin�aire � la normale de la surface d�finie par le contour "layer"

    # rayon_cordon (type int ou float) : correspond au rayon du cylindre repr�sentant le cordon

    # type_cordon (type str) : "cylindrique" pour avoir des cordons cylindriques ou "clavette" pour avoir des cordons l�g�rement aplatis

    # avec_extremite (type bool) : si on veut les extr�mit�s des cordons

    ##########
    # sortie #
    ##########

    # mesh (type list) : liste sous le format d�fini par la fonction load_mesh

    # liste_coordonnee_cordons (type list) : liste dont chaque sous liste comporte en premier item les coordonn�es du premier centre d'un cordon et en second item le second centre du cordon
    
    ##########################'''    

    mesh = []
    liste_coordonnee_cordons = []

    for i in range(len(layer)) :

        centre_base = layer[i][0]
        trait_cordon = operation_vecteur(layer[i][1],layer[i][0],"-")
        hauteur = norme_vecteur(trait_cordon)

        if trait_cordon != [0.0,0.0,0.0] :
            
            cordon,liste_coord_centre = generer_cylindre_mesh(axe,rayon_cordon,hauteur,centre_base,trait_cordon,N_facette_cordon,type_cordon,avec_extremite,"lineaire",0,"+",0)

            mesh += cordon
        
            liste_coordonnee_cordons += liste_coord_centre
        

    return mesh,liste_coordonnee_cordons

def Create_sous_contour(layer,axe,reduction,precision) :
    '''
    # cette fonction permet � partir d'un contour de cr�er un sous-contour qui est une r�duction du contour

    ##########################

    ##########
    # entr�e #
    ##########

    # layer (type list) : liste de couples de coordonn�es de points cons�cutifs du contour, ainsi que de la normale dirig�e vers l'ext�rieur sous le format [([x1,y1,z1],[x2,y2,z2],[nx,ny,nz]),...]

    # axe (type str) : correspond � la direction orthogonale au plan d�fini par le contour "layer"

    # reduction (type int ou float) : correspond au facteur de r�duction du contour, il peut �tre n�gatif pour un agrandissement 

    # precision (type int ou float) : pr�cision souhait�e

    ##########
    # sortie #
    ##########

    # under_layer (type list) : liste de couples de coordonn�es de points cons�cutifs du contour, ainsi que de la normale dirig�e vers l'ext�rieur sous le format [([x1,y1,z1],[x2,y2,z2],[nx,ny,nz]),...]

    ##########################'''

    if axe == "x" :

        coordonnees = [1,2,0]

    if axe == "y" :

        coordonnees = [0,2,1]

    if axe == "z" :

        coordonnees = [0,1,2]

    under_layer = []

    for i in range(len(layer)) :

        point_1 = layer[i][0]
        point_2 = layer[i][1]
        point_1_adjacent = []
        point_2_adjacent = []

        for j in range(len(layer)) :

            if comparaison_vecteur(layer[j][1],point_1,precision) or  comparaison_vecteur(layer[j][0],point_1,precision):

                point_1_adjacent.append(layer[j][2])

            if comparaison_vecteur(layer[j][0],point_2,precision) or comparaison_vecteur(layer[j][1],point_2,precision) :

                point_2_adjacent.append(layer[j][2])
                
        normale_1_1 = operation_vecteur(point_1_adjacent[0],float(norme_vecteur(point_1_adjacent[0]))/(-1*reduction),"/")
        normale_1_2 = operation_vecteur(point_1_adjacent[1],float(norme_vecteur(point_1_adjacent[1]))/(-1*reduction),"/")
        normale_2_1 = operation_vecteur(point_2_adjacent[0],float(norme_vecteur(point_2_adjacent[0]))/(-1*reduction),"/")
        normale_2_2 = operation_vecteur(point_2_adjacent[1],float(norme_vecteur(point_2_adjacent[1]))/(-1*reduction),"/")

        chemin_1 = operation_vecteur(normale_1_1,normale_1_2,"+")
        chemin_2 = operation_vecteur(normale_2_1,normale_2_2,"+")

        nouveau_point_1 = operation_vecteur(point_1,chemin_1,"+")

        nouveau_point_2 = operation_vecteur(point_2,chemin_2,"+")

        under_layer.append((nouveau_point_1,nouveau_point_2,layer[i][2]))

    return under_layer 





def trait_de_coupe(width,hauteur_de_coupe,coupe_au_centre) :
    '''
    # cette fonction permet de g�n�rer un trait
    # de la m�me hauteur que la taille des tranches
    # et au niveau de la tranche souhait�e avec un choix de hauteur
    # de coupe soit au centre du trait soit �
    # l'ordonn�e zmin du trait

    ##########################

    ##########
    # entr�e #
    ##########

    # width (type int ou float) : correspond � l'�paisseur de la tranche

    # hauteur_de_coupe (type int ou float) : correspond au niveau o� la tranche commence

    # coupe_au_centre (type bool) : si la coupe est au niveau de la hauteur de coupe + (�paisseur de la tranche)/2

    ##########
    # sortie #
    ##########

    # trait (type list) : liste dont le premier item correspond � la coordonn�e du d�but de coupe, le second item coorrespond � la coordonn�e de fin de coupe

    ##########################'''

    if coupe_au_centre :

        trait = [hauteur_de_coupe-width/2.0,hauteur_de_coupe+width/2.0]
        return trait

    trait = [hauteur_de_coupe,hauteur_de_coupe+width]
    return trait

def point_en_commun(facette1,facette2):
    '''
    # cette fonction permet de savoir combien de points ont en commun deux facettes

    ##########################

    ##########
    # entr�e #
    ##########

    # facette1 (type list): correspond � la liste des coordonn�es des trois sommets appartenant � la facette sous le format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]

    # facette2 (type list): correspond � la liste des coordonn�es des trois sommets appartenant � la facette sous le format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]    

    ##########
    # sortie #
    ##########

    # num_point_en_commun (type int) : le nombre de points en commun entre les facettes donn�es en entr�e

    # la pr�cision est � 0.001 de l'unit� utilis�e

    ##########################'''

    num_point_en_commun = 0
    deja_compte = 0

    for i in range(len(facette1)) :

        vecteur = operation_vecteur(facette1[i],facette2[0],"-")

        if comparaison_vecteur(vecteur,[0,0,0],0.001) and deja_compte == 0 :

            num_point_en_commun += 1
            deja_compte = 1

    deja_compte = 0

    for i in range(len(facette1)) :

        vecteur = operation_vecteur(facette1[i],facette2[1],"-")

        if comparaison_vecteur(vecteur,[0,0,0],0.001) and deja_compte == 0 :

            num_point_en_commun += 1
            deja_compte = 1

    deja_compte = 0

    for i in range(len(facette1)) :

        vecteur = operation_vecteur(facette1[i],facette2[2],"-")

        if comparaison_vecteur(vecteur,[0,0,0],0.001) and deja_compte == 0 :

            num_point_en_commun += 1
            deja_compte = 1

    return num_point_en_commun

        


def compte_point_niveau(facette,coordonnee,niveau,precision) :
    '''
    # cette fonction compte le nombre de points d'une facette qui sont � un certain niveau pour une coordonn�e donn�e

    ##########################

    ##########
    # entr�e #
    ##########

    # facette (type list): correspond � la liste des coordonn�es des trois sommets appartenant � la facette sous le format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]

    # coordonnee (type int ou float) : indice de la coordonn�e compar�e

    # niveau (type int ou float) : valeur correspondant au niveau

    # precision (type int ou float) : pr�cision souhait�e

    ##########
    # sortie #
    ##########

    # num_point_au_niveau (type int) : le nombre de points dont la coordonn�e choisie correspond au niveau demand�

    # point_au_niveau (type list) : liste des coordonn�es des points au niveau sous le foramt [[x1,y1,z1],[x2,y2,z2],...]

    ##########################'''

    num_point_au_niveau = 0
    point_au_niveau = []

    for i in range(len(facette)) :

        if abs(facette[i][coordonnee]-niveau) <= precision :

            point_au_niveau.append(facette[i])
            num_point_au_niveau += 1

    return num_point_au_niveau,point_au_niveau






    


    



def Create_cordon(layer,axe,width,hauteur_de_coupe,coupe_au_centre,trait_cordon,N_facette_cordon,rayon_cordon,overlap_entre_cordons,type_cordon,avec_extremite,type_maille,parametre_de_maille) :
    '''
    # cette fonction permet de retourner les cordons qui vont remplir la couche ainsi que leurs coordonn�es

    ##########################

    ##########
    # entr�e #
    ##########

    # layer (type list): : liste de couples de coordonn�es de points cons�cutifs du contour, ainsi que de la normale dirig�e vers l'ext�rieur sous le format [([x1,y1,z1],[x2,y2,z2],[nx,ny,nz]),...]

    # axe (type str) : direction orthogonale au plan d�fini par le contour "layer"

    # width (type int ou float) : �paisseur de la couche

    # hauteur_de_coupe (type int ou float) : niveau auquel on coupe

    # coupe_au_centre (type bool) : si on coupe au centre par rapport � la hauteur de coupe

    # trait_cordon (type list) : coordonn�es du vecteur orientation des cordons sous le format [x,y,z]

    # N_facette_cordon (type int) : nombre de sommets du polygone qui d�finira la base des cylindres repr�sentant les cordons

    # rayon_cordon (type int ou float) : rayon des cylindres repr�sentant les cordons

    # overlap_entre_cordons (type int ou float) : espace entre chaque cordon

    # type_cordon (type str) : "cylindrique" pour avoir des cordons cylindriques ou "clavette", ou "ellipse" pour avoir des cordons l�g�rement aplatis

    # avec_extremite (type bool) : si on veut les extr�mit�s des cordons

    # type_maille (type list) : le premier item correspond au type de la maille, "lineaire", "losange", "hexagonale". Le second correspond au caract�re crois� ou non , "croisee" ou "decroisee"

    # parametre_de_maille (type int ou float) : param�tre de la maille

    ##########
    # sortie #
    ##########

    # mesh_tout_cordons (type list) : liste repr�sentant les cordons sous le format d�fini par la fonction load_mesh

    # mesh_liste_cordons (type list) : liste des coordonn�es des diff�rents cordons avec pour chaque cordon une liste des coordonn�es du point de d�part et du point d'arriv�e

    ##########################'''

    type_de_maille = type_maille[0]
    caractere_maille = type_maille[1]
    mesh_tous_cordons = []
    mesh_liste_cordons = []

    if coupe_au_centre :

        hauteur_cordon = hauteur_de_coupe

    if not coupe_au_centre :

        hauteur_cordon = hauteur_de_coupe #+width/2 # je pensais qu'il fallait mettre �a pour ne pas que les cordons se chevauchent
    
    if axe == "x" :
        
        coordonnees = [1,2,0]
        direction_axe = [1,0,0]

    if axe == "y" :
        
        coordonnees = [0,2,1]
        direction_axe = [0,1,0]

    if axe == "z" :
        
        coordonnees = [0,1,2]
        direction_axe = [0,0,1]

    layer_nouvelle_base = []

    direction_orthogonale = operation_vecteur(direction_axe,trait_cordon,"vec")

    matrice_vers_base_origine = mise_en_base(trait_cordon,direction_orthogonale,direction_axe)
    matrice_vers_nouvelle_base = inverse_matrice(matrice_vers_base_origine)

    for point in range(len(layer)) :

        couple_point = []

        couple_point.append(prod_matriciel(matrice_vers_nouvelle_base,layer[point][0]))
        couple_point.append(prod_matriciel(matrice_vers_nouvelle_base,layer[point][1]))        

        layer_nouvelle_base.append(couple_point)

    xMax,xMin,yMax,yMin,zMax,zMin = extremum_layer(layer_nouvelle_base,[0,1,2])

    longueur_translation = yMax-yMin

    N_cordons = int(ceil(float(longueur_translation)/(2*rayon_cordon+overlap_entre_cordons)))

    point_depart = [xMin,yMin,zMin]

    

    for i in range(N_cordons) :

        liste_point_intersection = []

        for j in range(len(layer_nouvelle_base)) :

            if (point_depart[1] <= layer_nouvelle_base[j][0][1] and point_depart[1] >= layer_nouvelle_base[j][1][1]) or (point_depart[1] <= layer_nouvelle_base[j][1][1] and point_depart[1] >= layer_nouvelle_base[j][0][1]) :

                # il y a un point d'intersection

                if point_depart[1] != layer_nouvelle_base[j][0][1] or point_depart[1] != layer_nouvelle_base[j][1][1] :

                    # pour eviter que le cordon soit confondus sur le bord

                    vecteur_directeur = operation_vecteur(layer_nouvelle_base[j][0],layer_nouvelle_base[j][1],"-")
                    coef = float(point_depart[1]-layer_nouvelle_base[j][0][1])/vecteur_directeur[1]

                    coordonnee_x = coef*vecteur_directeur[0]+layer_nouvelle_base[j][0][0]

                    point_intersection_nouvelle_base = [coordonnee_x,point_depart[1],hauteur_cordon]
                    point_intersection_base_origine = prod_matriciel(matrice_vers_base_origine,point_intersection_nouvelle_base)
                    
                    vecteur_distance = operation_vecteur(point_depart,point_intersection_nouvelle_base,"-")
                    distance_point_origine = norme_vecteur(vecteur_distance)

                

                    liste_point_intersection.append([point_intersection_base_origine,distance_point_origine])

        liste_triee = tri(liste_point_intersection,"+",1)

        for j in range(len(liste_triee)) :

                if j%2 == 0 :

                    if j<len(liste_triee)-1 :

                        vect = operation_vecteur(liste_triee[j][0],liste_triee[j+1][0],"-")

                        hauteur = norme_vecteur(vect)
                        centre_base = liste_triee[j][0]

                        if caractere_maille == "croisee" :

                            if i%2 == 0 :
                                
                                cordon,liste_coord_centre = generer_cylindre_mesh(axe,rayon_cordon,hauteur,centre_base,trait_cordon,N_facette_cordon,type_cordon,avec_extremite,type_de_maille,parametre_de_maille,"+",yMin)
                                
                            if i%2 != 0 :

                                cordon,liste_coord_centre = generer_cylindre_mesh(axe,rayon_cordon,hauteur,centre_base,trait_cordon,N_facette_cordon,type_cordon,avec_extremite,type_de_maille,parametre_de_maille,"-",yMin)

                        if caractere_maille == "decroisee" :

                                cordon,liste_coord_centre = generer_cylindre_mesh(axe,rayon_cordon,hauteur,centre_base,trait_cordon,N_facette_cordon,type_cordon,avec_extremite,type_de_maille,parametre_de_maille,"+",yMin)
                            
                        mesh_liste_cordons += liste_coord_centre
                        mesh_tous_cordons = mesh_tous_cordons + cordon
                
                
        point_depart[1] += 2*rayon_cordon+overlap_entre_cordons

    return mesh_tous_cordons,mesh_liste_cordons

def recuperation_tranche(mesh,width,hauteur_de_coupe,coupe_au_centre,axe) :
    '''
    # cette fonction permet de retourner  un mesh correspond � la tranche de l'objet "mesh" pour un niveau donn� et un axe de d�coupe

    ##########################

    ##########
    # entr�e #
    ##########

    # mesh (type list) : liste sous le format d�fini par la fonction load_mesh

    # width (type int ou float) : �paisseur de la tranche

    # hauteur_de_coupe (type int ou float) : niveau auquel on coupe

    # coupe_au_centre (type bool) : si on coupe au centre par rapport � la hauteur de coupe

    # axe (type str) : axe de d�coupe

    ##########
    # sortie #
    ##########

    # coupe_mesh (type list) : liste repr�sentant la tranche sous le format d�fini par la fonction load_mesh

    ##########################'''

    facette = face(mesh)
    sommet = vertices(mesh)
    normal = normale(mesh)
    trait = trait_de_coupe(width,hauteur_de_coupe,coupe_au_centre)
    coupe_mesh = []

    if axe == "x" :

        axe_coupe = 0

    if axe == "y" :

        axe_coupe = 1

    if axe == "z" :

        axe_coupe = 2

    for faces in facette :
        check = ["OK","OK","OK"]
        compteur = 0
        sommet_facette = [sommet[faces[0]],sommet[faces[1]],sommet[faces[2]]]

        for indice in faces :
            point = sommet[indice]

            if point[axe_coupe] < trait[0] or point[axe_coupe] > trait[1] :

                check[compteur] = "NOK"

            compteur += 1        

        if check == ["OK","OK","OK"] :

            # toute la facette est dans la tranche de coupe "

            coupe_mesh.append(mesh[facette.index(faces)])

        if check != ["OK","OK","OK"] :

            # au moins un des sommets de la facette n'est pas dans la tranche

            if if_facette_traverse_couche(sommet_facette,trait,axe) :

                # la facette traverse la tranche

                sommets_nouvelle_facette = []

                if check.count("OK") == 0 :

                    # si tous les sommets de la facette sont hors de la tranche
                
                    for indexe in [[0,1],[1,2],[2,0]]:

                        if if_droite_traverse_couche(sommet_facette[indexe[0]],sommet_facette[indexe[1]],trait,axe) :

                            vecteur_directeur = vecteur_droite(sommet_facette[indexe[0]],sommet_facette[indexe[1]])
                            coefficient1 = (trait[0]-sommet_facette[indexe[0]][axe_coupe])/float(vecteur_directeur[axe_coupe])
                            coefficient2 = (trait[1]-sommet_facette[indexe[0]][axe_coupe])/float(vecteur_directeur[axe_coupe])

                            if abs(coefficient1)<abs(coefficient2) :

                                sommets_nouvelle_facette.append(operation_vecteur(sommet_facette[indexe[0]],operation_vecteur(vecteur_directeur,coefficient1,"*"),"+"))
                                sommets_nouvelle_facette.append(operation_vecteur(sommet_facette[indexe[0]],operation_vecteur(vecteur_directeur,coefficient2,"*"),"+"))

                            else :

                                sommets_nouvelle_facette.append(operation_vecteur(sommet_facette[indexe[0]],operation_vecteur(vecteur_directeur,coefficient2,"*"),"+"))
                                sommets_nouvelle_facette.append(operation_vecteur(sommet_facette[indexe[0]],operation_vecteur(vecteur_directeur,coefficient1,"*"),"+"))

                    facette_1 = [sommets_nouvelle_facette[0],sommets_nouvelle_facette[1],sommets_nouvelle_facette[2]]
                    facette_2 = [sommets_nouvelle_facette[2],sommets_nouvelle_facette[3],sommets_nouvelle_facette[0]]

                    coupe_mesh.append([mesh[facette.index(faces)][0],facette_1])
                    coupe_mesh.append([mesh[facette.index(faces)][0],facette_2])

                if check.count("OK") == 1 :

                    # si un seul sommet de la facette est dans la tranche

                    recuperer_point_in_couche = 0
                    
                    for indexe in [[0,1],[1,2],[2,0]]:

                        if if_droite_traverse_couche(sommet_facette[indexe[0]],sommet_facette[indexe[1]],trait,axe) :

                            vecteur_directeur = vecteur_droite(sommet_facette[indexe[0]],sommet_facette[indexe[1]])

                            if if_point_in_couche(sommet_facette[indexe[0]],trait,axe) :
                                
                                if trait[0] > min(sommet_facette[indexe[0]][axe_coupe],sommet_facette[indexe[1]][axe_coupe]) :

                                    coefficient = (trait[0]-sommet_facette[indexe[0]][axe_coupe])/float(vecteur_directeur[axe_coupe])

                                if trait[0] <= min(sommet_facette[indexe[0]][axe_coupe],sommet_facette[indexe[1]][axe_coupe]) :

                                    coefficient = (trait[1]-sommet_facette[indexe[0]][axe_coupe])/float(vecteur_directeur[axe_coupe])

                                if coefficient != 0 :

                                    sommets_nouvelle_facette.append(operation_vecteur(sommet_facette[indexe[0]],operation_vecteur(vecteur_directeur,coefficient,"*"),"+"))

                                if recuperer_point_in_couche == 0 :

                                    sommets_nouvelle_facette.append(sommet_facette[indexe[0]])
                                    recuperer_point_in_couche = 1
                                    

                            else :

                                if not de_part_et_autre([sommet_facette[indexe[0]],sommet_facette[indexe[1]]],trait,axe) :

                                    if trait[0] > min(sommet_facette[indexe[0]][axe_coupe],sommet_facette[indexe[1]][axe_coupe]) :

                                        coefficient = (trait[0]-sommet_facette[indexe[1]][axe_coupe])/float(vecteur_directeur[axe_coupe])

                                    if trait[0] <= min(sommet_facette[indexe[0]][axe_coupe],sommet_facette[indexe[1]][axe_coupe]) :

                                        coefficient = (trait[1]-sommet_facette[indexe[1]][axe_coupe])/float(vecteur_directeur[axe_coupe])

                                    if coefficient != 0 :

                                        sommets_nouvelle_facette.append(operation_vecteur(sommet_facette[indexe[1]],operation_vecteur(vecteur_directeur,coefficient,"*"),"+"))

                                    if recuperer_point_in_couche == 0 :

                                        sommets_nouvelle_facette.append(sommet_facette[indexe[1]])
                                        recuperer_point_in_couche = 1

                                if de_part_et_autre([sommet_facette[indexe[0]],sommet_facette[indexe[1]]],trait,axe) :

                                    coefficient_1 = (trait[0]-sommet_facette[indexe[0]][axe_coupe])/float(vecteur_directeur[axe_coupe])
                                    coefficient_2 = (trait[1]-sommet_facette[indexe[0]][axe_coupe])/float(vecteur_directeur[axe_coupe])

                                    if abs(coefficient_1) <= abs(coefficient_2) :

                                        sommets_nouvelle_facette.append(operation_vecteur(sommet_facette[indexe[0]],operation_vecteur(vecteur_directeur,coefficient_1,"*"),"+"))
                                        sommets_nouvelle_facette.append(operation_vecteur(sommet_facette[indexe[0]],operation_vecteur(vecteur_directeur,coefficient_2,"*"),"+"))

                                    else :

                                        sommets_nouvelle_facette.append(operation_vecteur(sommet_facette[indexe[0]],operation_vecteur(vecteur_directeur,coefficient_2,"*"),"+"))
                                        sommets_nouvelle_facette.append(operation_vecteur(sommet_facette[indexe[0]],operation_vecteur(vecteur_directeur,coefficient_1,"*"),"+"))

                    if len(sommets_nouvelle_facette) == 3 :

                        coupe_mesh.append([mesh[facette.index(faces)][0],sommets_nouvelle_facette])

                    if len(sommets_nouvelle_facette) == 4 :

                        facette_1 = [sommets_nouvelle_facette[0],sommets_nouvelle_facette[3],sommets_nouvelle_facette[1]]
                        facette_2 = [sommets_nouvelle_facette[1],sommets_nouvelle_facette[3],sommets_nouvelle_facette[2]]

                        coupe_mesh.append([mesh[facette.index(faces)][0],facette_1])
                        coupe_mesh.append([mesh[facette.index(faces)][0],facette_2])

                    if len(sommets_nouvelle_facette) == 5 :

                        while not (sommets_nouvelle_facette[0][axe_coupe] < trait[1] and sommets_nouvelle_facette[0][axe_coupe] > trait[0]) :

                            point_a_deplacer = sommets_nouvelle_facette[0]

                            sommets_nouvelle_facette.pop(0)

                            sommets_nouvelle_facette.append(point_a_deplacer)

                        facette_1 = [sommets_nouvelle_facette[0],sommets_nouvelle_facette[1],sommets_nouvelle_facette[4]]
                        facette_2 = [sommets_nouvelle_facette[1],sommets_nouvelle_facette[2],sommets_nouvelle_facette[4]]
                        facette_3 = [sommets_nouvelle_facette[2],sommets_nouvelle_facette[3],sommets_nouvelle_facette[4]]

                        coupe_mesh.append([mesh[facette.index(faces)][0],facette_1])
                        coupe_mesh.append([mesh[facette.index(faces)][0],facette_2])
                        coupe_mesh.append([mesh[facette.index(faces)][0],facette_3])                    

                if check.count("OK") == 2 :

                    # si deux sommets de la facette sont dans la tranche

                    for indexe in [[0,1],[1,2],[2,0]]:

                        if if_deux_points_in_couche(sommet_facette[indexe[0]],sommet_facette[indexe[1]],trait,axe) :

                            sommets_nouvelle_facette.append(sommet_facette[indexe[0]])
                            sommets_nouvelle_facette.append(sommet_facette[indexe[1]])

                        else :

                            vecteur_directeur = vecteur_droite(sommet_facette[indexe[0]],sommet_facette[indexe[1]])
                            
                            if trait[0] > min(sommet_facette[indexe[0]][axe_coupe],sommet_facette[indexe[1]][axe_coupe]) :

                                coefficient = (trait[0]-sommet_facette[indexe[0]][axe_coupe])/float(vecteur_directeur[axe_coupe])

                            if trait[0] <= min(sommet_facette[indexe[0]][axe_coupe],sommet_facette[indexe[1]][axe_coupe]) :

                                coefficient = (trait[1]-sommet_facette[indexe[0]][axe_coupe])/float(vecteur_directeur[axe_coupe])

                            sommets_nouvelle_facette.append(operation_vecteur(sommet_facette[indexe[0]],operation_vecteur(vecteur_directeur,coefficient,"*"),"+"))
                    
                    facette_1 = [sommets_nouvelle_facette[0],sommets_nouvelle_facette[1],sommets_nouvelle_facette[2]]
                    facette_2 = [sommets_nouvelle_facette[2],sommets_nouvelle_facette[3],sommets_nouvelle_facette[0]]


                    coupe_mesh.append([mesh[facette.index(faces)][0],facette_1])
                    coupe_mesh.append([mesh[facette.index(faces)][0],facette_2])

    return coupe_mesh

    

def slice_couche(mesh,width,hauteur_de_coupe,coupe_au_centre,axe,angle,N_facette_cordon,rayon_cordon,overlap_entre_cordons,overlap_entre_cordons_contour,type_cordon,avec_extremite,type_maille,parametre_de_maille,holographique,parametre) :
    '''
    # cette fonction permet de retourner  un mesh correspond � la tranche remplie de cordons de l'objet "mesh" pour un niveau donn� et un axe de d�coupe ainsi que les coordonn�es des cordons

    ##########################

    ##########
    # entr�e #
    ##########

    # mesh (type list) : liste sous le format d�fini par la fonction load_mesh

    # width (type int ou float) : �paisseur de la tranche

    # hauteur_de_coupe (type int ou float) : niveau auquel on coupe

    # coupe_au_centre (type bool) : si on coupe au centre par rapport � la hauteur de coupe

    # axe (type str) : axe de d�coupe

    # angle (type int ou float) : angle d�fini entre l'axe de d�coupe et la direction d�finie par les cordons

    # N_facette_cordon (type int) : nombre de sommets du polygone qui d�finira la base des cylindres repr�sentant les cordons

    # rayon_cordon (type int ou float) : rayon des cylindres repr�sentant les cordons

    # overlap_entre_cordons (type int ou float) : espace entre chaque cordon

    # overlap_entre_cordons_contour (type int ou float) : espace entre le cordon d�finissant le contour de la tranche et entre les cordons � l'int�rieur du contour de la tranche

    # type_cordon (type str) : "cylindrique" pour avoir des cordons cylindriques ou "clavette", ou "ellipse" pour avoir des cordons l�g�rement aplatis

    # avec_extremite (type bool) : si on veut les extr�mit�s des cordons

    # type_maille (type list) : le premier item correspond au type de la maille, "lineaire", "losange", "hexagonale","aleatoire". Le second correspond au caract�re crois� ou non , "croisee" ou "decroisee"

    # parametre_de_maille (type int ou float) : param�tre de la maille

    # holographique (type bool) : si on veut une surface holographique

    # parametre (type int ou float) : param�tre de la maille holographique

    ##########
    # sortie #
    ##########

    # mesh_entier (type list) : liste repr�sentant les cordons de la tranche sous le format d�fini par la fonction load_mesh

    # liste_coordonnees_cordons_tranche (type list) : liste des coordonn�es des diff�rents cordons de la tranche avec pour chaque cordon une liste des coordonn�es du point de d�part et du point d'arriv�e

    ##########################'''

    angle_rad = rad(angle)

    liste_coordonnees_cordons_tranche = [[],[]]

    trait = trait_de_coupe(width,hauteur_de_coupe,coupe_au_centre)

    extremum_mesh = Extremum(mesh)

    if axe == "x" :

        point_verifier = [extremum_mesh[0],extremum_mesh[1]]
        trait_cordon = [0,cos(angle_rad),sin(angle_rad)]
        unitaire = [1,0,0]

    if axe == "y" :

        point_verifier = [extremum_mesh[2],extremum_mesh[3]]
        trait_cordon = [sin(angle_rad),0,cos(angle_rad)]
        unitaire = [0,1,0]

    if axe == "z" :

        point_verifier = [extremum_mesh[4],extremum_mesh[5]]
        trait_cordon = [sin(angle_rad),cos(angle_rad),0]
        unitaire = [0,0,1]

    coupe_mesh = recuperation_tranche(mesh,width,hauteur_de_coupe,coupe_au_centre,axe)

    mesh_entier = []

    if point_verifier[1] <= trait[0] and len(coupe_mesh) != 0 :

        #tranche_de_mesh_inf = Create_diamant(coupe_mesh,trait[0],axe,"-",False,float(width)/1000)
        
        #layer_inf = Create_contour_diamant(tranche_de_mesh_inf,axe,trait[0],float(width)/1000)

        layer_inf = recuperation_layer_niveau(coupe_mesh,axe,trait[0],"-",float(width)/1000)        

        if len(layer_inf) != 0 :

            try :
                under_layer = Create_sous_contour(layer_inf,axe,overlap_entre_cordons_contour+rayon_cordon,float(width)/1000)
            except :
                under_layer = layer_inf
                
            cordon_contour,liste_coordonnees_cordons_contour = Create_contour_cordon(layer_inf,N_facette_cordon,axe,rayon_cordon,type_cordon,avec_extremite)

            mesh_entier += cordon_contour

            liste_coordonnees_cordons_tranche[0] = liste_coordonnees_cordons_contour

        

            #nouveau_mesh = reconstitution_couche(layer_inf+under_layer,axe,width)

            if not holographique :
                
                cordon_interieur,liste_coordonnees_cordons_interieur = Create_cordon(under_layer,axe,width,hauteur_de_coupe,coupe_au_centre,trait_cordon,N_facette_cordon,rayon_cordon,overlap_entre_cordons,type_cordon,avec_extremite,type_maille,parametre_de_maille)

            if holographique :

                trait_cordon_orthogonal = operation_vecteur(unitaire,trait_cordon,"vec")

                cordon_int_1,coord_cordon_1 = Create_cordon(under_layer,axe,width,hauteur_de_coupe,coupe_au_centre,trait_cordon,3,rayon_cordon,overlap_entre_cordons,"cylindrique",False,["lineaire","decroisee"],parametre_de_maille)
                cordon_int_2,coord_cordon_2 = Create_cordon(under_layer,axe,width,hauteur_de_coupe,coupe_au_centre,trait_cordon_orthogonal,3,rayon_cordon,overlap_entre_cordons,"cylindrique",False,["lineaire","decroisee"],parametre_de_maille)
                liste_coordonnees_cordons_interieur = maille_holographique(coord_cordon_1,coord_cordon_2,axe,parametre,trait_cordon,trait_cordon_orthogonal,rayon_cordon)
                cordon_interieur = []

                for i in range(len(liste_coordonnees_cordons_interieur)) :

                    vecteur_directeur = operation_vecteur(liste_coordonnees_cordons_interieur[i][1],liste_coordonnees_cordons_interieur[i][0],"-")
                    norme = norme_vecteur(vecteur_directeur)
                    vect = operation_vecteur(vecteur_directeur,norme,"/")
                    cordon,coord_perdu = generer_cylindre_mesh(axe,rayon_cordon,norme,liste_coordonnees_cordons_interieur[i][0],vect,N_facette_cordon,type_cordon,avec_extremite,type_maille[0],parametre_de_maille,"+",point_verifier[1])
                    cordon_interieur += cordon
                
            liste_coordonnees_cordons_tranche[1] = liste_coordonnees_cordons_interieur

            mesh_entier += cordon_interieur


    #####################################
    # traitement de la couche sup�rieure#
    #####################################

    #if point_verifier[0] >= trait[1] :

        #tranche_de_mesh_sup = Create_diamant(coupe_mesh,trait[1],axe,"+",False)

    #layer_inf = CreateContour(tranche_de_mesh_inf)

        

    #layer_sup = CreateContour(tranche_de_mesh_sup)

        

    #####################################
    # lissage couche                    #
    #####################################

    #nouveau_mesh = reconstitution_couche(layer_inf,axe,width)

    return mesh_entier,liste_coordonnees_cordons_tranche

def slice_objet(mesh,width,coupe_au_centre,axe,rotation_angle,N_facette_cordon,rayon_cordon,overlap_entre_cordons,overlap_entre_cordons_contour,type_cordon,avec_extremite,type_maille,parametre_de_maille,holographique,parametre) :
    '''
    # cette fonction permet de retourner  un mesh correspondant � l'objet "mesh" tranch� et rempli de cordons, selon un axe de d�coupe et une �paisseur de tranche

    ##########################

    ##########
    # entr�e #
    ##########

    # mesh (type list) : liste sous le format d�fini par la fonction load_mesh

    # width (type int ou float) : �paisseur des tranches

    # coupe_au_centre (type bool) : j'ai mis cette option mais je sais pas si elle a un int�r�t important, mettre False comme entr�e

    # axe (type str) : axe de d�coupe

    # rotation_angle (type int ou float) : angle correspondant au changement d'orientation des cordons � chaque nouvelle couche

    # N_facette_cordon (type int) : nombre de sommets du polygone qui d�finira la base des cylindres repr�sentant les cordons

    # rayon_cordon (type int ou float) : rayon des cylindres repr�sentant les cordons

    # overlap_entre_cordons (type int ou float) : espace entre chaque cordon

    # overlap_entre_cordons_contour (type int ou float) : espace entre le cordon d�finissant le contour de la tranche et entre les cordons � l'int�rieur du contour de la tranche

    # type_cordon (type str) : "cylindrique" pour avoir des cordons cylindriques ou "clavette", ou "ellipse" pour avoir des cordons l�g�rement aplatis

    # avec_extremite (type bool) : si on veut les extr�mit�s des cordons

    # type_maille (type list) : le premier item correspond au type de la maille, "lineaire", "losange", "hexagonale","aleatoire". Le second correspond au caract�re crois� ou non , "croisee" ou "decroisee"

    # parametre_de_maille (type int ou float) : param�tre de la maille

    # holographique (type bool) : si on veut une surface holographique

    # parametre (type int ou float) : param�tre de la maille holographique

    ##########
    # sortie #
    ##########

    # tranchage (type list) : liste repr�sentant les cordons n�cessaires � la r�alisation de l'objet sous le format d�fini par la fonction load_mesh

    # liste_coordonnees_cordons (type list) : liste des coordonn�es des diff�rents cordons de la tranche avec pour chaque cordon une liste des coordonn�es du point de d�part et du point d'arriv�e

    ##########################'''

    liste_coordonnees_cordons = []

    xmax,xmin,ymax,ymin,zmax,zmin = Extremum(mesh)

    tranchage = []
    angle = 0

    if axe == "x" :

        commencement = xmin

        taille = xmax-xmin

    if axe == "y" :

        commencement = ymin

        taille = ymax-ymin

    if axe == "z" :

        commencement = zmin

        taille = zmax-zmin

    N_decoupe = ceil(float(taille)/width)

    for i in range(int(N_decoupe)) :

        mesh_tranchage,liste_coordonnees_cordons_tranche = slice_couche(mesh,width,commencement+i*width,coupe_au_centre,axe,angle,N_facette_cordon,rayon_cordon,overlap_entre_cordons,overlap_entre_cordons_contour,type_cordon,avec_extremite,type_maille,parametre_de_maille,holographique,parametre)
        tranchage += mesh_tranchage
        liste_coordonnees_cordons.append(liste_coordonnees_cordons_tranche)
        angle += rotation_angle

    return tranchage,liste_coordonnees_cordons

###################### test ###############################                

#layer=[[[], [[-1, 1, 0], [0, 1, 0], [0, 0, 0]]], [[], [[0, 1, 0], [1, 1, 0], [0, 0, 0]]], [[], [[1, 1, 0], [1, 0, 0], [0, 0, 0]]], [[], [[1, 0, 0], [1, -1, 0], [0, 0, 0]]], [[], [[1, -1, 0], [0, -1, 0], [0, 0, 0]]], [[], [[0, -1, 0], [-1, -1, 0], [0, 0, 0]]], [[], [[-1, -1, 0], [-1, 0, 0], [0, 0, 0]]], [[], [[-1, 0, 0], [-1, 1, 0], [0, 0, 0]]]]
#print CreateContour(layer)

#from load import load_mesh
#my_mesh=load_mesh("creeper2.stl","binaire")
#print Extremum(my_mesh)
#coupe_mesh,liste_coordonnees_cordons=slice_objet(my_mesh,0.3,False,"z",30,12,0.3,0,0,"cylindrique",False,["lineaire","decroisee"],1,False,0.5)
#mesh_2 = regeneration_cordon(liste_coordonnees_cordons,1,"z")
#with open("coordonnees_carr�.csv","w") as fich:

    #fich.write("point d�but"+";"+"point fin"+"\n")
    #for i in range(len(liste_coordonnees_cordons[0])) :
        #fich.write(str(liste_coordonnees_cordons[0][i][0][0])+","+str(liste_coordonnees_cordons[0][i][0][1])+","+str(liste_coordonnees_cordons[0][i][0][2])+";"+str(liste_coordonnees_cordons[0][i][1][0])+","+str(liste_coordonnees_cordons[0][i][1][1])+","+str(liste_coordonnees_cordons[0][i][1][2])+"\n")

#from fonction_centre_gravite import *
#print Calcul_centre_gravite(liste_coordonnees_cordons)
#from fonction_generation_fichier_stl import *
#Create_fichier_stl("essai_cube",mesh_2)
#Create_fichier_stl("test_creeper",coupe_mesh)
#Create_fichier_csv("Classeur_cordons_cylindre",liste_coordonnees_cordons)
#Create_fichier_catia("Catia_cube_2",liste_coordonnees_cordons,1,"cylindrique",5,"z")

##########################################################


#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################


# fonctions qui ont pu me servir, parfois pour visualiser un r�sultat, mais qui dans la r�alisation finale ne servent plus car leur fonctionnement n'�tait pas assez optimis� ou trop compliqu�
# Ces fonctions peuvent encore servir

def reconstitution_couche(layer,axe,width) :
    '''
    # cette fonction cr�e une tranche d'�paisseur "width" � partir d'un contour "layer" et dont la surface est orthogonale � la direction "axe"

    ##########################

    ##########
    # entr�e #
    ##########

    # layer (type list): : liste de couples de coordonn�es de points cons�cutifs du contour, ainsi que de la normale dirig�e vers l'ext�rieur sous le format [([x1,y1,z1],[x2,y2,z2],[nx,ny,nz]),...]

    # axe (type str) : direction orthogonale au plan d�fini par le contour "layer"

    # width (type int ou float) : �paisseur de la tranche

    ##########
    # sortie #
    ##########

    #mesh (type list) : liste repr�sentant la tranche sous le format d�fini par la fonction load_mesh

    ##########################'''

    if axe == "x" :

        coordonnees = 0
        
    if axe == "y" :
        
        coordonnees = 1
        
    if axe == "z" :
        
        coordonnees = 2

    contour = layer

    mesh = []

    rajout_hauteur = [0,0,0]
    rajout_hauteur[coordonnees] += width

    for i in range(len(contour)) :


            facette_1 = [contour[i][0],contour[i][1],operation_vecteur(contour[i][0],rajout_hauteur,"+")]
            facette_2 = [facette_1[2],contour[i][1],operation_vecteur(contour[i][1],rajout_hauteur,"+")]

            normale_1 = contour[i][2]
            normale_1[coordonnees] = 0
            normale_2 = contour[i][2]
            normale_2[coordonnees] = 0

            mesh.append([normale_1,facette_1])
            mesh.append([normale_2,facette_2])

    return mesh

def separation_des_contours(layer,axe) :
    '''
    # cette fonction permet � partir d'un contour d�fini sur un niveau
    # de s�parer les diff�rents contours dans le cas ou l'objet 3D
    # pr�senterait un creux � ce niveau'''

    surface = []

    
    if axe == "x" :

        coordonnees = [1,2,0]
        
    if axe == "y" :
        
        coordonnees = [0,2,1]
        
    if axe == "z" :
        
        coordonnees = [0,1,2]

    liste_des_contours = [[layer[0]]]

    for i in range(1,len(layer)):

        for j in range(len(liste_des_contours)):

            if layer[i][0] == liste_des_contours[j][-1][1] :

                liste_des_contours[j].append(layer[i])

    return liste_des_contours

def Create_diamant(mesh,niveau,axe,signe,tout,precision) :
    '''
    # cette fonction cr�e un mesh "diamant�" � partir d'un mesh repr�sentant une tranche, le mesh "diament�" est un mesh dont la base est un polygone et dont tous les sommets de la base sont reli�s � un point unique

    ##########################

    ##########
    # entr�e #
    ##########

    # mesh (type list): liste sous le format d�fini par la fonction load_mesh

    # niveau (type int ou float) : valeur correspondant au niveau

    # axe (type str) : direction orthogonale au plan d�fini par la tranche

    # signe (type str) : si on veut le mesh diamant� inf�rieur ou sup�rieur au niveau

    # tout (type bool) : True si on veut le mesh diamant� et la tranche en retour ou False si on veut seulement le mesh diamant�

    # precision (type int ou float) : pr�cision souhait�e

    ##########
    # sortie #
    ##########

    # diamant_mesh (type list) : liste repr�sentant le nouveau mesh sous le format d�fini par la fonction load_mesh

    ##########################'''
    
    xmax,xmin,ymax,ymin,zmax,zmin=Extremum(mesh)

    if axe == "x" :

        coordonnees = [1,2,0]
        
        if signe == "-" :
            x = niveau-10
        else :
            x = niveau+10
            
        point = [x,(ymax+ymin)/2.0,(zmax+zmin)/2.0]

    if axe == "y" :
        coordonnees = [0,2,1]
        
        if signe == "-" :
            y = niveau-10
        else :
            y = niveau+10
            
        point = [(xmax+xmin)/2.0,y,(zmax+zmin)/2.0]

    if axe == "z" :
        coordonnees = [0,1,2]

        if signe == "-" :
            z = niveau-10
        else :
            z = niveau+10
            
        point = [(xmax+xmin)/2.0,(ymax+ymin)/2.0,z]
        
    diamant_mesh = []

    for i in range(len(mesh)) :
        
        num_point_niveau,point_niveau = compte_point_niveau(mesh[i][1],coordonnees[2],niveau,precision)
        
        if num_point_niveau == 2 :

            ######################## dans le cas d'un mauvais arrondi mais acceptable pour la pr�cision donn�e ###########################

            if point_niveau[0][coordonnees[2]] != niveau :
    
                point_niveau[0][coordonnees[2]] = niveau

            if point_niveau[1][coordonnees[2]] != niveau :

                point_niveau[1][coordonnees[2]] = niveau

            ######################################################################################

            

            nouvelle_facette = [point_niveau[0],point_niveau[1],point]
            
            vecteur_directeur_1 = operation_vecteur(nouvelle_facette[0],nouvelle_facette[1],"-")
            vecteur_directeur_2 = operation_vecteur(nouvelle_facette[1],nouvelle_facette[2],"-")
            

            vecteur_normal = operation_vecteur(vecteur_directeur_1,vecteur_directeur_2,"vec")

            if signe == "-" :

                if vecteur_normal[coordonnees[2]] > 0 :

                    # la normale n'est pas dirig�e vers l'ext�rieur

                    vecteur_normal = operation_vecteur(vecteur_normal,-1,"*")

            if signe == "+" :

                if vecteur_normal[coordonnees[2]] < 0 :

                    # la normale n'est pas dirig�e vers l'ext�rieur

                    vecteur_normal = operation_vecteur(vecteur_normal,-1,"*")
                
            diamant_mesh.append([vecteur_normal,nouvelle_facette])

        if tout :

            diamant_mesh.append(mesh[i])

    return diamant_mesh

def tri_facette(mesh):

    copie_mesh = copy.deepcopy(mesh)
    mesh_tri = [mesh[0]]

    while len(mesh_tri) < len(copie_mesh) :

        for i in range(len(copie_mesh)) :

            facette_a_supprimer = []

            if mesh_tri.count(copie_mesh[i]) == 0 and point_en_commun(copie_mesh[i][1],mesh_tri[len(mesh_tri)-1][1]) == 2 :

                mesh_tri.append(copie_mesh[i])

    return mesh_tri

def rectangle_de_coupe(mesh,width,hauteur_de_coupe,coupe_au_centre) :
    '''
    # cette fonction permet de g�n�rer un rectangle
    # de la m�me hauteur que la taille des tranches
    # et qui englobe tout l'objet mesh au niveau de la
    # tranche souhait�e avec un choix de hauteur
    # de coupe soit au centre du rectangle soit �
    # l'ordonn�e zmin du rectangle

    ##########################

    ##########
    # entr�e #
    ##########

    # mesh (type list) : liste sous le format d�fini par la fonction load_mesh

    # width (type int ou float) : correspond � l'�paisseur du pav�

    # hauteur_de_coupe (type int ou float) : correspond au niveau o� commence le pav�

    # coupe_au_centre (type bool) : si la coupe est au niveau de la hauteur de coupe + width/2

    ##########
    # sortie #
    ##########

    # coordonnees_pavet (type list) : liste des coordonn�es des sommets du pav� sous le format [[x1,y1,z1],[x2,y2,z2],...,[x8,y8,z8]]

    ##########################'''

    xMax,xMin,yMax,yMin,zMax,zMin = Extremum(mesh)
    
    if coupe_au_centre :
        coordonnees_pavet = [[xMin,yMin,hauteur_de_coupe-width/2.0],[xMin,yMax,hauteur_de_coupe-width/2.0],[xMax,yMax,hauteur_de_coupe-width/2.0],[xMan,yMin,hauteur_de_coupe-width/2.0],[xMin,yMin,hauteur_de_coupe+width/2.0],[xMin,yMax,hauteur_de_coupe+width/2.0],[xMax,yMax,hauteur_de_coupe+width/2.0],[xMan,yMin,hauteur_de_coupe+width/2.0]]
        return coordonnees_pavet
    
    coordonnees_pavet = [[xMin,yMin,hauteur_de_coupe],[xMin,yMax,hauteur_de_coupe],[xMax,yMax,hauteur_de_coupe],[xMan,yMin,hauteur_de_coupe],[xMin,yMin,hauteur_de_coupe+width],[xMin,yMax,hauteur_de_coupe+width],[xMax,yMax,hauteur_de_coupe+width],[xMan,yMin,hauteur_de_coupe+width]]
    return coordonnees_pavet

def Create_contour_diamant(mesh,axe,niveau_contour,precision) :

    if axe == "x" :

        coordonnees = 0

    if axe == "y" :

        coordonnees = 1

    if axe == "z" :

        coordonnees = 2

    contour_diamant = []

    for i in range(len(mesh)) :

        point_a_prendre = []

        if abs(mesh[i][1][0][coordonnees]-niveau_contour) <= precision :

            point_a_prendre.append(mesh[i][1][0])

        if abs(mesh[i][1][1][coordonnees]-niveau_contour) <= precision:

            point_a_prendre.append(mesh[i][1][1])

        if abs(mesh[i][1][2][coordonnees]-niveau_contour) <= precision :

            point_a_prendre.append(mesh[i][1][2])

        ##########################################################################################################################################################################################
        # pour faire une forme de tri qui permet que chaque point du contour apparaisse une seule fois avec l'indice 0 du couple de point et une fois avec l'indice 1 de l'autre couple de points#
        ##########################################################################################################################################################################################

        
        
        #check = False
        

        #for j in range(len(contour_diamant)) :

            #if comparaison_vecteur(contour_diamant[j][0],point_a_prendre[0],precision) :

                #check = True

            #if comparaison_vecteur(contour_diamant[j][1],point_a_prendre[1],precision) :

                #check = True

        #if not check :        

        contour_diamant.append((point_a_prendre[0],point_a_prendre[1],mesh[i][0]))

        #if check :

            #contour_diamant.append((point_a_prendre[1],point_a_prendre[0],mesh[i][0]))

        # double tri si on veux mais c'est long #############################################################################

        #check = False

        #for k in range(len(contour_diamant)) :
        
            #for j in range(len(contour_diamant_2)) :

                #if comparaison_vecteur(contour_diamant_2[j][0],contour_diamant[k][0],precision) :

                    #check = True

                #if comparaison_vecteur(contour_diamant_2[j][1],contour_diamant[k][1],precision) :

                    #check = True

            #if not check :        

                #contour_diamant_2.append((contour_diamant[k][0],contour_diamant[k][1],mesh[i][0]))

            #if check :

                #contour_diamant_2.append((contour_diamant[k][1],contour_diamant[k][0],mesh[i][0]))

        ######################################################################################################################################################################################

    return contour_diamant

#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################

# une des fonctions de Thibaud que j'ai adapt�e, pour comprendre quelques notions de gestion de la g�om�trie par des listes, mais qui par la suite ne m'a pas servi pour mon programme final

def CreateContour(layer):
    '''
    Create the limits edges of the layer.
    '''
    #layer.enable_connectivity()
    Edges = []
    
    for faceindex in range(len(face(layer))):
        faces = face(layer)[faceindex]
        NearFaces = get_face_adjacent_faces(layer,faceindex)
        if len(NearFaces) != 3:         #if there are more than 2 adjacent faces there is no limit edges in the triangle
            #mesh.append([normale_face([vertices(layer)[faces[0]],vertices(layer)[faces[1]],vertices(layer)[faces[2]]]),[vertices(layer)[faces[0]],vertices(layer)[faces[1]],vertices(layer)[faces[2]]]])
            for indexs in [(0,1),(1,2),(0,2)]:          
                A = vertices(layer)[faces[indexs[0]]]
                B = vertices(layer)[faces[indexs[1]]]
                check = True
                face_A=[]
                for facetest in NearFaces:
                    face_A.append(sommet_de_face(layer,facetest))
                    if if_point_in_facette(A,sommet_de_face(layer,facetest),0.0001) and if_point_in_facette(B,sommet_de_face(layer,facetest),0.0001):
                        check = False
                if check == True:
                    Edges.append((A,B))
    return Edges

#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################

# essais de fonctions non aboutis

def Create_cordon_essai(layer,angle_rad,extreme_cordon,axe,width,hauteur_de_coupe,coupe_au_centre,trait_cordon,rayon_cordon) :

    if coupe_au_centre :

        hauteur_cordon = hauteur_de_coupe

    else :

        hauteur_cordon = hauteur_de_coupe+width/2

    vecteur_directeur = [0,0,0]
    
    if axe == "x" :
        coordonnees = [1,2,0]
        point_max_max = [hauteur_de_coupe,extreme_mesh[0],extreme_mesh[2]]
        point_min_max = [hauteur_de_coupe,extreme_mesh[1],extreme_mesh[2]]
        point_max_min = [hauteur_de_coupe,extreme_mesh[0],extreme_mesh[3]]
        point_min_min = [hauteur_de_coupe,extreme_mesh[1],extreme_mesh[3]]

        if trait_cordon[1] < 0 :

            signe_1 = "-"

        if trait_cordon[1] >= 0 :

            signe_1 = "+"

        if trait_cordon[2] < 0 :

            signe_2 = "-"

        if trait_cordon[2] >= 0 :

            signe_2 = "+"        

    if axe == "y" :
        coordonnees = [0,2,1]
        point_max_max = [extreme_mesh[0],hauteur_de_coupe,extreme_mesh[2]]
        point_min_max = [extreme_mesh[1],hauteur_de_coupe,extreme_mesh[2]]
        point_max_min = [extreme_mesh[0],hauteur_de_coupe,extreme_mesh[3]]
        point_min_min = [extreme_mesh[1],hauteur_de_coupe,extreme_mesh[3]]

        if trait_cordon[0] < 0 :

            signe_1 = "-"

        if trait_cordon[0] >= 0 :

            signe_1 = "+"

        if trait_cordon[2] < 0 :

            signe_2 = "-"

        if trait_cordon[2] >= 0 :

            signe_2 = "+"

    if axe == "z" :
        coordonnees = [0,1,2]
        point_max_max = [extreme_mesh[0],extreme_mesh[2],hauteur_de_coupe]
        point_max_min = [extreme_mesh[0],extreme_mesh[3],hauteur_de_coupe]
        point_min_max = [extreme_mesh[1],extreme_mesh[2],hauteur_de_coupe]
        point_min_min = [extreme_mesh[1],extreme_mesh[3],hauteur_de_coupe]

        if trait_cordon[0] < 0 :

            signe_1 = "-"

        if trait_cordon[0] >= 0 :

            signe_1 = "+"

        if trait_cordon[1] < 0 :

            signe_2 = "-"

        if trait_cordon[1] >= 0 :

            signe_2 = "+"

    translation_axe_1 = extreme_mesh[0]-extreme_mesh[1]
    translation_axe_2 = extreme_mesh[2]-extreme_mesh[3]

    N_hauteur_1 = int(ceil(float(translation_axe_1)/(2*rayon_cordon)))
    N_hauteur_2 = int(ceil(float(translation_axe_2)/(2*rayon_cordon)))

    ########################################################################  coin doublement inf�rieur ##############################################

    if signe_1 == "+" and signe_2 == "+" :

        point_depart = point_min_min

        for i in range(len(N_hauteur_1)) :

            liste_point = []

            for j in range(len(layer)) :

                check,point_intersection = if_croisement(trait_cordon,point_depart,layer[j][0],layer[j][1],axe)

                if check :

                    liste_point.append([point_intersection,distance_points(point_intersection,point_depart)])

            liste = tri(liste_point,"+",1)

            for j in range(len(liste)) :

                if j%2 == 0 :

                    if j<len(liste) :

                        hauteur = distance(liste[j][0],liste[j+1][0])
                        centre_base = liste[j][0]
                        centre_base[coordonnees[2]] = hauteur_de_coupe
                        generer_cylindre_mesh(axe,rayon,hauteur,centre_base,trait_cordon)
                
                
                point_depart[coordonnees[0]] += N_hauteur_1*2*rayon_cordon

        for i in range(len(N_hauteur_2)) :

            liste_point = []

            for j in range(len(layer)) :

                check,point_intersection = if_croisement(trait_cordon,point_depart,layer[j][0],layer[j][1],axe)

                if check :

                    liste_point.append([point_intersection,distance_points(point_intersection,point_depart)])

            liste = tri(liste_point,"+",1)

            for j in range(len(liste)) :

                if j%2 == 0 :

                    if j<len(liste) :

                        hauteur = distance(liste[j][0],liste[j+1][0])
                        centre_base = liste[j][0]
                        centre_base[coordonnees[2]] = hauteur_de_coupe
                        generer_cylindre_mesh(axe,rayon,hauteur,centre_base,trait_cordon)
                
                
                point_depart[coordonnees[1]] += N_hauteur_2*2*rayon_cordon

    ########################################################################  coin inf�rieur sup�rieur ##############################################

def lissage_couche(tranche_mesh,axe,trait):

    if axe == "x" :
        coordonnees = [1,2,0]

    if axe == "y" :
        coordonnees = [0,2,1]

    if axe == "z" :
        coordonnees = [0,1,2]

    sommets = vertices(tranche_mesh)

    coupe_lisse = []
    mesh_lisse = []
    coupe_finis = []


    for i in range(len(tranche_mesh)) :

        point_moyenne_facette_1 = [0,0,0]
        point_moyenne_facette_2 = [0,0,0]
        point_x_moyenne_facette = (tranche_mesh[i][1][0][coordonnees[0]]+tranche_mesh[i][1][1][coordonnees[0]]+tranche_mesh[i][1][2][coordonnees[0]])/3.0
        point_y_moyenne_facette = (tranche_mesh[i][1][1][coordonnees[0]]+tranche_mesh[i][1][1][coordonnees[1]]+tranche_mesh[i][1][2][coordonnees[1]])/3.0

        point_moyenne_facette_1[coordonnees[0]] = point_x_moyenne_facette
        point_moyenne_facette_1[coordonnees[1]] = point_y_moyenne_facette
        point_moyenne_facette_1[coordonnees[2]] = trait[0]
        point_moyenne_facette_2[coordonnees[0]] = point_x_moyenne_facette
        point_moyenne_facette_2[coordonnees[1]] = point_y_moyenne_facette
        point_moyenne_facette_2[coordonnees[2]] = trait[1]

        if coupe_lisse.count([point_moyenne_facette_1,point_moyenne_facette_2]) == 0 and coupe_lisse.count([point_moyenne_facette_2,point_moyenne_facette_1]) == 0 :
            coupe_lisse.append([point_moyenne_facette_1,point_moyenne_facette_2,tranche_mesh[i][0]])

    

    for i in range(len(coupe_lisse)) :

        if i == 0 :

            point_avant = -1
            point_apres = i+1

        if i == len(coupe_lisse)-1 :

            point_avant = i-1
            point_apres = 0

        if i != 0 and i != len(coupe_lisse)-1 :

            point_avant = i-1
            point_apres = i+1


        mesh_lisse.append([coupe_lisse[point_avant][0],coupe_lisse[i][0],coupe_lisse[i][1],[coupe_lisse[point_avant][2],coupe_lisse[i][2]]])
        mesh_lisse.append([coupe_lisse[point_apres][1],coupe_lisse[i][0],coupe_lisse[i][1],[coupe_lisse[point_apres][2],coupe_lisse[i][2]]])

    for i in range(len(mesh_lisse)) :

        vecteur_directeur_1 = operation_vecteur(mesh_lisse[i][0],mesh_lisse[i][1],"-")
        vecteur_directeur_2 = operation_vecteur(mesh_lisse[i][1],mesh_lisse[i][2],"-")

        vecteur_normal = operation_vecteur(vecteur_directeur_1,vecteur_directeur_2,"vec")

        if mesh_lisse[i][3][0][coordonnees[0]]*mesh_lisse[i][3][1][coordonnees[0]] >= 0 :

            if vecteur_normal[coordonnees[0]]*mesh_lisse[i][3][0][coordonnees[0]] >= 0 and vecteur_normal[coordonnees[0]]*mesh_lisse[i][3][1][coordonnees[0]] >= 0 :

                vecteur_normal = vecteur_normal

            else :

                vecteur_normal = operation_vecteur(vecteur_normal,-1,"*")

        if mesh_lisse[i][3][0][coordonnees[1]]*mesh_lisse[i][3][1][coordonnees[1]] >= 0 :

            if vecteur_normal[coordonnees[1]]*mesh_lisse[i][3][0][coordonnees[1]] >= 0 and vecteur_normal[coordonnees[1]]*mesh_lisse[i][3][1][coordonnees[1]] >= 0 :

                vecteur_normal = vecteur_normal

            else :

                vecteur_normal = operation_vecteur(vecteur_normal,-1,"*")

        coupe_finis.append([vecteur_normal,[mesh_lisse[i][0],mesh_lisse[i][1],mesh_lisse[i][2]]])

    return coupe_finis

def lissage_couche_2(tranche_mesh,axe,trait) :
    
    if axe == "x" :
        coordonnees = [1,2,0]

    if axe == "y" :
        coordonnees = [0,1,2]

    if axe == "z" :
        coordonnees = [0,1,2]

    for i in range(len(tranche_mesh)) :

        if tranche_mesh[i][0][coordonnees[2]] != 0 :

            
            point_x_moyenne_facette = (tranche_mesh[i][1][0][coordonnees]+tranche_mesh[i][1][1][coordonnees]+tranche_mesh[i][1][2][coordonnees])/3.0

            for point in tranche_mesh[i][1] :

                tranche_mesh[i][1][0] = [point]

def remplir_tranchage(tranche_mesh,axe,trait_de_coupe) :

    if axe == "x" :
        coordonnees = 0

    if axe == "y" :
        coordonnees = 1

    if axe == "z" :
        coordonnees = 2

    sommets = vertices(tranche_mesh)

    points_surface_1 = []
    points_surface_2 = []

    for i in range(len(sommets)) :

        if sommets[i][indice] == trait_de_coupe[0] and points_surface_1.count(sommets[i]) == 0 :
            points_surface_1.append(sommets[i])

        if sommets[i][indice] != trait_de_coupe[1] and points_surface_2.count(sommets[i]) == 0 :
            points_surface_2.append(sommets[i])

def holographique_2_alea(coord_cordon_1,coord_cordon_2,axe,parametre,trait_cordon,orthogonal_trait_cordon,rayon_cordon) :
    try :
        from random import randint
    except :
        return None

    if axe == "x" :

        coordonnees = [1,2,0]
        unitaire = [1,0,0]
        axes = ["y","z"]
        direction_orthogonale = operation_vecteur(unitaire,trait_cordon,"vec")
        matrice_origine = mise_en_base(trait_cordon,unitaire,orthogonal_trait_cordon)
        matrice = inverse_matrice(matrice_origine)

    if axe == "y" :

        coordonnees = [2,0,1]
        unitaire = [0,1,0]
        axes = ["z","x"]
        direction_orthogonale = operation_vecteur(unitaire,trait_cordon,"vec")
        matrice_origine = mise_en_base(trait_cordon,unitaire,orthogonal_trait_cordon)
        matrice = inverse_matrice(matrice_origine)

    if axe == "z" :

        coordonnees = [0,1,2]
        unitaire = [0,0,1]
        axes = ["x","y"]
        direction_orthogonale = operation_vecteur(unitaire,trait_cordon,"vec")
        matrice_origine = mise_en_base(trait_cordon,unitaire,orthogonal_trait_cordon)
        matrice = inverse_matrice(matrice_origine)
    
    coord_cordon_nouvelle_base = []
    coord_cordon_nouvelle_base_2 = []

    for i in range(len(coord_cordon_1)) :

        coord_1 = prod_matriciel(matrice,coord_cordon_1[i][0])
        coord_2 = prod_matriciel(matrice,coord_cordon_1[i][1])
        
        
        if coord_1[0] <= coord_2[0] :
            coord_cordon_nouvelle_base.append([coord_1,coord_2])

        else :
            coord_cordon_nouvelle_base.append([coord_2,coord_1])

    for i in range(len(coord_cordon_2)) :

        coord_1_2 = prod_matriciel(matrice,coord_cordon_2[i][0])
        coord_2_2 = prod_matriciel(matrice,coord_cordon_2[i][1])

        if coord_1_2[2] <= coord_2_2[2] :
            coord_cordon_nouvelle_base_2.append([coord_1_2,coord_2_2])

        else :
            coord_cordon_nouvelle_base_2.append([coord_2_2,coord_1_2])

    extremum_mesh = extremum_layer(coord_cordon_nouvelle_base,[0,1,2])
    
    liste_point_relie = []
    liste_point_relie_2 = []
    liste_indice = []
    liste_indice_2 = []


    for i in range(len(coord_cordon_nouvelle_base)):

        indice_min = extremum_mesh[1]
        indice_max = extremum_mesh[0]
        point = [coord_cordon_nouvelle_base[i][0]]

        while indice_min < indice_max :

            vecteur_directeur = operation_vecteur(coord_cordon_nouvelle_base[i][1],coord_cordon_nouvelle_base[i][0],"-")
            
            if vecteur_directeur[0] == 0 :
                coefficient = 0

            if vecteur_directeur[0] != 0 :
                coefficient = float(indice_min-coord_cordon_nouvelle_base[i][0][0])/vecteur_directeur[0]

            if indice_min > coord_cordon_nouvelle_base[i][0][0] and indice_min < coord_cordon_nouvelle_base[i][1][0] and coefficient != 0 :

                if len(point) == 2 :

                    liste_point_relie.append(point)
                    point = [liste_point_relie[-1][1]]

                if len(point)< 2 :

                    chemin = operation_vecteur(vecteur_directeur,coefficient,"*")
                    point_2 = operation_vecteur(coord_cordon_nouvelle_base[i][0],chemin,"+")

                    if not comparaison_vecteur(point_2,point[0],0.01) :

                        point.append(operation_vecteur(coord_cordon_nouvelle_base[i][0],chemin,"+"))

            indice = float(parametre)/randint(1,2)
            liste_indice.append(indice)
            indice_min += indice

        if len(point) == 1 :

            point.append(coord_cordon_nouvelle_base[i][1])
            liste_point_relie.append(point)

        if len(point) == 0 :
            
            liste_point_relie.append([liste_point_relie[-1][1],coord_cordon_nouvelle_base[i][1]])

        if len(point) == 2 :
            
            point_2 = [point[1],coord_cordon_nouvelle_base[i][1]]
            liste_point_relie.append(point)
            liste_point_relie.append(point_2)

    for i in range(len(coord_cordon_nouvelle_base_2)):

        indice_min = extremum_mesh[5]
        indice_max = extremum_mesh[4]
        point = [coord_cordon_nouvelle_base_2[i][0]]

        while indice_min < indice_max :

            vecteur_directeur = operation_vecteur(coord_cordon_nouvelle_base_2[i][1],coord_cordon_nouvelle_base_2[i][0],"-")

            if vecteur_directeur[2] == 0 :
                coefficient = 0

            if vecteur_directeur[2] != 0 :
                coefficient = float(indice_min-coord_cordon_nouvelle_base_2[i][0][2])/vecteur_directeur[2]

            if indice_min > coord_cordon_nouvelle_base_2[i][0][2] and indice_min < coord_cordon_nouvelle_base_2[i][1][2] and coefficient != 0 :
                
                if len(point) == 2 :

                    liste_point_relie_2.append(point)
                    point = [liste_point_relie_2[-1][1]]

                if len(point)< 2 :

                    chemin = operation_vecteur(vecteur_directeur,coefficient,"*")
                    point_2 = operation_vecteur(coord_cordon_nouvelle_base_2[i][0],chemin,"+")

                    if not comparaison_vecteur(point_2,point[0],0.01) :

                        point.append(point_2)
                    
            indice = float(parametre)/randint(1,2)
            liste_indice_2.append(indice)
            indice_min += indice

        if len(point) == 1 :

            point.append(coord_cordon_nouvelle_base_2[i][1])
            liste_point_relie_2.append(point)

        if len(point) == 0 :
            
            liste_point_relie_2.append([liste_point_relie_2[-1][1],coord_cordon_nouvelle_base_2[i][1]])

        if len(point) == 2 :
            
            point_2 = [point[1],coord_cordon_nouvelle_base_2[i][1]]
            liste_point_relie_2.append(point)
            liste_point_relie_2.append(point_2)

    indice_min_1 = extremum_mesh[1]
    indice_max_1 = extremum_mesh[0]
    indice_min_2 = extremum_mesh[5]
    indice_max_2 = extremum_mesh[4]

    j = 0

    coord_cordon = []

    indice = liste_indice[0]

    for g in range(len(liste_indice)) :

        indice = liste_indice[g]        
        indice_min_22 = indice_min_2
        
        for k in range(len(liste_indice_2)) :

            indice_2 = liste_indice_2[k]

            if j%2 == 0 :

                for i in range(len(liste_point_relie)) :

                    if liste_point_relie[i][0][0] >= indice_min_1-float(rayon_cordon)/3 and liste_point_relie[i][0][0] < indice_min_1+indice-float(rayon_cordon)/3 and liste_point_relie[i][0][2] >= indice_min_22-float(rayon_cordon)/3 and liste_point_relie[i][0][2] < indice_min_22+indice_2-float(rayon_cordon)/3 :

                        coord_cordon.append(liste_point_relie[i])

            if j%2 != 0 :

                for i in range(len(liste_point_relie_2)) :

                    if liste_point_relie_2[i][0][0] >= indice_min_1-float(rayon_cordon)/3 and liste_point_relie_2[i][0][0] < indice_min_1+indice-float(rayon_cordon)/3 and  liste_point_relie_2[i][0][2] >= indice_min_22-float(rayon_cordon)/3 and liste_point_relie_2[i][0][2] < indice_min_22+indice_2-float(rayon_cordon)/3 :

                        coord_cordon.append(liste_point_relie_2[i])

            
            indice_min_22 += indice_2
            j += 1

        indice_min_1 += indice
        j += 1

    coord_cordon_origine = []

    for i in range(len(coord_cordon)):

        coord_x = prod_matriciel(matrice_origine,coord_cordon[i][0])
        coord_y = prod_matriciel(matrice_origine,coord_cordon[i][1])
        vecteur_directeur = operation_vecteur(coord_x,coord_y,"-")
        

        if not comparaison_vecteur(vecteur_directeur,[0,0,0],0.0001) :

            coord_cordon_origine.append([coord_x,coord_y])                   

    return coord_cordon_origine

def holographique_essai(layer,axe,parametre,trait_cordon) :

    nouveau_mesh = reconstitution_couche(layer,axe,width)

    extremum_mesh = Extremum(mesh)

    if axe == "x" :

        coordonnees = [1,2,0]
        unitaire = [1,0,0]
        axes = ["y","z"]
        direction_orthogonale = operation_vecteur(unitaire,trait_cordon,"vec")
        matrice_origine = mise_en_base(trait_cordon,unitaire,direction_orthogonale)
        matrice = inverse_matrice(matrice_origine)

    if axe == "y" :

        coordonnees = [2,0,1]
        unitaire = [0,1,0]
        axes = ["z","x"]
        direction_orthogonale = operation_vecteur(unitaire,trait_cordon,"vec")
        matrice_origine = mise_en_base(trait_cordon,unitaire,direction_orthogonale)
        matrice = inverse_matrice(matrice_origine)

    if axe == "z" :

        coordonnees = [0,1,2]
        unitaire = [0,0,1]
        axes = ["x","y"]
        direction_orthogonale = operation_vecteur(unitaire,trait_cordon,"vec")
        matrice_origine = mise_en_base(trait_cordon,unitaire,direction_orthogonale)
        matrice = inverse_matrice(matrice_origine)

    mesh_nouvelle_base = []

    for i in range(len(nouveau_mesh)) :

        normale = prod_matriciel(matrice,mesh[i][0])
        point_1 = prod_matriciel(matrice,mesh[i][1][0])
        point_2 = prod_matriciel(matrice,mesh[i][1][1])
        point_3 = prod_matriciel(matrice,mesh[i][1][2])

        mesh_nouvelle_base.append([normale,[point_1,point_2,point_3]])

    extremum_mesh = Extremum(mesh_nouvelle_base)

    distance = extremum_mesh[1]-extremum_mesh[2]
    N_decoupe = ceil(float(distance)/parametre)
    point_depart = extremum_mesh[2]

    nouveau_mesh_2 = []

    for i in range(N_decoupe) :

        coupe_mesh = recuperation_tranche(mesh_nouvelle_base,parametre,point_depart,False,"x")
        nouveau_mesh_2.append(coupe_mesh)    

    n_decoupe = ceil(float(distance_1)/parametre)
        
        

    #Create_cordon(layer,axe,width,hauteur_de_coupe,coupe_au_centre,trait_cordon,N_facette_cordon,rayon_cordon,overlap_entre_cordons,type_cordon,avec_extremite,type_maille,parametre_de_maille)


            

                

            

        
    

