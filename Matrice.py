class CMatrice:
    def __init__(self, n, entetes_lignes=None, entetes_colonnes=None):
        self.n = n  
        self.entetes_lignes = entetes_lignes
        self.entetes_colonnes = entetes_colonnes
        self.matrice = [[0 for j in range(n)] for i in range(n)]

    def __str__(self):
        s = ''
        if self.entetes_colonnes:
            s += '\t' + '\t'.join(self.entetes_colonnes) + '\n'
        for i in range(self.n):
            if self.entetes_lignes:
                s += self.entetes_lignes[i] + '\t'
            for j in range(self.n):
                s += str(self.matrice[i][j]) + '\t'
            s += '\n'
        return s
    
    def __getitem__(self, i):
        return self.matrice[i]

    def __setitem__(self, i, value):
        self.matrice[i] = value

    def __len__(self):
        return self.n
    
    def edit_entetes_lignes(self, entetes_lignes):
        self.entetes_lignes = entetes_lignes

    def edit_entetes_colonnes(self, entetes_colonnes):
        self.entetes_colonnes = entetes_colonnes

