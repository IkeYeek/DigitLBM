# coding:latin-1

from math import pi,cos,sin
try :
    from random import randint
except :
    ' rien faire '
from slicer.fonction_vecteur import *
from slicer.fonction_matrice import *

def polygone_regulier(centre,nombre_points,rayon,hauteur,matrice,avec_dome) :
    '''
    # cette fonction crée deux polygones réguliers à partir d'un point qui sera le centre du premier polygone, le centre du second est le centre du premier translaté 

    ##########################

    ##########
    # entrée #
    ##########

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # nombre_points (type int) : le nombre de sommets du polygone

    # rayon (type float ou int) : distance centre-sommet

    # hauteur (type float ou int) : distance entre le centre du premier polygone et le centre du second polygone

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    # avec_dome (type bool) : si on veut les extrémités du cordon
    
    ##########
    # sortie #
    ##########

    # coord_point (type list) : liste des coordonnées des différents sommets du premier polygone sous le format [[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]]

    # coord_point_haut (type list) : liste des coordonnées des différents sommets du second polygone sous le format [[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]]

    # mesh_dome (type list) : mesh représentant les extrémités (liste vide si pas d'extrémités)

    ##########################'''

    coord_point = []
    coord_point_haut = []
    coord_point_new_base = []
    coord_point_haut_new_base = []
    centre_nouvelle_base = prod_matriciel(matrice,centre)
    centre_nouvelle_base_haut = operation_vecteur(centre_nouvelle_base,[0,hauteur,0],"+")

    for i in range(nombre_points) :

        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
        y=centre_nouvelle_base[2]+rayon*sin(2*pi/nombre_points*i)

        point_bas = [x,centre_nouvelle_base[1],y]
        point_haut = [x,centre_nouvelle_base[1]+hauteur,y]

        coord_point_new_base.append(point_bas)
        coord_point_haut_new_base.append(point_haut)


        point_bas_ancienne_base = prod_matriciel(inverse_matrice(matrice),point_bas)
        point_haut_ancienne_base = prod_matriciel(inverse_matrice(matrice),point_haut)
        
        coord_point.append(point_bas_ancienne_base)
        coord_point_haut.append(point_haut_ancienne_base)

    coord_point_new_base.append(coord_point_new_base[0])
    coord_point_haut_new_base.append(coord_point_haut_new_base[0])

    if avec_dome :

        mesh_dome = dome(rayon,centre_nouvelle_base,"-",coord_point_new_base,inverse_matrice(matrice))
        mesh_dome += dome(rayon,centre_nouvelle_base_haut,"+",coord_point_haut_new_base,inverse_matrice(matrice))

    if not avec_dome :

        mesh_dome = []
        
    coord_point.append(coord_point[0]) # pour fermer le cylindre
    coord_point_haut.append(coord_point_haut[0])

    return coord_point,coord_point_haut,mesh_dome        

def generer_cylindre_mesh(axe,rayon,hauteur,centre_base,vecteur_directeur,N_facette_cordon,type_cordon,avec_dome,type_maille,parametre_de_maille,orientation_maille,coord_de_depart) :
    '''
    # cette fonction crée un mesh représentant un "cylindre" avec un polygone à N sommets comme une base
    # la normale de la base du cordon est orthogonale à la direction axe et colinéaire à vecteur_directeur

    ##########################

    ##########
    # entrée #
    ##########

    # axe (type str) : axe correspond à l'une des directions principales de la base canonique

    # rayon (type int ou float) : rayon du cordon

    # hauteur (type int ou float) : correspond à la longueur du cordon

    # centre_base (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # vecteur_directeur (type list) : liste des coordonnées de la normale de la base de centre "centre_base" , orienté vers l'intérieur du cordon, sous le format [x,y,z]

    # N_facette_cordon (type int) : le nombre de sommets du polygone de la base du cordon

    # type_cordon (type str) : "cylindrique" pour des cordons cylindriques, "clavette" pour des cordons plats, ou "ellipse" pour des cordons à sections elliptiques

    # avec_dome (type bool) : pour avoir les extrémités ou non

    # type_maille (type str) : correspond au type de maille, "lineaire", "losange", "hexagonale", "aleatoire"

    # parametre_de_maille (type int ou float) : espace entre deux alternances de mailles

    # orientation_maille (type str) : "+" si la maille est orientée à "gauche", "-" si la maille est orientée à "droite"

    # coord_de_depart (type int ou float) : dans le cas d'un maillage cela devient l'origine du maillage

    ##########
    # sortie #
    ##########

    # mesh (type list) : liste sous le format défini par la fonction load_mesh

    # liste_coord_centre (type list) : liste des coordonnées des centres successifs du cordon sous le format [[[x1,y1,z1],[x2,y2,z2]],[[x2,y2,z2],[x3,y3,z3]],...]

    ##########################'''

    avec_decalage = True

    if type_maille == "lineaire" :

        avec_decalage = False    

    if axe == "x" :

        coordonnees = [1,2,0]
        unitaire = [1,0,0]

    if axe == "y" :

        coordonnees = [0,2,1]
        unitaire = [0,1,0]

    if axe == "z" :

        unitaire = [0,0,1]
        coordonnees = [0,1,2]

    unitaire_2 = operation_vecteur(unitaire,vecteur_directeur,"vec")

    matrice_base = inverse_matrice(mise_en_base(unitaire,vecteur_directeur,unitaire_2))

    mesh = []
    centre_base_haut_nouvelle_base = prod_matriciel(matrice_base,centre_base)
    centre_base_haut_nouvelle_base[1] = centre_base_haut_nouvelle_base[1]+hauteur
    centre_base_haut = prod_matriciel(inverse_matrice(matrice_base),centre_base_haut_nouvelle_base)

    ###################################### récupération des bases ##################################################

    type_base = ["cylindrique","ellipse","clavette"]
    fonction_base = [polygone_regulier,polygone_ellipse,polygone_clavette]
    mailles = ["losange","hexagonale","aleatoire"]
    fonction_maille = [[polygone_regulier_maille,polygone_regulier_hex,polygone_regulier_alea],[polygone_ellipse_maille,polygone_ellipse_hex,polygone_ellipse_alea],[polygone_clavette_maille,polygone_clavette_hex,polygone_clavette_alea]]
    indice_base = type_base.index(type_cordon)
    

    coord_point,coord_point_haut,mesh_dome = fonction_base[indice_base](centre_base,N_facette_cordon,rayon,hauteur,matrice_base,avec_dome)

    if avec_decalage :

        indice_maille = mailles.index(type_maille)

        coord_point_tot_incomplet,liste_coord_centre = fonction_maille[indice_base][indice_maille](centre_base,N_facette_cordon,rayon,hauteur,matrice_base,parametre_de_maille,orientation_maille,coord_de_depart)
                
        coord_point_tot = []
        coord_point_tot.append(coord_point)
        coord_point_tot += coord_point_tot_incomplet
        coord_point_tot.append(coord_point_haut)

    if not avec_decalage :

        liste_coord_centre = [[centre_base,centre_base_haut]]

    # formation de la base inférieure et de la base supérieure ainsi que des surfaces latérales
    
    for i in range(len(coord_point)-1) :

        if not avec_dome :
            facette_inf = [centre_base,coord_point[i],coord_point[i+1]]
            facette_sup = [coord_point_haut[i],centre_base_haut,coord_point_haut[i+1]]
            normale_inf = operation_vecteur(vecteur_directeur,-1,"*")
            normale_sup = vecteur_directeur
            mesh.append([normale_inf,facette_inf])
            mesh.append([normale_sup,facette_sup])

        if not avec_decalage :
        
            facette_laterale_1 = [coord_point[i+1],coord_point[i],coord_point_haut[i]]
            facette_laterale_2 = [coord_point[i+1],coord_point_haut[i],coord_point_haut[i+1]]
            
            normal_comparaison_1 = operation_vecteur(coord_point[i],centre_base,"-")
            normal_comparaison_2 = operation_vecteur(coord_point[i+1],centre_base,"-")
            normale_laterale = operation_vecteur(normal_comparaison_1,normal_comparaison_2,"+")
            
            mesh.append([normale_laterale,facette_laterale_1])
            mesh.append([normale_laterale,facette_laterale_2])

        if avec_decalage :

            for j in range(len(coord_point_tot)-1) :

                facette_laterale_1 = [coord_point_tot[j][i+1],coord_point_tot[j][i],coord_point_tot[j+1][i]]
                facette_laterale_2 = [coord_point_tot[j][i+1],coord_point_tot[j+1][i],coord_point_tot[j+1][i+1]]                
                
                normal_comparaison_1 = operation_vecteur(coord_point_tot[j][i],centre_base,"-")
                normal_comparaison_2 = operation_vecteur(coord_point_tot[j][i+1],centre_base,"-")
                normale_laterale = operation_vecteur(normal_comparaison_1,normal_comparaison_2,"+")
                
                mesh.append([normale_laterale,facette_laterale_1])
                mesh.append([normale_laterale,facette_laterale_2])

    mesh += mesh_dome

    return mesh,liste_coord_centre

