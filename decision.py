import csv
import math 
import json

def construire_arbre(data,donnees_possibles,attribut_classe='class',racine={}):
    gains = calcul_gains(data,donnees_possibles,attribut_classe)
    meilleur_attribut = max(gains, key=gains.get, default=None)
    print(f"meilleur attribut : {meilleur_attribut}")

    if gains[meilleur_attribut] == 0:
        # si le gain est nul, on a atteint une feuille, on renvoie la valeur de la classe
        print(f"\033[32m\033[1m\033[31mLe gain est nul\033[0m")
        print('\n')
        print(data)
        print(data[0][attribut_classe])
        racine = {attribut_classe:data[0][attribut_classe]}
        return racine
    racine = {meilleur_attribut:{}}

    for valeur in donnees_possibles[meilleur_attribut]:
        racine[meilleur_attribut][valeur] = {}

    print(f"\033[32m\033[1marbre créé avec la racine {meilleur_attribut}\033[0m")
    afficher_arbre(racine)
    print('\n\n')

    for valeur in donnees_possibles[meilleur_attribut]:
        print(f"\033[32mtraitement de la valeur \033[1m{valeur}\033[0m\033[32m de l'attribut {meilleur_attribut}\033[0m")
        sous_ensemble = [instance for instance in data if instance[meilleur_attribut] == valeur]
        print(f"\033[35msous-ensemble : {sous_ensemble}\033[0m")
        print(f"\033[34mdonnées possibles : {donnees_possibles}\033[0m")
        print('\n')

        if len(sous_ensemble)==0:
            print(f"\033[32m\033[1m\033[31mLe sous-ensemble est vide\033[0m")
            print('\n')
            continue
        elif len(sous_ensemble)==1:
            print(f"\033[32m\033[1m\033[31mLe sous-ensemble ne contient qu'une seule instance\033[0m")
            print('\n')
            racine[meilleur_attribut][valeur] = list(sous_ensemble[0].values())[0]
            continue
        elif len(donnees_possibles)==1:
            print(f"\033[32m\033[1m\033[31mIl n'y a plus d'attribut à traiter\033[0m")
            print('\n')
            racine[meilleur_attribut][valeur] = list(sous_ensemble[0].values())[0]
            continue
        else:
            print(f"\033[32m\033[1m\033[31mIl y a encore des attributs à traiter\033[0m")
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
            print(f"\033[35msous-ensemble plus petit : {sous_ensemble_plus_petit}\033[0m")
            print(f"\033[34mdonnées possibles plus petites : {donnees_possibles_plus_petit}\033[0m")
            print(f"\033[33m{racine}\033[0m")
            racine[meilleur_attribut][valeur] = construire_arbre(sous_ensemble_plus_petit,donnees_possibles_plus_petit,attribut_classe)
    afficher_arbre(racine)
    return racine    

def afficher_arbre(racine,indent=0,debug=False):
    if debug:
        pass
    if indent == 0:
        print('\033[32m',end='')
    for cle,valeur in racine.items():
        print(f"{'| '*indent}{cle}")
        if type(valeur) is dict:
            afficher_arbre(valeur,indent+1)
        else:
            print(f"{'| '*(indent+1)}\033[31m{valeur}\033[0m\033[32m")
    if indent == 0:
        print('\033[0m')

    with open('tree.json', 'w') as f:
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

def calcul_gains(data,donnees_possibles,attribut_classe='class'):
    """
    calcul du gain d'information pour un attribut avec les formules de la doc
    """
    gains={}
    print(donnees_possibles)
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
            print(f"gain({attribut})\t= {(round(gain,10))}")
            gains[attribut] = gain
    return gains


filename = "data/golf.csv"
for instance in read_data(filename)[0]:
    print(instance)
print('\n')
print(read_data(filename)[1])

print('\n')
attribut_classe = 'play'
data,donnees_possibles = read_data(filename)
arbre=construire_arbre(data,donnees_possibles,attribut_classe)
print('\nArbre construit :')
afficher_arbre(arbre,debug=True)