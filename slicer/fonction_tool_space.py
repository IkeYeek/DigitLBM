# coding:latin-1

from slicer.fonction_matrice import *
from slicer.AdditionalFunction import rad
from slicer.fonction_vecteur import operation_vecteur
from math import cos,sin

def rotate_mesh(mesh,axe,angle_en_deg) :
    '''
    # cette fonction effectue une rotation de l'objet par rapport à un axe selon un certain angle

    ##########################

    ##########
    # entrée #
    ##########

    # mesh (type list) : liste sous le format défini par la fonction load_mesh représentant l'objet

    # axe (type str) : axe selon lequel on effectue la rotation

    # angle_en_deg (type int ou float) : angle en degré de la rotation 

    ##########
    # sortie #
    ##########

    # mesh_apres_rotation (type list) : liste sous le format défini par la fonction load_mesh représentant l'objet après rotation

    ##########################'''

    angle = rad(angle_en_deg)
    mesh_apres_rotation = []

    if axe == "x" :

        unitaire = [1,0,0]
        vecteur_1 = [0,cos(angle),sin(angle)]
        vecteur_2 = [0,-sin(angle),cos(angle)]

        matrice = mise_en_base(unitaire,vecteur_1,vecteur_2)

    if axe == "y" :

        unitaire = [0,1,0]
        vecteur_1 = [cos(angle),0,-sin(angle)]
        vecteur_2 = [sin(angle),0,cos(angle)]

        matrice = mise_en_base(vecteur_1,unitaire,vecteur_2)

    if axe == "z" :

        unitaire = [0,0,1]
        vecteur_1 = [cos(angle),sin(angle),0]
        vecteur_2 = [-sin(angle),cos(angle),0]

        matrice = mise_en_base(vecteur_1,vecteur_2,unitaire)

    for i in range(len(mesh)) :

        new_normal = prod_matriciel(matrice,mesh[i][0])
        new_point_1 = prod_matriciel(matrice,mesh[i][1][0])
        new_point_2 = prod_matriciel(matrice,mesh[i][1][1])
        new_point_3 = prod_matriciel(matrice,mesh[i][1][2])

        mesh_apres_rotation.append([new_normal,[new_point_1,new_point_2,new_point_3]])

    return mesh_apres_rotation

def translation_mesh(mesh,translation_selon_x,translation_selon_y,translation_selon_z) :
    '''
    # cette fonction effectue une translation de l'objet dans l'espace

    ##########################

    ##########
    # entrée #
    ##########

    # mesh (type list) : liste sous le format défini par la fonction load_mesh représentant l'objet

    # translation_selon_x (type int ou float) : translation selon l'axe x

    # translation_selon_y (type int ou float) : translation selon l'axe y

    # translation_selon_z (type int ou float) : translation selon l'axe z

    ##########
    # sortie #
    ##########

    # new_mesh (type list) : liste sous le format défini par la fonction load_mesh représentant l'objet après translation

    ##########################'''

    new_mesh = []

    vecteur = [translation_selon_x,translation_selon_y,translation_selon_z]

    for i in range(len(mesh)) :

        point_1 = operation_vecteur(mesh[i][1][0],vecteur,"+")
        point_2 = operation_vecteur(mesh[i][1][1],vecteur,"+")
        point_3 = operation_vecteur(mesh[i][1][2],vecteur,"+")

        new_mesh.append([mesh[i][0],[point_1,point_2,point_3]])

    return new_mesh    



    