def polygone_clavette(centre,nombre_points,rayon,hauteur,matrice,avec_dome) :
    '''
    # cette fonction crée deux clavettes à partir d'un point qui sera le centre du premier polygone, le centre du second est le centre du premier translaté 

    ##########################

    ##########
    # entrée #
    ##########

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # nombre_points (type int) : le nombre de sommets du polygone

    # rayon (type float ou int) : distance centre-sommet

    # hauteur (type float ou int) : distance entre le centre du premier polygone et le centre du second polygone

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    # avec_dome (type bool) : si on veut les extrémités

    ##########
    # sortie #
    ##########

    # coord_point (type list) : liste des coordonnées des différents sommets du premier polygone sous le format [[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]]

    # coord_point_haut (type list) : liste des coordonnées des différents sommets du second polygone sous le format [[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]]

    # mesh_dome (type list) : liste sous le format défini par la fonction load_mesh, mesh correspondant aux extrémités

    ##########################'''

    coord_point = []
    coord_point_haut = []
    coord_point_new_base = []
    coord_point_haut_new_base = []
    centre_nouvelle_base = prod_matriciel(matrice,centre)
    centre_nouvelle_base_haut = operation_vecteur(centre_nouvelle_base,[0,hauteur,0],"+")

    
    centre_nouvelle_base_1 = operation_vecteur(centre_nouvelle_base,[0,0,float(rayon)/2],"+")
    centre_nouvelle_base_2 = operation_vecteur(centre_nouvelle_base,[0,0,float(rayon)/2],"-")

    for i in range(2*nombre_points) :

        if i <= nombre_points-1 :
            
            x_1 = centre_nouvelle_base_1[0]+rayon*cos(pi/nombre_points*i)
            y_1 = centre_nouvelle_base_1[2]+rayon*sin(pi/nombre_points*i)

            point_bas_1 = [x_1,centre_nouvelle_base[1],y_1]
            point_haut_1 = [x_1,centre_nouvelle_base[1]+hauteur,y_1]

            coord_point_new_base.append(point_bas_1)
            coord_point_haut_new_base.append(point_haut_1)

            point_bas_ancienne_base_1 = prod_matriciel(inverse_matrice(matrice),point_bas_1)
            point_haut_ancienne_base_1 = prod_matriciel(inverse_matrice(matrice),point_haut_1)
            
            coord_point.append(point_bas_ancienne_base_1)
            coord_point_haut.append(point_haut_ancienne_base_1)

        else :
            
            x_2 = centre_nouvelle_base_2[0]+rayon*cos(pi/nombre_points*i)
            y_2 = centre_nouvelle_base_2[2]+rayon*sin(pi/nombre_points*i)

            point_bas_2 = [x_2,centre_nouvelle_base[1],y_2]
            point_haut_2 = [x_2,centre_nouvelle_base[1]+hauteur,y_2]

            coord_point_new_base.append(point_bas_2)
            coord_point_haut_new_base.append(point_haut_2)

            point_bas_ancienne_base_2 = prod_matriciel(inverse_matrice(matrice),point_bas_2)
            point_haut_ancienne_base_2 = prod_matriciel(inverse_matrice(matrice),point_haut_2)

            coord_point.append(point_bas_ancienne_base_2)
            coord_point_haut.append(point_haut_ancienne_base_2)

    
        
    coord_point_new_base.append(coord_point_new_base[0])
    coord_point_haut_new_base.append(coord_point_haut_new_base[0])

    if avec_dome :

        mesh_dome = dome(rayon,centre_nouvelle_base,"-",coord_point_new_base,inverse_matrice(matrice))
        mesh_dome += dome(rayon,centre_nouvelle_base_haut,"+",coord_point_haut_new_base,inverse_matrice(matrice))

    if not avec_dome :

        mesh_dome = []

    coord_point.append(coord_point[0]) # pour fermer le cylindre
    coord_point_haut.append(coord_point_haut[0])

    return coord_point,coord_point_haut,mesh_dome

