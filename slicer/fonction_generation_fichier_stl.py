# coding:latin-1

from slicer.fonction_vertices_face import *

from slicer.fonction_generation_cordons import polygone_regulier,polygone_ellipse,polygone_clavette

from slicer.fonction_matrice import inverse_matrice,mise_en_base,prod_matriciel

from slicer.fonction_vecteur import operation_vecteur,norme_vecteur

from math import ceil

def Create_fichier_stl(nom_fichier,mesh) :
    '''
    # cette fonction crée un fichier stl à partir d'un mesh

    ##########################

    ##########
    # entrée #
    ##########

    # nom_fichier (type str) : nom du fichier (pas besoin de mettre l'extension)

    # mesh (type list) : liste sous le format défini par la fonction load_mesh

    ##########
    # sortie #
    ##########

    # None

    ##########################'''

    with open(str(nom_fichier)+".stl","w") as fich :
        fich.write("solid OpenSCAD_Model"+2*"\n")
        
        for i in range(len(mesh)) :
            fich.write("  facet normal "+str(mesh[i][0][0])+" "+str(mesh[i][0][1])+" "+str(mesh[i][0][2])+2*"\n")
            fich.write("    outer loop"+2*"\n")
            fich.write("      vertex "+str(mesh[i][1][0][0])+" "+str(mesh[i][1][0][1])+" "+str(mesh[i][1][0][2])+2*"\n")
            fich.write("      vertex "+str(mesh[i][1][1][0])+" "+str(mesh[i][1][1][1])+" "+str(mesh[i][1][1][2])+2*"\n")
            fich.write("      vertex "+str(mesh[i][1][2][0])+" "+str(mesh[i][1][2][1])+" "+str(mesh[i][1][2][2])+2*"\n")
            fich.write("    endloop"+2*"\n")
            fich.write("  endfacet"+2*"\n")

        fich.write("endsolid OpenSCAD_Model")

    return None

def Create_fichier_stl(nom_fichier,mesh) :
    '''
    # cette fonction crée un fichier stl à partir d'un mesh

    ##########################

    ##########
    # entrée #
    ##########

    # nom_fichier (type str) : nom du fichier (pas besoin de mettre l'extension)

    # mesh (type list) : liste sous le format défini par la fonction load_mesh

    ##########
    # sortie #
    ##########

    # None

    ##########################'''

    with open(str(nom_fichier)+".stl","w") as fich :
        fich.write("solid OpenSCAD_Model"+2*"\n")
        
        for i in range(len(mesh)) :
            fich.write("  facet normal "+str(mesh[i][0][0])+" "+str(mesh[i][0][1])+" "+str(mesh[i][0][2])+2*"\n")
            fich.write("    outer loop"+2*"\n")
            fich.write("      vertex "+str(mesh[i][1][0][0])+" "+str(mesh[i][1][0][1])+" "+str(mesh[i][1][0][2])+2*"\n")
            fich.write("      vertex "+str(mesh[i][1][1][0])+" "+str(mesh[i][1][1][1])+" "+str(mesh[i][1][1][2])+2*"\n")
            fich.write("      vertex "+str(mesh[i][1][2][0])+" "+str(mesh[i][1][2][1])+" "+str(mesh[i][1][2][2])+2*"\n")
            fich.write("    endloop"+2*"\n")
            fich.write("  endfacet"+2*"\n")

        fich.write("endsolid OpenSCAD_Model")

    return None

def str_to_float_2(caractere) :

    caractere_str = str(caractere)
    indice = caractere_str.index(".")
    caractere_float = caractere_str[0:indice]+","+caracter_str[indice+1:]

    return caractere_float

