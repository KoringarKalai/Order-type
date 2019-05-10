import numpy as np
from scipy import spatial
import cv2

class Vecteur:
    "Structure de vecteur"

def test():
    listePoint = []
    p1 = Vecteur()
    p1.x = 10
    p1.y = 10
    p1.num = 1
    p2 = Vecteur()
    p2.x = 90
    p2.y = 10
    p2.num = 2
    p3 = Vecteur()
    p3.x = 90
    p3.y = 90
    p3.num = 3
    p4 = Vecteur()
    p4.x = 10
    p4.y = 90
    p4.num = 4
    p5 = Vecteur()
    p5.x = 75
    p5.y = 50
    p5.num = 5
    listePoint.append(p1)
    listePoint.append(p2)
    listePoint.append(p3)
    listePoint.append(p4)
    listePoint.append(p5)

    print(comparaison(p1,p2,p1,p2))
    print(comparaison(p1,p2,p2,p3))
    print(comparaison(p1,p2,p3,p4))
    print(comparaison(p1,p2,p4,p5))
    print(comparaison(p1,p2,p2,p3))
    print(comparaison(p1,p2,p3,p5))
    print(comparaison(p1,p2,p3,p4))
    print(comparaison(p1,p2,p5,p3))
    print(comparaison(p1,p2,p3,p4))
    print(comparaison(p1,p2,p3,p4))
    centre = [p1,p2]
    lps = triBulle(listePoint,centre)
    image = np.zeros((100, 100, 3), np.uint8)
    for i in range(0,len(listePoint)):
        print(lps[i].num)
        image[listePoint[i].x,listePoint[i].y] = [255, 255, 255]
    cv2.imwrite("test.png", image)


# Renvois le sens de rotation de a->b b->c c->a
def orientation(a,b,c) :
    # Initialisation du vecteur AB 
    ab = Vecteur()
    ab.x = b.x - a.x
    ab.y = b.y - a.y
    # Initialisation du vecteur AC  
    ac = Vecteur()
    ac.x = c.x - a.x
    ac.y = c.y - a.y
    # Determinant de la matrice AB AC 
    z = ab.x * ac.y - ab.y * ac.x
    #print(a.x,"\t",a.y,"\t",b.x,"\t",b.y,"\t",c.x,"\t",c.y,"\t",ab.x,"\t",ac.y,"\t",ab.y,"\t",ac.x,"\t",z)
    if z < 10 ** -11 and z > -1 * 10 ** -11:
        return 1
    if z < 0:
        return -1
    else:
        return 1

# Compare l'angle de c et d autour de a en partant de c
def comparaison(a,b,c,d):

    if a.num == c.num :
        return False
    if a.num == d.num :
        return True
    if b.num == c.num :
        return False
    if b.num == d.num :
        return True
    
    # Calcul ordre de c et d autour de a en partant de b
    signeABC = orientation(a,b,c)
    signeABD = orientation(a,b,d)

    if signeABC > 0:
        if signeABD > 0: 
            # ++ 
            signeACD = orientation(a,c,d)
            if signeACD > 0:
                return False
            else : 
                return True
        else: 
            # +- 
            return False
    else: 
        if signeABD > 0: 
            # -+ 
            return True
        else: 
            # -- 
            signeACD = orientation(a,c,d)
            if signeACD > 0:
                return False
            else : 
                return True

# Renvois une copie de la liste triee par angle autour du point centrale en partant du second point donne
def triBulle(points, centre):
    pts = points[:]
    permutation = True
    i = 0
    while permutation == True:
        permutation = False
        i = i + 1
        for j in range(0, len(pts) - i):
            #compare les 2 pts (on echange si pts[j] > pts[j+1])
            if comparaison(centre[0], centre[1], pts[j], pts[j+1]):
                permutation = True
                # On echange les deux elements
                pts[j], pts[j + 1] = \
                pts[j + 1],pts[j]
    return pts

# Genere une image de taille size contenant les points de la liste points
def genererImageGinibre(size, points, nom):
    # Dessine une image noir de taille size
    image = np.zeros((size, size, 3), np.uint8)
    for i in range(0,len(points)):
        x = int(points[i].x / np.sqrt(len(points)) * size/8 - size/2)
        y = int(points[i].y / np.sqrt(len(points)) * size/8 - size/2)
        
        image[x,y] = [255, 255, 255]
    cv2.imwrite(nom + ".png", image)