def polygone_ellipse(centre,nombre_points,rayon,hauteur,matrice,avec_dome) :
    '''
    # cette fonction crée deux polygones elliptiques à partir d'un point qui sera le centre du premier polygone, le centre du second est le centre du premier translaté 

    ##########################

    ##########
    # entrée #
    ##########

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # nombre_points (type int) : le nombre de sommets du polygone

    # rayon (type float ou int) : distance centre-sommet

    # hauteur (type float ou int) : distance entre le centre du premier polygone et le centre du second polygone

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    # avec_dome (type bool) : si on veut les extrémités du cordon
    
    ##########
    # sortie #
    ##########

    # coord_point (type list) : liste des coordonnées des différents sommets du premier polygone sous le format [[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]]

    # coord_point_haut (type list) : liste des coordonnées des différents sommets du second polygone sous le format [[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]]

    # mesh_dome (type list) : mesh représentant les extrémités (liste vide si pas d'extrémités)

    ##########################'''

    coord_point = []
    coord_point_haut = []
    coord_point_new_base = []
    coord_point_haut_new_base = []
    centre_nouvelle_base = prod_matriciel(matrice,centre)
    centre_nouvelle_base_haut = operation_vecteur(centre_nouvelle_base,[0,hauteur,0],"+")
    parametre = 1.3*rayon

    for i in range(nombre_points) :

        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
        y=centre_nouvelle_base[2]+parametre*sin(2*pi/nombre_points*i)

        point_bas = [x,centre_nouvelle_base[1],y]
        point_haut = [x,centre_nouvelle_base[1]+hauteur,y]

        coord_point_new_base.append(point_bas)
        coord_point_haut_new_base.append(point_haut)


        point_bas_ancienne_base = prod_matriciel(inverse_matrice(matrice),point_bas)
        point_haut_ancienne_base = prod_matriciel(inverse_matrice(matrice),point_haut)
        
        coord_point.append(point_bas_ancienne_base)
        coord_point_haut.append(point_haut_ancienne_base)

    coord_point_new_base.append(coord_point_new_base[0])
    coord_point_haut_new_base.append(coord_point_haut_new_base[0])

    if avec_dome :

        mesh_dome = dome(rayon,centre_nouvelle_base,"-",coord_point_new_base,inverse_matrice(matrice))
        mesh_dome += dome(rayon,centre_nouvelle_base_haut,"+",coord_point_haut_new_base,inverse_matrice(matrice))

    if not avec_dome :

        mesh_dome = []
        
    coord_point.append(coord_point[0]) # pour fermer le cylindre
    coord_point_haut.append(coord_point_haut[0])

    return coord_point,coord_point_haut,mesh_dome 

def dome(rayon,centre,signe,coordonnee,matrice) :

    '''
    # cette fonction retourne le mesh représentant les extrémités du cordon

    ##########################

    ##########
    # entrée #
    ##########

    # rayon (type float ou int) : distance centre-sommet

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # signe (type str) : si on veut la première extrémité :"-", si on veut l'autre extrémité :"+"

    # coordonnee (type list) : liste des coordonnées des points appartenant à la base du cordon sous le format [[x1,y1,z1],[x2,y2,z2],...]

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    ##########
    # sortie #
    ##########

    # mesh (type list) : liste sous le format défini par la fonction load_mesh, mesh correspondant aux extrémités

    ##########################'''

    mesh = []
    
    centre_dome = operation_vecteur(centre,[0,rayon,0],signe)

    for i in range(len(coordonnee)) :

        if i == len(coordonnee)-1 :
            apres = 0

        else :
            apres = i+1

        facette_new_base = [centre_dome,coordonnee[i],coordonnee[apres]]
        vec_normal = normale_face(facette_new_base)
        
        if signe == "+"  :
            
            
            facette = [prod_matriciel(matrice,centre_dome),prod_matriciel(matrice,coordonnee[apres]),prod_matriciel(matrice,coordonnee[i])]

        if signe == "-" :

            facette = [prod_matriciel(matrice,centre_dome),prod_matriciel(matrice,coordonnee[i]),prod_matriciel(matrice,coordonnee[apres])]

        if signe == "+" and vec_normal[1] < 0 :

            vec_normal = operation_vecteur(vec_normal,-1,"*")

        if signe == "-" and vec_normal[1] > 0 :

            vec_normal = operation_vecteur(vec_normal,-1,"*")

        vec_normale_bonne_base = prod_matriciel(matrice,vec_normal)

        mesh.append([vec_normale_bonne_base,facette])

    return mesh

#####################################################################################################
#####################################################################################################
#####################################################################################################

# fonctions incluant un maillage