def Create_fichier_catia(nom_fichier,coord_cordon,rayon_cordon,type_cordon,N_facette_cordon,axe) :
    '''
    # cette fonction crée un fichier excel à partir des coordonnées des cordons, qui peut être lu par le logiciel Catia

    ##########################

    ##########
    # entrée #
    ##########

    # nom_fichier (type str) : nom du fichier (pas besoin de mettre l'extension)

    # coord_cordon (type list) : liste des coordonnées des cordons

    # rayon_cordon (type int ou float) : rayon des cordons

    # type_cordon (type str) : "cylindrique", "ellipse" ou "clavette"

    # N_facette_cordon : nombre de facettes composant la base des cordons

    # axe (type str) : axe de découpe 

    ##########
    # sortie #
    ##########

    # None

    ##########################'''

    try :
        import xlrd
        from xlwt import Workbook
    except :
        return None
    
    classeur = Workbook()
    feuille = classeur.add_sheet("OCB")

    if axe == "x" :

        unitaire = [1,0,0]

    if axe == "y" :

        unitaire = [0,1,0]

    if axe == "z" :

        unitaire = [0,0,1]
        
    ligne = 0

    for i in range(len(coord_cordon)) :

        for m in range(2) :
        
            for j in range(len(coord_cordon[i][m])) :

                vecteur_directeur = operation_vecteur(coord_cordon[i][m][j][1],coord_cordon[i][m][j][0],"-")
                hauteur = norme_vecteur(vecteur_directeur)

                if hauteur != 0 :
                
                    unitaire_2 = operation_vecteur(unitaire,vecteur_directeur,"vec")

                    matrice_base = inverse_matrice(mise_en_base(unitaire,vecteur_directeur,unitaire_2))

                    centre_1_new_base = operation_vecteur(prod_matriciel(matrice_base,coord_cordon[i][m][j][0]),[0,rayon_cordon,0],"-")
                    centre_1 = prod_matriciel(inverse_matrice(matrice_base),centre_1_new_base)
                    centre_2_new_base = operation_vecteur(prod_matriciel(matrice_base,coord_cordon[i][m][j][1]),[0,rayon_cordon,0],"+")
                    centre_2 = prod_matriciel(inverse_matrice(matrice_base),centre_2_new_base)

                    if type_cordon == "cylindrique" :

                        coord_courbe_1,coord_courbe_2,ext = polygone_regulier(coord_cordon[i][m][j][0],N_facette_cordon,rayon_cordon,hauteur,matrice_base,False)

                    if type_cordon == "ellipse" :

                        coord_courbe_1,coord_courbe_2,ext = polygone_ellipse(coord_cordon[i][m][j][0],N_facette_cordon,rayon_cordon,hauteur,matrice_base,False)

                    if type_cordon == "clavette" :

                        coord_courbe_1,coord_courbe_2,ext = polygone_clavette(coord_cordon[i][m][j][0],N_facette_cordon,rayon_cordon,hauteur,matrice_base,False)

                    feuille.write(ligne,0,"StartLoft")
                    ligne += 1
                    feuille.write(ligne,0,"StartCurve")
                    ligne += 1
                    
                    for point in coord_courbe_1 :

                            feuille.write(ligne,0,float(point[0]))
                            feuille.write(ligne,1,float(point[1]))
                            feuille.write(ligne,2,float(point[2]))
                            ligne += 1

                    feuille.write(ligne,0,"EndCurve")
                    ligne += 1
                    feuille.write(ligne,0,"StartCurve")
                    ligne += 1

                    for point in coord_courbe_2 :

                            feuille.write(ligne,0,float(point[0]))
                            feuille.write(ligne,1,float(point[1]))
                            feuille.write(ligne,2,float(point[2]))
                            ligne += 1

                    feuille.write(ligne,0,"EndCurve")
                    ligne += 1
                    feuille.write(ligne,0,"EndLoft")
                    ligne += 1
                    feuille.write(ligne,0,"StartLoft")
                    ligne += 1
                    feuille.write(ligne,0,"StartCurve")
                    ligne += 1

                    k = 0

                    for k in range(len(coord_courbe_1)):

                        feuille.write(ligne,0,float(coord_courbe_1[k][0]))
                        feuille.write(ligne,1,float(coord_courbe_1[k][1]))
                        feuille.write(ligne,2,float(coord_courbe_1[k][2]))
                        ligne += 1

                        if k == ceil(float(len(coord_courbe_1))/2) :

                            feuille.write(ligne,0,"EndCurve")
                            ligne += 1
                            feuille.write(ligne,0,"StartCurve")
                            ligne += 1
                            feuille.write(ligne,0,float(coord_courbe_1[0][0]))
                            feuille.write(ligne,1,float(coord_courbe_1[0][1]))
                            feuille.write(ligne,2,float(coord_courbe_1[0][2]))
                            ligne += 1
                            feuille.write(ligne,0,float(centre_1[0]))
                            feuille.write(ligne,1,float(centre_1[1]))
                            feuille.write(ligne,2,float(centre_1[2]))
                            ligne += 1
                            feuille.write(ligne,0,float(coord_courbe_1[k][0]))
                            feuille.write(ligne,1,float(coord_courbe_1[k][1]))
                            feuille.write(ligne,2,float(coord_courbe_1[k][2]))
                            ligne += 1
                            feuille.write(ligne,0,"EndCurve")
                            ligne += 1
                            feuille.write(ligne,0,"StartCurve")
                            ligne += 1

                    feuille.write(ligne,0,"EndCurve")
                    ligne += 1
                    feuille.write(ligne,0,"EndLoft")
                    ligne += 1
                    feuille.write(ligne,0,"StartLoft")
                    ligne += 1
                    feuille.write(ligne,0,"StartCurve")
                    ligne += 1

                    k = 0

                    for k in range(len(coord_courbe_2)):

                        feuille.write(ligne,0,float(coord_courbe_2[k][0]))
                        feuille.write(ligne,1,float(coord_courbe_2[k][1]))
                        feuille.write(ligne,2,float(coord_courbe_2[k][2]))
                        ligne += 1

                        if k == ceil(float(len(coord_courbe_2))/2) :

                            feuille.write(ligne,0,"EndCurve")
                            ligne += 1
                            feuille.write(ligne,0,"StartCurve")
                            ligne += 1
                            feuille.write(ligne,0,float(coord_courbe_2[0][0]))
                            feuille.write(ligne,1,float(coord_courbe_2[0][1]))
                            feuille.write(ligne,2,float(coord_courbe_2[0][2]))
                            ligne += 1
                            feuille.write(ligne,0,float(centre_2[0]))
                            feuille.write(ligne,1,float(centre_2[1]))
                            feuille.write(ligne,2,float(centre_2[2]))
                            ligne += 1
                            feuille.write(ligne,0,float(coord_courbe_2[k][0]))
                            feuille.write(ligne,1,float(coord_courbe_2[k][1]))
                            feuille.write(ligne,2,float(coord_courbe_2[k][2]))
                            ligne += 1
                            feuille.write(ligne,0,"EndCurve")
                            ligne += 1
                            feuille.write(ligne,0,"StartCurve")
                            ligne += 1

                    feuille.write(ligne,0,"EndCurve")
                    ligne += 1
                    feuille.write(ligne,0,"EndLoft")
                    ligne += 1
                    
    feuille.write(ligne,0,"End")
    classeur.save(nom_fichier+".xls")

    return None

