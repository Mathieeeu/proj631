from prediction import *

if __name__ == "__main__":

    # VARIABLES A MODIFIER
    filename = "data/golf.csv"          # données discrètes
    # filename = "data/golf_bis.csv"    # données continues
    attribut_classe = 'play'

    # Creation et affichage de l'arbre de décision à partir des données d'entrainement (10 premières instances)
    data,donnees_possibles = read_data(filename)
    data_training = data[:10]
    arbre=construire_arbre(data_training,donnees_possibles,attribut_classe,method="ID3")
    afficher_arbre(arbre,debug=True)

    # Creation et affichage de la matrice de confusion à partir des données de test (Dernières instances)
    data_test = data[10:]
    matrice = matrice_confusion(data_test,donnees_possibles,arbre,attribut_classe)
    print(matrice)