def polygone_regulier_maille(centre,nombre_points,rayon,hauteur,matrice,parametre_de_maille,orientation_maille,coord_de_depart) :
    '''
    # cette fonction crée des polygones réguliers intermédiaires, mode losange, à partir d'un point qui sera le centre du premier polygone, le centre du second est le centre du premier translaté 

    ##########################

    ##########
    # entrée #
    ##########

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # nombre_points (type int) : le nombre de sommets du polygone

    # rayon (type float ou int) : distance centre-sommet

    # hauteur (type float ou int) : distance entre le centre du premier polygone et le centre du second polygone

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    # parametre_de_maille (type int ou float) : espace entre chaque polygone intermédiaire

    # orientation_maille (type str) : "+" si on commence par la gauche, "-" si on commence par la droite

    # coord_de_depart (type int ou float) : correspond à l'origine du maillage
    
    ##########
    # sortie #
    ##########

    # coord_point_tot (type list) : liste des coordonnées des différents sommets des polygones intermédiaires sous le format [[[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]],...]

    # liste_coord_centre (type list) : liste des coordonnées des centres successifs du cordon sous le format [[[x1,y1,z1],[x2,y2,z2]],[[x2,y2,z2],[x3,y3,z3]],...]

    ##########################'''

    coord_point_tot = []
    centre_nouvelle_base = prod_matriciel(matrice,centre)
    centre_nouvelle_base_haut = operation_vecteur(centre_nouvelle_base,[0,hauteur,0],"+")
    liste_centre = [centre]
    
    j = coord_de_depart
    indice = 0

    while j < centre_nouvelle_base[1]+hauteur :

        if j > centre_nouvelle_base[1] :

            coord_point = []
            
            for i in range(nombre_points) :

                if (float(indice)/parametre_de_maille)%2 == 0 :

                    if orientation_maille == "+" :

                        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                        y=centre_nouvelle_base[2]+float(rayon)/2+rayon*sin(2*pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]+float(rayon)/2]

                    else :

                        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                        y=centre_nouvelle_base[2]-float(rayon)/2+rayon*sin(2*pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]-float(rayon)/2]

                if (float(indice)/parametre_de_maille)%2 != 0 :

                    if orientation_maille == "+" :

                        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                        y=centre_nouvelle_base[2]-float(rayon)/2+rayon*sin(2*pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]-float(rayon)/2]

                    else :

                        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                        y=centre_nouvelle_base[2]+float(rayon)/2+rayon*sin(2*pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]+float(rayon)/2]
                        

                point_bas = [x,j,y]

                liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_poly))

                point_bas_ancienne_base = prod_matriciel(inverse_matrice(matrice),point_bas)
                
                coord_point.append(point_bas_ancienne_base)

            coord_point.append(coord_point[0])
            coord_point_tot.append(coord_point)

        j += parametre_de_maille
        indice += parametre_de_maille

    liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_nouvelle_base_haut))

    liste_coord_centre = []

    for j in range(len(liste_centre)-1) :

        liste_coord_centre.append([liste_centre[j],liste_centre[j+1]])

    return coord_point_tot,liste_coord_centre

def polygone_clavette_maille(centre,nombre_points,rayon,hauteur,matrice,parametre_de_maille,orientation_maille,coord_de_depart) :
    '''
    # cette fonction crée des clavettes intermédiaires, mode losange, à partir d'un point qui sera le centre du premier polygone, le centre du second est le centre du premier translaté 

    ##########################

    ##########
    # entrée #
    ##########

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # nombre_points (type int) : le nombre de sommets du polygone

    # rayon (type float ou int) : distance centre-sommet

    # hauteur (type float ou int) : distance entre le centre du premier polygone et le centre du second polygone

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    # parametre_de_maille (type int ou float) : espace entre chaque polygone intermédiaire

    # orientation_maille (type str) : "+" si on commence par la gauche, "-" si on commence par la droite

    # coord_de_depart (type int ou float) : correspond à l'origine du maillage

    ##########
    # sortie #
    ##########

    # coord_point_tot (type list) : liste des coordonnées des différents sommets des polygones intermédiaires sous le format [[[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]],...]

    # liste_coord_centre (type list) : liste des coordonnées des centres successifs du cordon sous le format [[[x1,y1,z1],[x2,y2,z2]],[[x2,y2,z2],[x3,y3,z3]],...]

    ##########################'''

    coord_point_tot = []
    centre_nouvelle_base = prod_matriciel(matrice,centre)
    centre_nouvelle_base_haut = operation_vecteur(centre_nouvelle_base,[0,hauteur,0],"+")
    liste_centre = [centre]
    
    centre_nouvelle_base_1 = operation_vecteur(centre_nouvelle_base,[0,0,float(rayon)/2],"+")
    centre_nouvelle_base_2 = operation_vecteur(centre_nouvelle_base,[0,0,float(rayon)/2],"-")

    j = coord_de_depart
    indice = 0

    while j < centre_nouvelle_base[1]+hauteur :

        if j > centre_nouvelle_base[1] :

            coord_point = []

            for i in range(2*nombre_points) :

                if i <= nombre_points-1 :

                    if (float(indice)/parametre_de_maille)%2 == 0 :

                        if orientation_maille == "+" :
                    
                            x_1 = centre_nouvelle_base_1[0]+rayon*cos(pi/nombre_points*i)
                            y_1 = centre_nouvelle_base_1[2]+float(rayon)+rayon*sin(pi/nombre_points*i)
                            centre_poly = [centre_nouvelle_base_1[0],j,centre_nouvelle_base_1[2]+float(rayon)]

                        else :

                            x_1 = centre_nouvelle_base_1[0]+rayon*cos(pi/nombre_points*i)
                            y_1 = centre_nouvelle_base_1[2]-float(rayon)+rayon*sin(pi/nombre_points*i)
                            centre_poly = [centre_nouvelle_base_1[0],j,centre_nouvelle_base_1[2]-float(rayon)]

                    if (float(indice)/parametre_de_maille)%2 != 0 :

                        if orientation_maille == "+" :
                    
                            x_1 = centre_nouvelle_base_1[0]+rayon*cos(pi/nombre_points*i)
                            y_1 = centre_nouvelle_base_1[2]-float(rayon)+rayon*sin(pi/nombre_points*i)
                            centre_poly = [centre_nouvelle_base_1[0],j,centre_nouvelle_base_1[2]-float(rayon)]

                        else :

                            x_1 = centre_nouvelle_base_1[0]+rayon*cos(pi/nombre_points*i)
                            y_1 = centre_nouvelle_base_1[2]+float(rayon)+rayon*sin(pi/nombre_points*i)
                            centre_poly = [centre_nouvelle_base_1[0],j,centre_nouvelle_base_1[2]+float(rayon)]

                    point_bas_1 = [x_1,j,y_1]    

                    point_bas_ancienne_base_1 = prod_matriciel(inverse_matrice(matrice),point_bas_1)
                    
                    
                    coord_point.append(point_bas_ancienne_base_1)

                else :

                    if (float(indice)/parametre_de_maille)%2 == 0 :

                        if orientation_maille == "+" :

                            x_2 = centre_nouvelle_base_2[0]+rayon*cos(pi/nombre_points*i)
                            y_2 = centre_nouvelle_base_2[2]+float(rayon)+rayon*sin(pi/nombre_points*i)
                            centre_poly = [centre_nouvelle_base_2[0],j,centre_nouvelle_base_2[2]+float(rayon)]

                        else :

                            x_2 = centre_nouvelle_base_2[0]+rayon*cos(pi/nombre_points*i)
                            y_2 = centre_nouvelle_base_2[2]-float(rayon)+rayon*sin(pi/nombre_points*i)
                            centre_poly = [centre_nouvelle_base_2[0],j,centre_nouvelle_base_2[2]-float(rayon)]

                    if (float(indice)/parametre_de_maille)%2 != 0 :

                        if orientation_maille == "+" :

                            x_2 = centre_nouvelle_base_2[0]+rayon*cos(pi/nombre_points*i)
                            y_2 = centre_nouvelle_base_2[2]-float(rayon)+rayon*sin(pi/nombre_points*i)
                            centre_poly = [centre_nouvelle_base_2[0],j,centre_nouvelle_base_2[2]-float(rayon)]

                        else :

                            x_2 = centre_nouvelle_base_2[0]+rayon*cos(pi/nombre_points*i)
                            y_2 = centre_nouvelle_base_2[2]+float(rayon)+rayon*sin(pi/nombre_points*i)
                            centre_poly = [centre_nouvelle_base_2[0],j,centre_nouvelle_base_2[2]+float(rayon)]

                    point_bas_2 = [x_2,j,y_2]

                    point_bas_ancienne_base_2 = prod_matriciel(inverse_matrice(matrice),point_bas_2)

                    coord_point.append(point_bas_ancienne_base_2)

                liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_poly))

            coord_point.append(coord_point[0])
            coord_point_tot.append(coord_point)

        j += parametre_de_maille
        indice += parametre_de_maille

    liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_nouvelle_base_haut))

    liste_coord_centre = []

    for j in range(len(liste_centre)-1) :

        liste_coord_centre.append([liste_centre[j],liste_centre[j+1]])

    return coord_point_tot,liste_coord_centre