def lecture(nom_fichier) :
    '''
    # cette fonction lit un fichier

    ##########################

    ##########
    # entrée #
    ##########

    # nom_fichier (type str) : nom du fichier (il faut mettre l'extension)

    ##########
    # sortie #
    ##########

    # None

    ##########################'''
    
    with open(str(nom_fichier),"r") as fich :
        line = fich.readline()
        print(line)

        while line :

            line = fich.readline()
            print(line)

    return None

def Create_fichier_csv(nom_du_fichier,coord_cordon) :
    '''
    # cette fonction crée un fichier au format .csv récapitulant les coordonnées de chacun des cordons

    ##########################

    ##########
    # entrée #
    ##########

    # nom_du_fichier (type str) : nom du fichier (il ne faut pas mettre l'extension)

    # coord_cordon (type list) : liste des coordonnées des cordons

    ##########
    # sortie #
    ##########

    # None

    ##########################'''

    with open(nom_du_fichier+".csv","w") as fich :

        fich.write("point de départ"+";"+"point d'arrivée"+"\n")

        for i in range(len(coord_cordon)) :

            for k in range(2) :

                for j in range(len(coord_cordon[i][k])) :

                    fich.write(str(coord_cordon[i][k][j][0])+";"+str(coord_cordon[i][k][j][1])+"\n")

        fich.write("End")

    return None