# Genere une image de taille size contenant les points de la liste points
def genererImageUnif(size, points, nom):
    # Dessine une image noir de taille size
    image = np.zeros((size, size, 3), np.uint8)
    for i in range(0,len(points)):
        x = int(points[i].x * size/2 - size/2)
        y = int(points[i].y * size/2 - size/2)
        
        image[x,y] = [255, 255, 255]
    cv2.imwrite(nom + ".png", image)

# Genere n point repartis de facon aleatoire avec la loi uniforme dans l'intervale [0,1]²
def genererUniforme(n):
    # Liste des points 
    listePoint = []
    # Genere les n points 
    for i in range(0,n):
        p = Vecteur()
        p.x = np.random.uniform(1, 2) - 1
        p.y = np.random.uniform(1, 2) - 1 
        p.num = i + 1 
        listePoint.append(p)
    # Retour de la liste de points
    return listePoint

# Genere n point repartis de facon aleatoire avec la loi uniforme dans le cercle unitaire
def genererUniformeCircle(n):
    # Liste des points 
    listePoint = []
    # Genere les n points 
    for i in range(0,n):
        p = Vecteur()
        length = np.sqrt(np.random.uniform(0, 1))
        angle = np.pi * np.random.uniform(0, 2)
        p.x = length * np.cos(angle)
        p.y = length * np.sin(angle)
        p.num = i + 1 
        listePoint.append(p)
    # Retour de la liste de points
    return listePoint

# Genere n point repartis de facon aleatoire avec la loi normale centree en 0 de variance 1
def genererNormal(n):
    # Liste des points 
    listePoint = []
    # Genere les n points 
    for i in range(0,n):
        p = Vecteur()
        p.x = np.random.normal(0, 1)
        p.y = np.random.normal(0, 1)
        p.num = i + 1 
        listePoint.append(p)
    # Retour de la liste de points
    return listePoint

# Genere n point repartis de facon aleatoire avec la loi du Ginibre tronque dans l'intervale [0,sqrt(n)]²
def genererGinibre(n):
    # Genere la matrice de taille n x n remplis de nombre complexe aleatoire suivant la loi normale( N(0,1) + N(0,1)i )
    M = np.zeros((n,n),dtype=complex)
    for i in range(0,n):
        for j in range(0,n):
            x = np.random.normal(0, 1)
            y = np.random.normal(0, 1)
            M[i][j] = x + y * 1j
    # Valeurs propre de la matrice M 
    vp = np.linalg.eigvals(M)
    # Liste des points 
    listePoint = []
    for i in range(0,n):
        p = Vecteur()
        p.x = vp[i].real
        p.y = vp[i].imag
        p.num = i + 1 
        listePoint.append(p)
    return listePoint

def genererEvolveBruit(size, n, old, bruit):
    # Liste des points 
    listePoint = []
    # Genere les n points 
    for i in range(0,n):
        p = old[i]
        p.x = old[i].x + (0.5 - np.random.rand()) * bruit
        p.y = old[i].y + (0.5 - np.random.rand()) * bruit

        p.x = size if p.x > size else p.x
        p.x = 0 if p.x < 0 else p.x

        p.y = size if p.y > size else p.y
        p.y = 0 if p.y < 0 else p.y

        listePoint.append(p)
    # Retour de la liste de points
    return listePoint

# Retourne la signature minimale du la liste de points points
def signature(points):
    # Initialisation du mot 
    minmot = "z"

    # Pour chaque numerotation 12
    for i in range(0,len(points)):
        for j in range(0,len(points)):
            if i != j:
                # On recupere les deux premiers points du tableau 
                centre = [points[i] , points[j]]
                # On on effectue le trie par rapport a ces deux points 
                firstSort = triBulle(points, centre)
                # On les renumerote 
                for k in range(0,len(points)):
                    firstSort[k].num = k + 1
                # On genere le mot 
                # On initialise le mot 
                mot = ""
                # On cree le mot pour chaque point de depart 
                for i2 in range(0,len(points)):
                    if i2 == 0 :
                        centre = [firstSort[0] , firstSort[1]]
                    else :
                        centre = [firstSort[i2], firstSort[0]]
                    lpSorted = triBulle(firstSort, centre)
                    for j2 in range(0,len(lpSorted)):
                        if i2 + 1 != lpSorted[j2].num :
                            mot = mot + "" + str(lpSorted[j2].num)
                    #mot += "\n"
                    if mot > minmot:
                        break
                if minmot > mot:
                    minmot = mot
    return minmot

