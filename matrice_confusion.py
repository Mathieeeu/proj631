from Matrice import CMatrice
from decision_tree import read_data,construire_arbre,afficher_arbre

def compte_occurences(arbre,attribut_classe='class',occurences={}):
    """
    compte le nombre d'occurences de chaque classe dans l'arbre de décision
    """
    for cle,valeur in arbre.items():
        if type(valeur) is dict:
            compte_occurences(valeur,attribut_classe,occurences)
        else:
            if valeur not in occurences:
                occurences[valeur] = 0
            occurences[valeur] += 1
    return occurences

def matrice_confusion(data,donnees_possibles,arbre,attribut_classe='class'):
    """
    construit la matrice de confusion pour un arbre de décision
    """
    n = len(donnees_possibles[attribut_classe])
    valeurs_classe = list(donnees_possibles[attribut_classe])
    matrice = CMatrice(n,valeurs_classe,valeurs_classe)

    occurences = compte_occurences(arbre,attribut_classe)
    for i in range(n):
        matrice[i][i] = occurences[valeurs_classe[i]]


    return matrice

filename = "data/golf.csv"
attribut_classe = 'play'
data,donnees_possibles = read_data(filename)
arbre=construire_arbre(data,donnees_possibles,attribut_classe)
afficher_arbre(arbre,debug=True)

matrice = matrice_confusion(data,donnees_possibles,arbre,attribut_classe)
print(matrice)