def polygone_ellipse_maille(centre,nombre_points,rayon,hauteur,matrice,parametre_de_maille,orientation_maille,coord_de_depart) :
    '''
    # cette fonction crée des ellipses intermédiaires, mode losange, à partir d'un point qui sera le centre du premier polygone, le centre du second est le centre du premier translaté 

    ##########################

    ##########
    # entrée #
    ##########

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # nombre_points (type int) : le nombre de sommets du polygone

    # rayon (type float ou int) : distance centre-sommet

    # hauteur (type float ou int) : distance entre le centre du premier polygone et le centre du second polygone

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    # parametre_de_maille (type int ou float) : espace entre chaque polygone intermédiaire

    # orientation_maille (type str) : "+" si on commence par la gauche, "-" si on commence par la droite

    # coord_de_depart (type int ou float) : correspond à l'origine du maillage
    
    ##########
    # sortie #
    ##########

    # coord_point_tot (type list) : liste des coordonnées des différents sommets des polygones intermédiaires sous le format [[[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]],...]

    # liste_coord_centre (type list) : liste des coordonnées des centres successifs du cordon sous le format [[[x1,y1,z1],[x2,y2,z2]],[[x2,y2,z2],[x3,y3,z3]],...]

    ##########################'''

    coord_point_tot = []
    centre_nouvelle_base = prod_matriciel(matrice,centre)
    centre_nouvelle_base_haut = operation_vecteur(centre_nouvelle_base,[0,hauteur,0],"+")
    liste_centre = [centre]
    
    j = coord_de_depart
    indice = 0
    parametre = 1.3*rayon

    while j < centre_nouvelle_base[1]+hauteur :

        if j > centre_nouvelle_base[1] :

            coord_point = []
            
            for i in range(nombre_points) :

                if (float(indice)/parametre_de_maille)%2 == 0 :

                    if orientation_maille == "+" :

                        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                        y=centre_nouvelle_base[2]+float(rayon)/2+parametre*sin(2*pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]+float(rayon)/2]

                    else :

                        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                        y=centre_nouvelle_base[2]-float(rayon)/2+parametre*sin(2*pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]-float(rayon)/2]

                if (float(indice)/parametre_de_maille)%2 != 0 :

                    if orientation_maille == "+" :

                        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                        y=centre_nouvelle_base[2]-float(rayon)/2+parametre*sin(2*pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]-float(rayon)/2]

                    else :

                        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                        y=centre_nouvelle_base[2]+float(rayon)/2+parametre*sin(2*pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]+float(rayon)/2]
                        

                point_bas = [x,j,y]

                liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_poly))

                point_bas_ancienne_base = prod_matriciel(inverse_matrice(matrice),point_bas)
                
                coord_point.append(point_bas_ancienne_base)

            coord_point.append(coord_point[0])
            coord_point_tot.append(coord_point)

        j += parametre_de_maille
        indice += parametre_de_maille

    liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_nouvelle_base_haut))

    liste_coord_centre = []

    for j in range(len(liste_centre)-1) :

        liste_coord_centre.append([liste_centre[j],liste_centre[j+1]])

    return coord_point_tot,liste_coord_centre

def polygone_regulier_hex(centre,nombre_points,rayon,hauteur,matrice,parametre_de_maille,orientation_maille,coord_de_depart) :
    '''
    # cette fonction crée des polygones réguliers intermédiaires, mode hexagonal, à partir d'un point qui sera le centre du premier polygone, le centre du second est le centre du premier translaté 

    ##########################

    ##########
    # entrée #
    ##########

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # nombre_points (type int) : le nombre de sommets du polygone

    # rayon (type float ou int) : distance centre-sommet

    # hauteur (type float ou int) : distance entre le centre du premier polygone et le centre du second polygone

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    # parametre_de_maille (type int ou float) : espace entre chaque polygone intermédiaire

    # orientation_maille (type str) : "+" si on commence par la gauche, "-" si on commence par la droite

    # coord_de_depart (type int ou float) : correspond à l'origine du maillage
    
    ##########
    # sortie #
    ##########

    # coord_point_tot (type list) : liste des coordonnées des différents sommets des polygones intermédiaires sous le format [[[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]],...]

    # liste_coord_centre (type list) : liste des coordonnées des centres successifs du cordon sous le format [[[x1,y1,z1],[x2,y2,z2]],[[x2,y2,z2],[x3,y3,z3]],...]

    ##########################'''

    coord_point_tot = []
    centre_nouvelle_base = prod_matriciel(matrice,centre)
    centre_nouvelle_base_haut = operation_vecteur(centre_nouvelle_base,[0,hauteur,0],"+")
    liste_centre = [centre]
    
    j = coord_de_depart
    indice = 0

    while j < centre_nouvelle_base[1]+hauteur :

        if j > centre_nouvelle_base[1] :

            coord_point = []
            
            for i in range(nombre_points) :

                if indice == 0 or indice == 3 :

                    x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                    y=centre_nouvelle_base[2]+rayon*sin(2*pi/nombre_points*i)
                    centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]]

                if indice == 1 or indice == 2 :

                    if orientation_maille == "+" :

                        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                        y=centre_nouvelle_base[2]+float(rayon)+rayon*sin(2*pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]+float(rayon)]

                    else :

                        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                        y=centre_nouvelle_base[2]-float(rayon)+rayon*sin(2*pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]-float(rayon)]                        

                point_bas = [x,j,y]

                liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_poly))

                point_bas_ancienne_base = prod_matriciel(inverse_matrice(matrice),point_bas)
                
                coord_point.append(point_bas_ancienne_base)

            coord_point.append(coord_point[0])
            coord_point_tot.append(coord_point)

        j += parametre_de_maille
        indice += 1
        
        if indice > 3 :

            indice = 0

    liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_nouvelle_base_haut))

    liste_coord_centre = []

    for j in range(len(liste_centre)-1) :

        liste_coord_centre.append([liste_centre[j],liste_centre[j+1]])

    return coord_point_tot,liste_coord_centre

