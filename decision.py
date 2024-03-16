import csv
import math 
import json

def construire_arbre(data,donnees_possibles,attribut_classe='class',racine={}):
    gains = calcul_gains(data,donnees_possibles,attribut_classe)
    meilleur_attribut = max(gains, key=gains.get)
    print(f"meilleur attribut : {meilleur_attribut}")

    racine = {meilleur_attribut:{}}

    for valeur in donnees_possibles[meilleur_attribut]:
        racine[meilleur_attribut][valeur] = {}

    print(f"\033[32m\033[1marbre créé avec la racine {meilleur_attribut}\033[0m")
    afficher_arbre(racine)
    print('\n\n')


    sous_ensembles = {}
    for valeur in donnees_possibles[meilleur_attribut]:
        sous_ensembles[valeur] = [instance for instance in data if instance[meilleur_attribut] == valeur]

    for valeur,ensemble in sous_ensembles.items():
        for instance in ensemble:
            del instance[meilleur_attribut]
        print(f"\n\n\033[32m\033[1mnouvel arbre pour {valeur}\033[0m :: {ensemble}\n")

        print(donnees_possibles)
        donnees_possibles_sans_attribut = donnees_possibles.copy()
        del donnees_possibles_sans_attribut[meilleur_attribut]
        gains=calcul_gains(ensemble,donnees_possibles_sans_attribut,attribut_classe)
        print(gains)
        if all(gain == 0 for gain in gains.values()):
            print(f"feuille avec valeur de classe {ensemble[0][attribut_classe]}")
            racine[meilleur_attribut][valeur] = ensemble[0][attribut_classe]
            print(f"racine : {racine}")
        else:
            meilleur_attribut_enfant = max(gains, key=gains.get)
            print(f"nouvel arbre avec attribut {meilleur_attribut_enfant}")
            valeurs_possibles_attr_enf = donnees_possibles_sans_attribut[meilleur_attribut_enfant]
            print(f"valeurs possibles pour {meilleur_attribut_enfant} : {valeurs_possibles_attr_enf}")

            
            racine[meilleur_attribut][valeur] = {meilleur_attribut_enfant:{}}
            for val in valeurs_possibles_attr_enf:
                racine[meilleur_attribut][valeur][meilleur_attribut_enfant][val] = {}
            print(f"meilleur attribut : {meilleur_attribut_enfant}")
            afficher_arbre(racine[meilleur_attribut][valeur]) 
            
            abr=construire_arbre(
                ensemble,
                donnees_possibles_sans_attribut,
                attribut_classe,
                racine[meilleur_attribut][valeur][meilleur_attribut_enfant])
            racine[meilleur_attribut][valeur] = abr

    afficher_arbre(racine)
    print(racine[meilleur_attribut])
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