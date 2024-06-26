import csv
import math 
import json

global debug
debug = False

def construire_arbre(data,donnees_possibles,attribut_classe='class',racine={},method="ID3"):
    # on ne prend pas en compte les lignes ayant des données manquantes
    data = [instance for instance in data if '?' not in instance.values()]
    # on supprime les ? des données possibles
    for attribut in donnees_possibles:
        donnees_possibles[attribut].discard('?')
    if method == "ID3":
        gains = calcul_gains(data,donnees_possibles,attribut_classe)
        meilleur_attribut = max(gains, key=gains.get, default=None)
    elif method == "C45":
        gains = ratio_gain(data,donnees_possibles,attribut_classe)
        meilleur_attribut = max(gains, key=gains.get, default=None)
    print(f"meilleur attribut : {meilleur_attribut}") if debug else None

    if gains[meilleur_attribut] == 0:
        # si le gain est nul, on a atteint une feuille, on renvoie la valeur de la classe majoritaire
        print(f"\033[32m\033[1m\033[31mLe gain est nul\033[0m") if debug else None
        print('\n' if debug else '',end='')
        print(data if debug else '',end='')
        print(data[0][attribut_classe] if debug else '',end='')
        racine = {attribut_classe:max(data, key=data.count)[attribut_classe]}
        return racine
    
    racine = {meilleur_attribut:{}}

    for valeur in donnees_possibles[meilleur_attribut]:
        racine[meilleur_attribut][valeur] = {}

    print(f"\033[32m\033[1marbre créé avec la racine {meilleur_attribut}\033[0m") if debug else None
    afficher_arbre(racine)
    print('\n\n' if debug else '',end='')

    print(donnees_possibles[meilleur_attribut] if debug else '',end='')

    for valeur in donnees_possibles[meilleur_attribut]:
        print(f"\033[32mtraitement de la valeur \033[1m{valeur}\033[0m\033[32m de l'attribut {meilleur_attribut}\033[0m") if debug else None
        sous_ensemble = [instance for instance in data if instance[meilleur_attribut] == valeur]
        print(f"\033[35msous-ensemble : {sous_ensemble}\033[0m") if debug else None
        print(f"\033[34mdonnées possibles : {donnees_possibles}\033[0m") if debug else None
        print('\n' if debug else '',end='')

        if len(sous_ensemble)==0:
            print(f"\033[32m\033[1m\033[31mLe sous-ensemble est vide\033[0m") if debug else None
            print('\n' if debug else '',end='')
            racine[meilleur_attribut][valeur] = {attribut_classe:'null'}
        elif len(sous_ensemble)==1:
            print(f"\033[32m\033[1m\033[31mLe sous-ensemble ne contient qu'une seule instance\033[0m") if debug else None
            print('\n' if debug else '',end='')
            racine[meilleur_attribut][valeur] = {attribut_classe:sous_ensemble[0][attribut_classe]}
        elif len(donnees_possibles)==1:
            print(f"\033[32m\033[1m\033[31mIl n'y a plus d'attribut à traiter\033[0m") if debug else None
            print('\n' if debug else '',end='')
            racine[meilleur_attribut][valeur] = {attribut_classe:max(sous_ensemble, key=sous_ensemble.count)[attribut_classe]}
        else:
            print(f"\033[32m\033[1m\033[31mIl y a encore des attributs à traiter\033[0m") if debug else None
            # créer un sous-ensemble de données sans l'attribut déjà traité
            sous_ensemble_plus_petit = []
            donnees_possibles_plus_petit = donnees_possibles.copy()
            for instance in sous_ensemble:
                instance_plus_petit = instance.copy()
                instance_plus_petit.pop(meilleur_attribut)
                sous_ensemble_plus_petit.append(instance_plus_petit)
            for instance in donnees_possibles:
                if instance == meilleur_attribut:
                    donnees_possibles_plus_petit.pop(instance)
            print(f"\033[35msous-ensemble plus petit : {sous_ensemble_plus_petit}\033[0m") if debug else None
            print(f"\033[34mdonnées possibles plus petites : {donnees_possibles_plus_petit}\033[0m") if debug else None
            print(f"\033[33m{racine}\033[0m") if debug else None
            racine[meilleur_attribut][valeur] = construire_arbre(sous_ensemble_plus_petit,donnees_possibles_plus_petit,attribut_classe,method)
    afficher_arbre(racine)
    return racine