def polygone_clavette_hex(centre,nombre_points,rayon,hauteur,matrice,parametre_de_maille,orientation_maille,coord_de_depart) :
    '''
    # cette fonction crée des clavettes intermédiaires, mode hexagonal, à partir d'un point qui sera le centre du premier polygone, le centre du second est le centre du premier translaté 

    ##########################

    ##########
    # entrée #
    ##########

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # nombre_points (type int) : le nombre de sommets du polygone

    # rayon (type float ou int) : distance centre-sommet

    # hauteur (type float ou int) : distance entre le centre du premier polygone et le centre du second polygone

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    # parametre_de_maille (type int ou float) : espace entre chaque polygone intermédiaire

    # orientation_maille (type str) : "+" si on commence par la gauche, "-" si on commence par la droite

    # coord_de_depart (type int ou float) : correspond à l'origine du maillage

    ##########
    # sortie #
    ##########

    # coord_point_tot (type list) : liste des coordonnées des différents sommets des polygones intermédiaires sous le format [[[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]],...]

    # liste_coord_centre (type list) : liste des coordonnées des centres successifs du cordon sous le format [[[x1,y1,z1],[x2,y2,z2]],[[x2,y2,z2],[x3,y3,z3]],...]

    ##########################'''

    coord_point_tot = []
    centre_nouvelle_base = prod_matriciel(matrice,centre)
    centre_nouvelle_base_haut = operation_vecteur(centre_nouvelle_base,[0,hauteur,0],"+")
    liste_centre = [centre]
    
    centre_nouvelle_base_1 = operation_vecteur(centre_nouvelle_base,[0,0,float(rayon)/2],"+")
    centre_nouvelle_base_2 = operation_vecteur(centre_nouvelle_base,[0,0,float(rayon)/2],"-")

    j = coord_de_depart
    indice = 0

    while j < centre_nouvelle_base[1]+hauteur :

        if j > centre_nouvelle_base[1] :

            coord_point = []

            for i in range(2*nombre_points) :

                if i <= nombre_points-1 :

                    if indice == 0 or indice == 3 :

                        x_1 = centre_nouvelle_base_1[0]+rayon*cos(pi/nombre_points*i)
                        y_1 = centre_nouvelle_base_1[2]+rayon*sin(pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base_1[0],j,centre_nouvelle_base_1[2]]

                    if indice == 1 or indice == 2 :

                        if orientation_maille == "+" :
                    
                            x_1 = centre_nouvelle_base_1[0]+rayon*cos(pi/nombre_points*i)
                            y_1 = centre_nouvelle_base_1[2]+float(rayon)+rayon*sin(pi/nombre_points*i)
                            centre_poly = [centre_nouvelle_base_1[0],j,centre_nouvelle_base_1[2]+float(rayon)]

                        else :

                            x_1 = centre_nouvelle_base_1[0]+rayon*cos(pi/nombre_points*i)
                            y_1 = centre_nouvelle_base_1[2]-float(rayon)+rayon*sin(pi/nombre_points*i)
                            centre_poly = [centre_nouvelle_base_1[0],j,centre_nouvelle_base_1[2]-float(rayon)]

                    point_bas_1 = [x_1,j,y_1]    

                    point_bas_ancienne_base_1 = prod_matriciel(inverse_matrice(matrice),point_bas_1)
                    
                    
                    coord_point.append(point_bas_ancienne_base_1)

                else :

                    if indice == 0 or indice == 3 :

                        x_2 = centre_nouvelle_base_2[0]+rayon*cos(pi/nombre_points*i)
                        y_2 = centre_nouvelle_base_2[2]+rayon*sin(pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base_1[0],j,centre_nouvelle_base_1[2]]

                    if indice == 1 or indice == 2 :

                        if orientation_maille == "+" :

                            x_2 = centre_nouvelle_base_2[0]+rayon*cos(pi/nombre_points*i)
                            y_2 = centre_nouvelle_base_2[2]+float(rayon)+rayon*sin(pi/nombre_points*i)
                            centre_poly = [centre_nouvelle_base_2[0],j,centre_nouvelle_base_2[2]+float(rayon)]

                        else :

                            x_2 = centre_nouvelle_base_2[0]+rayon*cos(pi/nombre_points*i)
                            y_2 = centre_nouvelle_base_2[2]-float(rayon)+rayon*sin(pi/nombre_points*i)
                            centre_poly = [centre_nouvelle_base_2[0],j,centre_nouvelle_base_2[2]-float(rayon)]

                    point_bas_2 = [x_2,j,y_2]

                    point_bas_ancienne_base_2 = prod_matriciel(inverse_matrice(matrice),point_bas_2)

                    coord_point.append(point_bas_ancienne_base_2)

                liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_poly))

            coord_point.append(coord_point[0])
            coord_point_tot.append(coord_point)

        j += parametre_de_maille
        indice += 1

        if indice > 3 :

            indice = 0

    liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_nouvelle_base_haut))

    liste_coord_centre = []

    for j in range(len(liste_centre)-1) :

        liste_coord_centre.append([liste_centre[j],liste_centre[j+1]])

    return coord_point_tot,liste_coord_centre

