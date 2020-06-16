# coding:latin-1

from slicer.fonction_vecteur import *
import copy

def mise_en_base(vecteur_1,vecteur_2,vecteur_3) :
    '''
    # cette fonction permet de construire la matrice dont les colonnes
    # sont les coordonn�es des trois vecteurs donn�s en entr�e

    ##########################

    ##########
    # entr�e #
    ##########

    # vecteur_1 (type list) : liste des coordonn�es du vecteur sous le format [x,y,z]

    # vecteur_2 (type list) : liste des coordonn�es du vecteur sous le format [x,y,z]

    # vecteur_3 (type list) : liste des coordonn�es du vecteur sous le format [x,y,z]

    # le vecteur nul ne peut pas �tre donn� en entr�e

    ##########
    # sortie #
    ##########

    # liste_base (type list) : correspond � la matrice 3X3 dont le premier item est la liste des coordonn�es x, le second la liste des coordonn�es y et le troisi�me la liste des coordonn�es z

    ##########################'''

    liste_base = []
    vecteur_1_u = operation_vecteur(vecteur_1,norme_vecteur(vecteur_1),"/")
    vecteur_2_u = operation_vecteur(vecteur_2,norme_vecteur(vecteur_2),"/")
    vecteur_3_u = operation_vecteur(vecteur_3,norme_vecteur(vecteur_3),"/")

    for i in range(len(vecteur_1_u)) :

        liste = [vecteur_1_u[i],vecteur_2_u[i],vecteur_3_u[i]]
        liste_base.append(liste)

    return liste_base

def prod_matriciel(matrice,vecteur) :
    '''
    # cette fonction effectue un produit matriciel entre une matrice carr�e NXN et un vecteur assimil� � une matrice colonne compos�e de N lignes

    ##########################

    ##########
    # entr�e #
    ##########

    # matrice (type liste) : liste compos�e de N listes � N items dont chaque item est un float ou un int

    # vecteur (type list) : liste des coordonn�es du vecteur sous le format [x,y,z]

    ##########
    # sortie #
    ##########

    # coordonnee (type liste) : r�sultat du produit matriciel sous le format d'une liste � N items, dont chaque item est un float ou un int

    ##########################'''

    coordonnee = [0,0,0]

    for i in range(len(vecteur)) :
        
        for j in range(len(vecteur)) :

            coordonnee[i] += matrice[i][j]*vecteur[j]

    return coordonnee

def inverse_matrice(matrice) :
    '''
    # cette fonction calcule l'inverse d'une matrice orthogonale en faisant la transpos�e de la matrice

    ##########################

    ##########
    # entr�e #
    ##########

    # matrice (type liste) : liste compos�e de N listes � N items dont chaque item est un float ou un int

    # la matrice doit �tre orthogonale pour renvoyer l'inverse, sinon cela renvoie sa matrice transpos�e

    ##########
    # sortie #
    ##########

    # inverse (type liste) : liste compos�e de N listes � N items dont chaque item est un float ou un int, repr�sentant l'inverse de la matrice othogonale (sa transpos�e)

    # inverse est aussi une matrice orthogonale

    ##########################'''

    inverse = copy.deepcopy(matrice)

    for i in range(len(inverse)) :

        for j in range(len(inverse[i])) :

            inverse[i][j] = matrice[j][i]

    return inverse

def determinant(matrice):
    '''
    # cette fonction calcule le d�terminant d'une matrice carr�e 3X3

    ##########################

    ##########
    # entr�e #
    ##########

    # matrice (type liste) : liste compos�e de 3 listes � 3 items dont chaque item est un float ou un int

    ##########
    # sortie #
    ##########

    # det (type float ou int) : d�terminant de la matrice

    ##########################'''
    
    det00 = matrice[1][1]*matrice[2][2]-matrice[1][2]*matrice[2][1]
    det01 = matrice[1][0]*matrice[2][2]-matrice[1][2]*matrice[2][0]
    det02 = matrice[1][0]*matrice[2][1]-matrice[1][1]*matrice[2][0]

    det = det00-det01+det02
    
    return det

    
    