def afficher_arbre(racine,indent=0,debug=False,i=0):
    style_reset="\033[0m"
    # couleurs sur https://i.stack.imgur.com/KTSQa.png parce que c'est stylé ;)
    style_titre = "\033[35m\033[1m"
    style_attribut="\033[38;5;28m"
    style_valeur="\033[38;5;37m"
    style_classe="\033[31m"

    if indent == 0:
        print(f"\n{style_titre}Arbre construit :{style_reset}") if debug else None
        print(f"{style_attribut}",end='') if debug else None
    for cle,valeur in racine.items():
        if i%2==1:
            print(f"{'| '*indent}{style_valeur}{cle}{style_reset}{style_attribut}") if debug else None
        else:
            print(f"{'| '*indent}{cle}") if debug else None
        if type(valeur) is dict:
            afficher_arbre(valeur,indent+1,debug,i+1)
        else:
            print(f"{'| '*(indent+1)}{style_classe}{valeur}{style_reset}{style_attribut}") if debug else None
    if indent == 0:
        print(f"{style_reset}") if debug else None
        with open(f'tree.json', 'w') as f:
            json.dump(racine, f, indent=4)

def read_data(filename):
    """
    lecture des données d'apprentissage à partir d'un fichier csv
    format : 
        - première ligne : nom des attributs
        - chaque ligne suivante : une instance
    renvoie une liste de dictionnaires où chaque dictionnaire représente une instance avec les attributs comme clés et un dictionnaire des valeurs possibles pour chaque attribut
    """
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        data = [dict(row) for row in reader]

    donnees_possibles = {}
    for instance in data:
        for attribut,valeur in instance.items():
            if attribut not in donnees_possibles:
                donnees_possibles[attribut] = set()
            donnees_possibles[attribut].add(valeur)
    
    #discrétisation des valeurs quand elles sont continues
    attributs_discretisables = liste_discretisable(donnees_possibles)
    for attribut in attributs_discretisables:
        print("AAAA")
        data,donnees_possibles=discretiser(data,donnees_possibles,attribut,attributs_discretisables[attribut])

    return data,donnees_possibles

def I(p,n):
    if p == 0 or n == 0:
        return 0
    return -p/(p+n)*math.log2(p/(p+n)) -n/(p+n)*math.log2(n/(p+n))

def E(data,donnees_possibles,attribut,attribut_classe='class'):
    """
    calcul de l'entropie pour un attribut donné
    """
    valeurs_classe = list(donnees_possibles[attribut_classe])
    entropie = 0
    for valeur in donnees_possibles[attribut]:
        p = 0
        n = 0
        for instance in data:
            if instance[attribut] == valeur:
                if instance[attribut_classe] == valeurs_classe[0]:
                    p += 1
                else:
                    n += 1
        entropie += (p + n) / (len(data)) * I(p, n)
    return entropie

def split_entropie(data,donnees_possibles,attribut,attribut_classe='class'):
    """
    calcul le split d'entropie pour un attribut donné (C4.5) 
    split = - sum(v€S) (|Sv|/|S|) * log2(|Sv|/|S|)
    """
    split = 0
    for valeur in donnees_possibles[attribut]:
        sous_ensemble = [instance for instance in data if instance[attribut] == valeur]
        if len(sous_ensemble) != 0:
            split -= len(sous_ensemble) / len(data) * math.log2(len(sous_ensemble) / len(data))
    return split

def ratio_gain(data,donnees_possibles,attribut_classe='class'):
    """
    calcul des ratios de gain C4.5 de l'ensemble pour chaque attribut
    """
    ratios = {}
    for attribut in donnees_possibles:
        if attribut != attribut_classe:
            split = split_entropie(data,donnees_possibles,attribut,attribut_classe)
            gain = calcul_gains(data,donnees_possibles,attribut_classe)[attribut]
            ratios[attribut] = gain / split if split != 0 else float('inf')
    return ratios

def calcul_gains(data,donnees_possibles,attribut_classe='class'):
    """
    calcul du gain d'information pour un attribut avec les formules de la doc
    """
    gains={}
    print(donnees_possibles if debug else '',end='')
    for attribut in donnees_possibles:
        if attribut != attribut_classe:
            p = 0
            n = 0
            valeurs_classe = list(donnees_possibles[attribut_classe])
            for instance in data:
                if instance[attribut_classe] == valeurs_classe[0]:
                    p += 1
                else:
                    n += 1
            gain = I(p,n) - E(data,donnees_possibles,attribut,attribut_classe)
            print(f"gain({attribut})\t= {(round(gain,10))}") if debug else None
            gains[attribut] = gain
    return gains

