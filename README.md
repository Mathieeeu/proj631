Arbres de décision ID3 et C4.5
=======

Introduction
-----------
Un arbre de décision est un outil d'aide à la décision représentant par un arbre des ensembles de 
choix conduisant aux décisions. Les différentes décisions possibles sont situées aux extrémités des 
branches (les « feuilles » de l'arbre), et sont atteintes en fonction de décisions prises à chaque étape. 

Features
-----------
- Création d'un arbre de décision avec les algorithmes ID3 et C4.5
- Affichage de l'arbre de décision
- Création d'une matrice de confusion
- Prise en charge des attributs continus
- Enregistrement de l'arbre de décision dans un fichier séparé

Utilisation
-----------
Pour utiliser ce programme, il faut executer le fichier `main.py` avec la commande suivante : `python main.py`. Celui-ci contient un exemple d'utilisation des arbres de décision avec l'algorithmes ID3 pour le jeu de données `"golf.csv"`.

ID3
-----------
ID3 (Iterative Dichotomiser 3) est un algorithme de classification qui construit un arbre de décision.
L'algorithme calcule l'entropie de chaque attribut et choisit l'attribut qui a l'entropie la plus basse, c'est-à-dire celui qui différentie le mieux les données.

Les étapes de l'algorithme sont les suivantes :
1.  - Calculer l'entropie de chaque attribut et selection du "meilleur" attribut. L'entropie est une mesure de l'incertitude d'un ensemble de données; plus l'entropie est élevée, plus les données sont dispersées.
    - Créer un noeud de l'arbre avec l'attribut sélectionné
2. Partitionner l'ensemble d'apprentissage en sous-ensembles en fonction des valeurs de l'attribut sélectionné
3. Répéter les étapes 1 et 2 pour chaque sous-ensemble jusqu'à satisfaire l'une des conditions d'arret suivantes :
    - Il n'y a plus d'exemples d'apprentissage
    - Tous les exemples d'apprentissage appartiennent à la même classe
    - Il n'y a plus d'attributs à tester

Pour créer un arbre avec cet algorithme, il faut executer la commande suivante : `construire_arbre(donnees,donnees_possibles,classe,method="ID3")` (le paramètre method est optionnel, par défaut il est égal à "ID3").

C4.5
-----------
C4.5 est une extension de l'algorithme ID3. Cependant, C4.5 utilise le rapport de gain d'information pour choisir l'attribut qui sera utilisé pour diviser les données.

C4.5 présente les extensions suivantes par rapport à ID3 :
- Gestion des valeurs manquantes
- Gestion des attributs continus
- Post-elagage de l'arbre

Pour créer un arbre avec cet algorithme, il faut executer la commande suivante : `construire_arbre(donnees,donnees_possibles,classe,method="C45")`.

Format de l'arbre
-----------
L'arbre est représenté sous forme de dictionnaire.
Chaque noeud est un nouveau dictionnaire avec comme clés les valeurs possibles de l'attribut et comme valeur un autre dictionnaire représentant le noeud suivant.
Les feuilles de l'arbre sont des dictionnaires avec une seule clé "classe" et comme valeur la classe prédite.

Exemple d'arbre :
```
{'outlook': {'sunny': {'temp': {'mild': {'play': 'no'}, 'cool': {'play': 'yes'}, 'hot': {'play': 'no'}}}, 'rain': {'wind': {'false': {'play': 'yes'}, 'true': {'play': 'no'}}}, 'overcast': {'play': 'yes'}}}
```

Affichage de l'arbre
-----------
Pour afficher l'arbre, il faut executer la commande suivante : `afficher_arbre(arbre,debug=True)`.
Lors de l'execution de cette commande, l'arbre sera affiché sous forme de texte dans la console et enregistré dans un fichier "arbre.json".

Matrice de confusion
-----------
La matrice de confusion est un outil permettant de mesurer la qualité d'un système de classification.
Elle permet de visualiser les erreurs de classification en comparant les classes prédites avec les classes réelles.

Pour créer la matrice de confusion, il faut executer la commande suivante : `matrice_confusion(donnees,donnees_possibles,arbre,classe)`.