# Retourne la signature minimale avec l'enveloppe convexe pour les choix de 1 et 2 
def signatureHull(points):
    # Initialisation du mot 
    minmot = "z"
    
    # On formate les points pour utiliser la fonction qui trouve l'enveloppe convexe
    tab = listeToTab(points)
    # On calcule l'envelope convexe
    hull = spatial.qhull.ConvexHull(tab)
    # Pour chaque couple de points consecutif sur l'enveloppe convexe on calcule la signature en triant autour des points 
    for simplex in hull.simplices:
        # On recupere les deux points consecutif de l'enveloppe 
        centre = [points[simplex[0]] , points[simplex[1]]]
        # On on effectue le trie par rapport a ces deux points 
        firstSort = triBulle(points, centre)
        # On renumerote les points 
        for i in range(0,len(points)):
            firstSort[i].num = i + 1
        # On initialise le mot avec le 1er tri
        mot = ""
        # On cree le mot pour chaque point de depart 
        for i2 in range(0,len(points)):
            if i2 == 0 :
                centre = [firstSort[0] , firstSort[1]]
            else :
                centre = [firstSort[i2], firstSort[0]]
            lpSorted = triBulle(firstSort, centre)
            for j2 in range(0,len(lpSorted)):
                if i2 + 1 != lpSorted[j2].num :
                    mot = mot + " " + str(lpSorted[j2].num)
            #mot += "\n"
            if mot > minmot:
                break
        if minmot > mot:
            minmot = mot
    return minmot

# Affiche les coordonee des points
def printPoints(points):
    for k in range(0,len(points)):
        print("P",points[k].num,": (",points[k].x,",",points[k].y,")")

# Retourne un tableau contenant les points donne dans la forme [xi,yi]
def listeToTab(points):
    res = np.array([[0 for x in range(2)] for y in range(len(points))] )
    for k in range(0,len(points)):
        res[k] = [points[k].x , points[k].y]
    return res
# -------------------------------------------- Main --------------------------------------------------------- #

# Taille des images
size = 100
# Nombre de point a creer
n = 5
# Exemple de generation d'une image et de retour de signature 
lp = genererUniformeCircle(n)
genererImageUnif(size,lp,"UnifCircle")
# print(signature(lp))

mapUniforme = {}
mapGinibre = {}
for i in range(0,100000) :
    if i%1000 == 0: 
        print(i)
        print("UNIFORME : Nombre de signature differentes : ",len(mapUniforme))
        print(mapUniforme)
        print("GINIBRE : Nombre de signature differentes : ",len(mapGinibre))
        print(mapGinibre)

    # ----------------------------------- STATS GINIBRE ------------------------------------ #
    lp = genererGinibre(n)
    # genererImageGinibre(size,lp,"Ginibre")
    s = signature(lp)
    if s in mapGinibre :
        mapGinibre[s] = mapGinibre[s] + 1 
    else :
        mapGinibre[s] = 1 
        genererImageGinibre(size,lp,s)
    # ----------------------------------- STATS UNIFORM ------------------------------------ #
    lp = genererUniformeCircle(n)
    # genererImageGinibre(size,lp,"Ginibre")
    s = signature(lp)
    if s in mapUniforme :
        mapUniforme[s] = mapUniforme[s] + 1 
    else :
        mapUniforme[s] = 1 
        genererImageUnif(size,lp,s)

print("UNIFORME : Nombre de signature differentes : ",len(mapUniforme))
print(mapUniforme)
print("GINIBRE : Nombre de signature differentes : ",len(mapGinibre))
print(mapGinibre)

