# coding:latin-1

from slicer.fonction_vecteur import comparaison_vecteur

def indice_min(L,debut,fin,n,critere):
    '''
    # cette fonction compare une sous-liste aux autres et la met à la bonne place selon le tri demandé

    ##########################

    ##########
    # entrée #
    ##########

    # L (type list) : liste à trier

    # debut (type int) : indice de la première sous-liste à regarder

    # fin (type int) : indice de la dernière sous-liste à regarder

    # n (type int) : indice de l'item selon lequel on effectue le tri

    # critere (type str) : si le tri est croissant alors critere est "+" sinon critere est "-"

    ##########
    # sortie #
    ##########

    # imin (type int) : indice de la nouvelle place de la sous-liste 

    ##########################'''
    
    imin = debut
    
    for p in range(debut,fin+1) :                                            # On parcourt la liste pour l'index 'debut' à 'fin'
        
        if critere == "+" :                                                  # Si le critere est "+" , le tri s'effectue dans le sens croissant
            if L[p][n] < L[imin][n] :                                          # Si la valeur rencontrée est inférieure à la valeur min alors elle devient imin
                imin = p
        else :
            if L[p][n] > L[imin][n] :                                          # Si la valeur rencontrée est supérieure à la valeur min alors elle devient imin car on tri dans le sens décroisant
                imin = p
    return imin

def echange(L,i,j):
    '''
    # cette fonction échange le ième et le jème item d'une liste

    ##########################

    ##########
    # entrée #
    ##########

    # L (type list) : liste

    # i (type int) : indice du ième item de la liste

    # j (type int) : indice du jème item de la liste

    ##########
    # sortie #
    ##########

    # None

    ##########################'''
    
    L[i],L[j] = L[j],L[i]
    
    return None

def tri_selection(L,n,critere):
    '''
    # cette fonction trie une liste selon la méthode sélection

    ##########################

    ##########
    # entrée #
    ##########

    # L (type list) : liste à trier

    # critere (type str) : si le tri est croissant alors critere est "+" sinon critere est "-"

    # n (type int) : correspond à l'indice selon lequel le tri s'effectue

    ##########
    # sortie #
    ##########

    # L (type list) : liste triée

    ##########################'''
    
    for i in range(0,len(L)) :                                              # On parcourt la liste
        
        j = indice_min(L,i,len(L)-1,n,critere)                                # On cherche l'indice min dans le cas ou critere = "+" et l'indice max dans le cas ou critere = "-"
        echange(L,i,j)                                                      # On échange le ième élément avec le jème élément
        
    return L

def tri(listedonnees,critere,n):
    '''
    # cette fonction trie une liste de listes selon un critère et l'indice des sous-listes pour lequel on trie

    ##########################

    ##########
    # entrée #
    ##########

    # listedonnees (type list) : liste de listes

    # critere (type str) : si le tri est croissant alors critere est "+" sinon critere est "-"

    # n (type int) : correspond à l'indice selon lequel le tri s'effectue

    ##########
    # sortie #
    ##########

    # listedonnees (type list) : correspond à la liste triée

    ##########################'''
    
    try :                                                                    #Petite sécurité si on est hors de la liste (au niveau du n)
        listedonnees[0][n]
    except IndexError :
        return listedonnees
    
    if tri_selection(listedonnees,n,critere) == -1 :                         #Sécurité par rapport au critere
        return listedonnees
    
    if type(listedonnees[0][n]) == str :                                     #Si les listes à trier sont des lettres alors :
        for i in range(len(listedonnees)):
            listedonnees[i][n] = listedonnees[i][n].capitalize()               #On met en majuscules les sous-sous-listes composées de lettres
            
    tri_selection(listedonnees,n,critere)                                    #On trie la liste                                
    return listedonnees


#####################################################
#####################################################
#####################################################

# cette fonction ne marche pas pour toutes les géométries

def tri_layer(layer,precision) :

    layer_trie = [layer[0]]

    for j in range(len(layer)) :
        for i in range(len(layer)) :

            check = True

            for k in range(len(layer_trie)) :

                if comparaison_vecteur(layer_trie[k][0],layer[i][0],precision) and comparaison_vecteur(layer_trie[k][1],layer[i][1],precision) :

                    check = False
                    
            if check :

                deja_pris_en_compte = 0

                if comparaison_vecteur(layer[i][0],layer_trie[-1][0],precision) and not comparaison_vecteur(layer[i][1],layer_trie[-1][1],precision):

                    layer_trie.append(layer[i])
                    deja_pris_en_compte = 1

                if comparaison_vecteur(layer[i][0],layer_trie[-1][1],precision) and not comparaison_vecteur(layer[i][1],layer_trie[-1][0],precision) and deja_pris_en_compte == 0 :

                    layer_trie.append(layer[i])
                    deja_pris_en_compte = 1

                if comparaison_vecteur(layer[i][1],layer_trie[-1][1],precision) and not comparaison_vecteur(layer[i][0],layer_trie[-1][0],precision) and deja_pris_en_compte == 0 :

                    layer_trie.append(layer[i])
                    deja_pris_en_compte = 1

                if comparaison_vecteur(layer[i][1],layer_trie[-1][0],precision) and not comparaison_vecteur(layer[i][0],layer_trie[-1][1],precision) and deja_pris_en_compte == 0 :

                    layer_trie.append(layer[i])
                    deja_pris_en_compte = 1

    if len(layer_trie) != len(layer) :

        return layer

    return layer_trie




        
                               