def polygone_ellipse_hex(centre,nombre_points,rayon,hauteur,matrice,parametre_de_maille,orientation_maille,coord_de_depart) :
    '''
    # cette fonction crée des ellipses intermédiaires, mode hexagonal, à partir d'un point qui sera le centre du premier polygone, le centre du second est le centre du premier translaté 

    ##########################

    ##########
    # entrée #
    ##########

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # nombre_points (type int) : le nombre de sommets du polygone

    # rayon (type float ou int) : distance centre-sommet

    # hauteur (type float ou int) : distance entre le centre du premier polygone et le centre du second polygone

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    # parametre_de_maille (type int ou float) : espace entre chaque polygone intermédiaire

    # orientation_maille (type str) : "+" si on commence par la gauche, "-" si on commence par la droite

    # coord_de_depart (type int ou float) : correspond à l'origine du maillage
    
    ##########
    # sortie #
    ##########

    # coord_point_tot (type list) : liste des coordonnées des différents sommets des polygones intermédiaires sous le format [[[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]],...]

    # liste_coord_centre (type list) : liste des coordonnées des centres successifs du cordon sous le format [[[x1,y1,z1],[x2,y2,z2]],[[x2,y2,z2],[x3,y3,z3]],...]

    ##########################'''

    coord_point_tot = []
    centre_nouvelle_base = prod_matriciel(matrice,centre)
    centre_nouvelle_base_haut = operation_vecteur(centre_nouvelle_base,[0,hauteur,0],"+")
    liste_centre = [centre]
    parametre = 1.3*rayon
    
    j = coord_de_depart
    indice = 0

    while j < centre_nouvelle_base[1]+hauteur :

        if j > centre_nouvelle_base[1] :

            coord_point = []
            
            for i in range(nombre_points) :

                if indice == 0 or indice == 3 :

                    x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                    y=centre_nouvelle_base[2]+parametre*sin(2*pi/nombre_points*i)
                    centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]]

                if indice == 1 or indice == 2 :

                    if orientation_maille == "+" :

                        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                        y=centre_nouvelle_base[2]+float(rayon)+parametre*sin(2*pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]+float(rayon)]

                    else :

                        x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                        y=centre_nouvelle_base[2]-float(rayon)+parametre*sin(2*pi/nombre_points*i)
                        centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]-float(rayon)]                        

                point_bas = [x,j,y]

                liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_poly))

                point_bas_ancienne_base = prod_matriciel(inverse_matrice(matrice),point_bas)
                
                coord_point.append(point_bas_ancienne_base)

            coord_point.append(coord_point[0])
            coord_point_tot.append(coord_point)

        j += parametre_de_maille
        indice += 1
        
        if indice > 3 :

            indice = 0

    liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_nouvelle_base_haut))

    liste_coord_centre = []

    for j in range(len(liste_centre)-1) :

        liste_coord_centre.append([liste_centre[j],liste_centre[j+1]])

    return coord_point_tot,liste_coord_centre

def polygone_regulier_alea(centre,nombre_points,rayon,hauteur,matrice,parametre_de_maille,orientation_maille,coord_de_depart) :
    '''
    # cette fonction crée des polygones réguliers intermédiaires, mode aléatoire, à partir d'un point qui sera le centre du premier polygone, le centre du second est le centre du premier translaté 

    ##########################

    ##########
    # entrée #
    ##########

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # nombre_points (type int) : le nombre de sommets du polygone

    # rayon (type float ou int) : distance centre-sommet

    # hauteur (type float ou int) : distance entre le centre du premier polygone et le centre du second polygone

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    # parametre_de_maille (type int ou float) : espace entre chaque polygone intermédiaire

    # orientation_maille (type str) : "+" si on commence par la gauche, "-" si on commence par la droite

    # coord_de_depart (type int ou float) : correspond à l'origine du maillage
    
    ##########
    # sortie #
    ##########

    # coord_point_tot (type list) : liste des coordonnées des différents sommets des polygones intermédiaires sous le format [[[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]],...]

    # liste_coord_centre (type list) : liste des coordonnées des centres successifs du cordon sous le format [[[x1,y1,z1],[x2,y2,z2]],[[x2,y2,z2],[x3,y3,z3]],...]

    ##########################'''

    coord_point_tot = []
    centre_nouvelle_base = prod_matriciel(matrice,centre)
    centre_nouvelle_base_haut = operation_vecteur(centre_nouvelle_base,[0,hauteur,0],"+")
    liste_centre = [centre]
    
    j = coord_de_depart
    aleatoire = randint(-5,5)
    indice = float(aleatoire)/5

    while j < centre_nouvelle_base[1]+hauteur :

        if j > centre_nouvelle_base[1] :

            coord_point = []
            
            for i in range(nombre_points) :
                
                x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                y=centre_nouvelle_base[2]+rayon*indice+rayon*sin(2*pi/nombre_points*i)
                centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]+rayon*indice]                       

                point_bas = [x,j,y]

                liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_poly))

                point_bas_ancienne_base = prod_matriciel(inverse_matrice(matrice),point_bas)
                
                coord_point.append(point_bas_ancienne_base)

            coord_point.append(coord_point[0])
            coord_point_tot.append(coord_point)

        j += parametre_de_maille
        aleatoire = randint(-5,5)
        indice = float(aleatoire)/5

    liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_nouvelle_base_haut))

    liste_coord_centre = []

    for j in range(len(liste_centre)-1) :

        liste_coord_centre.append([liste_centre[j],liste_centre[j+1]])

    return coord_point_tot,liste_coord_centre