def est_discretisable(donnees_possibles,attribut):
    """
    vérifie si un attribut peut être discrétisé
    """
    for valeur in donnees_possibles[attribut]:
        try:
            float(valeur)
        except ValueError:
            return False
    return True

def liste_discretisable(donnees_possibles):
    res = {}
    for attribut in donnees_possibles:
        if est_discretisable(donnees_possibles,attribut):
            res[attribut] = donnees_possibles[attribut]
    return res

def discretiser(data,donnees_possibles,attribut,valeurs_possibles):
    """
    On crée deux intervalles qui séparent les valeurs possibles de l'attribut en deux à la médiane
    """
    data_discretise = []
    donnees_possibles_discretise = donnees_possibles.copy()

    liste_intervalles = []
    valeurs_triees = sorted([float(valeur) for valeur in valeurs_possibles])
    print(f"valeurs triées pour {attribut}: {valeurs_triees}") if debug else None
    indice_median = len(valeurs_triees)//2

    borne_inf = float("-inf")
    borne_sup = float("inf")

    intervalle_inf = [borne_inf,valeurs_triees[indice_median]]
    intervalle_sup = [valeurs_triees[indice_median]+1,borne_sup]
    
    print(f"intervalle inférieur : {intervalle_inf}") if debug else None
    print(f"intervalle supérieur : {intervalle_sup}") if debug else None

    for instance in data:
        instance_discretise = instance.copy()
        if float(instance[attribut]) <= intervalle_inf[1]:
            instance_discretise[attribut] = f"[{intervalle_inf[0]};{intervalle_inf[1]}]"
        else:
            instance_discretise[attribut] = f"[{intervalle_sup[0]};{intervalle_sup[1]}]"
        data_discretise.append(instance_discretise)

    donnees_possibles_discretise[attribut] = {f"[{intervalle_inf[0]};{intervalle_inf[1]}]",f"[{intervalle_sup[0]};{intervalle_sup[1]}]"}
    print(f"données discrétisées : {data_discretise}") if debug else None
    print(f"valeurs possibles discrétisées : {donnees_possibles_discretise}") if debug else None
    return data_discretise,donnees_possibles_discretise

# TESTS -----------------------------------------------------------------------

# if __name__ == '__main__':
    # filename = "data/golf.csv"

    # for instance in read_data(filename)[0]:
    #     print(instance)
    # print('\n')
    # print(read_data(filename)[1])
    # print('\n')

    # attribut_classe = 'play'
    # data,donnees_possibles = read_data(filename)
    # arbre=construire_arbre(data,donnees_possibles,attribut_classe)


    # afficher_arbre(arbre,debug=True)


    # filename = "data/golf_bis.csv"
    # data,donnees_possibles = read_data(filename)
    # colonnes_a_discretiser = ['temp','humidity']
    # data,donnees_possibles = discretser_data(data,donnees_possibles,colonnes_a_discretiser,nb_domaines=4)

    # arbre_bis=construire_arbre(data,donnees_possibles,attribut_classe)
    # afficher_arbre(arbre_bis,debug=True)

    # TEST C4.5
    # filename = "data/golf_copy.csv"
    # attribut_classe = 'play'
    # data,donnees_possibles = read_data(filename)

    # donnees_discretisables = liste_discretisable(donnees_possibles)
    # for attribut in donnees_discretisables:
    #     data,donnees_possibles=discretiser(data,donnees_possibles,attribut,donnees_discretisables[attribut])
    # print(data)
    # print(donnees_possibles)

    # arbre = construire_arbre(data,donnees_possibles,attribut_classe,method="C45")
    # afficher_arbre(arbre,debug=True)
    # attribut = "outlook"
    # print(calcul_gains(data,donnees_possibles,attribut_classe)[attribut])
    # print(split_entropie(data,donnees_possibles,attribut,attribut_classe))
    # print(ratio_gain(data,donnees_possibles,attribut_classe))
    # arbre=construire_arbre(data,donnees_possibles,attribut_classe,method="C45")
    # afficher_arbre(arbre,debug=True)