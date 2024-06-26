from Matrice import CMatrice
from decision_tree import read_data,construire_arbre,afficher_arbre

def verifier_instance(instance,arbre,attribut_classe='class'):
    res = False
    for cle in instance.keys():
        if cle in arbre:
            if instance[cle] in arbre[cle]:
                if len(arbre[cle][instance[cle]].keys()) == 1 and list(arbre[cle][instance[cle]].keys())[0] == attribut_classe:
                    if arbre[cle][instance[cle]][attribut_classe] == instance[attribut_classe]:
                        res = True
                    return res
                else:
                    res = verifier_instance(instance,arbre[cle][instance[cle]],attribut_classe)
                    return res
    return res

def matrice_confusion(data,donnees_possibles,arbre,attribut_classe='class'):
    """
    construit la matrice de confusion pour un arbre de décision
    """
    n = len(donnees_possibles[attribut_classe])
    valeurs_classe = list(donnees_possibles[attribut_classe])
    matrice = CMatrice(n,valeurs_classe,valeurs_classe)

    for i in range(n):
        for j in range(n):
            for instance in data:
                if instance[attribut_classe] == valeurs_classe[i]:
                    if verifier_instance(instance,arbre,attribut_classe) and i==j:
                        matrice[i][j] += 1
                    elif not verifier_instance(instance,arbre,attribut_classe) and i!=j:
                        matrice[j][i] += 1
    return matrice

def predire_valeurs_manquantes(data,donnees_possibles,arbre,attribut_classe='class'):
    """
    prédit les valeurs manquantes dans un jeu de données (c'est les valeurs avec des '?')
    """
    # ne touche qu'aux lignes avec des '?'
    return data

# TESTS -----------------------------------------------------------------------
    # filename = "data/golf_copy.csv"
    # attribut_classe = 'play'
    # data,donnees_possibles = read_data(filename)
    # print(data)
    # arbre2 = construire_arbre(data,donnees_possibles,attribut_classe,method="ID3")
    # afficher_arbre(arbre2,debug=True)
    # data_corrigee = predire_valeurs_manquantes(data,donnees_possibles,arbre2,attribut_classe)

    # # enregistre les données corrigées dans un fichier csv
    # with open(f"{filename[:-4]}_corrigee.csv","w") as f:
    #     f.write(','.join(data_corrigee[0].keys())+'\n')
    #     for instance in data_corrigee:
    #         f.write(','.join([str(v) for v in instance.values()])+'\n')