def Create_fichier_python(nom_fichier) :

    '''
    # cette fonction crée une copie d'un fichier python sans accentuation et sans c cédille

    ##########################

    ##########
    # entrée #
    ##########

    # nom_du_fichier (type str) : nom du fichier (il faut mettre l'extension)

    ##########
    # sortie #
    ##########

    # None

    ##########################'''

    ligne = []

    with open(nom_fichier,"r") as fich :

        line = fich.readline()
        ligne.append(line)
        while line :
            line = fich.readline()
            ligne.append(line)

    for i in range(len(ligne)) :

        for j in range(len(ligne[i])) :

            caractere = ""

            if ligne[i][j] == "é" or ligne[i][j] == "è" or ligne[i][j] == "ê" or ligne[i][j] == "ë":

                caractere = "e"

            if ligne[i][j] == "ù" or ligne[i][j] == "û" or  ligne[i][j] == "ü" :

                caractere = "u"

            if ligne[i][j] == "à" or ligne[i][j] == "â" or  ligne[i][j] == "ä" :

                caractere = "a"

            if ligne[i][j] == "ô" or ligne[i][j] == "ö" :

                caractere = "o"

            if ligne[i][j] == "î" or ligne[i][j] == "ï" :

                caractere = "i"

            if ligne[i][j] == "ç" :

                caractere = "c"

            if caractere != "" :

                ligne[i] = ligne[i][:j]+caractere+ligne[i][j+1:]

    with open("aaaiuvheivuheivh.py","w") as fich :

        for i in range(len(ligne)) :

            fich.write(ligne[i])

def if_commentaire(line) :

    '''
    # cette fonction teste si on lit une ligne commentaire ou non

    ##########################

    ##########
    # entrée #
    ##########

    # line (type str) : correspond à la ligne d'un fichier

    ##########
    # sortie #
    ##########

    # boléen

    ##########################'''

    for i in range(len(line)) :

        if line[i] != " " :

            if line[i] == "#" :

                return True

            return False

def if_saut(line) :

    '''
    # cette fonction teste si on lit un saut de ligne ou non

    ##########################

    ##########
    # entrée #
    ##########

    # line (type str) : correspond à la ligne d'un fichier

    ##########
    # sortie #
    ##########

    # boléen

    ##########################'''

    line_2 = line

    line_3 = line_2.split("\n")

    for i in range(len(line_3[0])) :

        if line_3[0][i] != " " and line_3[0][i] != "" :

            return False

    return True

def compte_ligne_fonction(nom_fichier,nom_fonction) :

    '''
    # cette fonction compte le nombre de ligne de code d'une fonction pour un fichier donné

    ##########################

    ##########
    # entrée #
    ##########

    # nom_fichier (type str) : nom du fichier (il faut mettre l'extension)

    # nom_fonction (type str) : nom de la fonction
    
    ##########
    # sortie #
    ##########

    # nombre_de_lignes_de_code (type int) : nombre de lignes de code de la fonction (hors commentaire et saut de ligne)

    ##########################'''

    ligne_depart ="def "+nom_fonction
    indice = len(ligne_depart)
    nombre_de_lignes_de_code = 0
    stop = False
    deja = 0

    with open(nom_fichier,"r") as fich :

        ligne = str(fich.readline())

        while ligne :

            if ligne[:indice] == ligne_depart :

                nombre_de_lignes_de_code += 1
                deja = 1

            if deja == 1 and not if_commentaire(ligne) and not if_saut(ligne) :

                nombre_de_lignes_de_code += 1

            if  ligne[:7] == "return " and deja == 1 :

                nombre_de_lignes_de_code -= 1

                deja = 2

            ligne = str(fich.readline())

    return nombre_de_lignes_de_code

        

                    
            


            

            

                
                





    
        
        