def polygone_clavette_alea(centre,nombre_points,rayon,hauteur,matrice,parametre_de_maille,orientation_maille,coord_de_depart) :
    '''
    # cette fonction crée des clavettes intermédiaires, mode aléatoire, à partir d'un point qui sera le centre du premier polygone, le centre du second est le centre du premier translaté 

    ##########################

    ##########
    # entrée #
    ##########

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # nombre_points (type int) : le nombre de sommets du polygone

    # rayon (type float ou int) : distance centre-sommet

    # hauteur (type float ou int) : distance entre le centre du premier polygone et le centre du second polygone

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    # parametre_de_maille (type int ou float) : espace entre chaque polygone intermédiaire

    # orientation_maille (type str) : "+" si on commence par la gauche, "-" si on commence par la droite

    # coord_de_depart (type int ou float) : correspond à l'origine du maillage

    ##########
    # sortie #
    ##########

    # coord_point_tot (type list) : liste des coordonnées des différents sommets des polygones intermédiaires sous le format [[[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]],...]

    # liste_coord_centre (type list) : liste des coordonnées des centres successifs du cordon sous le format [[[x1,y1,z1],[x2,y2,z2]],[[x2,y2,z2],[x3,y3,z3]],...]

    ##########################'''

    coord_point_tot = []
    centre_nouvelle_base = prod_matriciel(matrice,centre)
    centre_nouvelle_base_haut = operation_vecteur(centre_nouvelle_base,[0,hauteur,0],"+")
    liste_centre = [centre]
    
    centre_nouvelle_base_1 = operation_vecteur(centre_nouvelle_base,[0,0,float(rayon)/2],"+")
    centre_nouvelle_base_2 = operation_vecteur(centre_nouvelle_base,[0,0,float(rayon)/2],"-")

    j = coord_de_depart
    aleatoire = randint(-5,5)
    indice = float(aleatoire)/5

    while j < centre_nouvelle_base[1]+hauteur :

        if j > centre_nouvelle_base[1] :

            coord_point = []

            for i in range(2*nombre_points) :

                if i <= nombre_points-1 :

                    x_1 = centre_nouvelle_base_1[0]+rayon*indice+rayon*cos(pi/nombre_points*i)
                    y_1 = centre_nouvelle_base_1[2]+rayon*indice+rayon*sin(pi/nombre_points*i)
                    centre_poly = [centre_nouvelle_base_1[0],j,centre_nouvelle_base_1[2]+rayon*indice]

                    point_bas_1 = [x_1,j,y_1]    

                    point_bas_ancienne_base_1 = prod_matriciel(inverse_matrice(matrice),point_bas_1)
                    
                    
                    coord_point.append(point_bas_ancienne_base_1)

                else :

                    x_2 = centre_nouvelle_base_2[0]+rayon*indice+rayon*cos(pi/nombre_points*i)
                    y_2 = centre_nouvelle_base_2[2]+rayon*indice+rayon*sin(pi/nombre_points*i)
                    centre_poly = [centre_nouvelle_base_1[0],j,centre_nouvelle_base_1[2]+rayon*indice]

                    point_bas_2 = [x_2,j,y_2]

                    point_bas_ancienne_base_2 = prod_matriciel(inverse_matrice(matrice),point_bas_2)

                    coord_point.append(point_bas_ancienne_base_2)

                liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_poly))

            coord_point.append(coord_point[0])
            coord_point_tot.append(coord_point)

        j += parametre_de_maille
        aleatoire = randint(-5,5)
        indice = float(aleatoire)/5
        
    liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_nouvelle_base_haut))

    liste_coord_centre = []

    for j in range(len(liste_centre)-1) :

        liste_coord_centre.append([liste_centre[j],liste_centre[j+1]])

    return coord_point_tot,liste_coord_centre

def polygone_ellipse_alea(centre,nombre_points,rayon,hauteur,matrice,parametre_de_maille,orientation_maille,coord_de_depart) :
    '''
    # cette fonction crée des ellipses intermédiaires, mode aléatoire, à partir d'un point qui sera le centre du premier polygone, le centre du second est le centre du premier translaté 

    ##########################

    ##########
    # entrée #
    ##########

    # centre (type list) : liste des coordonnées du centre du polygone sous le format [x,y,z]

    # nombre_points (type int) : le nombre de sommets du polygone

    # rayon (type float ou int) : distance centre-sommet

    # hauteur (type float ou int) : distance entre le centre du premier polygone et le centre du second polygone

    # matrice (type list) : matrice carrée 3X3 correspond à la matrice de passage de la base canonique à la base de la normale du premier polygone orienté vers le second polygone

    # parametre_de_maille (type int ou float) : espace entre chaque polygone intermédiaire

    # orientation_maille (type str) : "+" si on commence par la gauche, "-" si on commence par la droite

    # coord_de_depart (type int ou float) : correspond à l'origine du maillage
    
    ##########
    # sortie #
    ##########

    # coord_point_tot (type list) : liste des coordonnées des différents sommets des polygones intermédiaires sous le format [[[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]],...]

    # liste_coord_centre (type list) : liste des coordonnées des centres successifs du cordon sous le format [[[x1,y1,z1],[x2,y2,z2]],[[x2,y2,z2],[x3,y3,z3]],...]

    ##########################'''

    coord_point_tot = []
    centre_nouvelle_base = prod_matriciel(matrice,centre)
    centre_nouvelle_base_haut = operation_vecteur(centre_nouvelle_base,[0,hauteur,0],"+")
    liste_centre = [centre]
    parametre = 1.3*rayon
    
    j = coord_de_depart
    aleatoire = randint(-5,5)
    indice = float(aleatoire)/5

    while j < centre_nouvelle_base[1]+hauteur :

        if j > centre_nouvelle_base[1] :

            coord_point = []
            
            for i in range(nombre_points) :
                
                x=centre_nouvelle_base[0]+rayon*cos(2*pi/nombre_points*i)
                y=centre_nouvelle_base[2]+rayon*indice+parametre*sin(2*pi/nombre_points*i)
                centre_poly = [centre_nouvelle_base[0],j,centre_nouvelle_base[2]+rayon*indice]                       

                point_bas = [x,j,y]

                liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_poly))

                point_bas_ancienne_base = prod_matriciel(inverse_matrice(matrice),point_bas)
                
                coord_point.append(point_bas_ancienne_base)

            coord_point.append(coord_point[0])
            coord_point_tot.append(coord_point)

        j += parametre_de_maille
        aleatoire = randint(-5,5)
        indice = float(aleatoire)/5

    liste_centre.append(prod_matriciel(inverse_matrice(matrice),centre_nouvelle_base_haut))

    liste_coord_centre = []

    for j in range(len(liste_centre)-1) :

        liste_coord_centre.append([liste_centre[j],liste_centre[j+1]])

    return coord_point_tot,liste_coord_centre




        

        

    
        
                                

    

    
    
