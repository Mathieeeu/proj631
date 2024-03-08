import csv
import math 

class Tree:
    def __init__(self,attribut):
        self.attribut = attribut
        self.enfants = {}
    
    def __str__(self):
        return f"Tree({self.attribut})"
    
    def __repr__(self):
        return f"Tree({self.attribut})"
    
    def add_enfant(self,valeur,arbre):
        self.enfants[valeur] = arbre

def afficher_arbre(arbre,indent=0):
    print(f"{'-'*indent}{arbre.attribut}")
    for valeur,enfant in arbre.enfants.items():
        print(f"{' '*(indent+1)}\{valeur}")
        afficher_arbre(enfant,indent+4)


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

def calcul_gains(filename,data,donnees_possibles,attribut_classe='class'):
    """
    calcul du gain d'information pour un attribut avec les formules de la doc
    """
    gains={}
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
            print(f"gain({attribut})\t= {(round(gain,3))}")
            gains[attribut] = gain
    return gains

def creer_arbre(filename,data,donnees_possibles,attribut_classe='class'):
    gains = calcul_gains(filename,data,donnees_possibles,attribut_classe)
    meilleur_attribut = max(gains, key=gains.get)
    print(f"\nmeilleur attribut: {meilleur_attribut}")

    arbre = Tree(meilleur_attribut)

    for valeur in donnees_possibles[meilleur_attribut]:
        print(f"pour {meilleur_attribut} = {valeur}")
        sous_ensemble = [instance for instance in data if instance[meilleur_attribut] == valeur]
        for i in range(len(sous_ensemble)):
            print(sous_ensemble[i])
        print()
        if len(sous_ensemble) <= 1:
            print(f"feuille: {sous_ensemble[0][attribut_classe]}")
            arbre.add_enfant(valeur,Tree(sous_ensemble[0][attribut_classe]))
        else:
            donnees_possibles_restantes = donnees_possibles.copy()
            del donnees_possibles_restantes[meilleur_attribut]
            arbre.add_enfant(valeur,creer_arbre(filename,sous_ensemble,donnees_possibles_restantes,attribut_classe))
    return arbre


filename = "data/golf.csv"
for instance in read_data(filename)[0]:
    print(instance)
print('\n')
print(read_data(filename)[1])

print('\n')
attribut_classe = 'play'
data,donnees_possibles = read_data(filename)
arbre=creer_arbre(filename,data,donnees_possibles,attribut_classe)
print('\n')
afficher_arbre(arbre)