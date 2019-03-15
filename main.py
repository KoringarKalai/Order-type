import numpy as np
import cv2

class Vecteur:
    "Structure de vecteur"

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
    if z == 0: 
        return 0
    if z < 0:
        return -1
    else:
        return 1

# Compare l'angle de c et d autour de a en partant de c
def comparaison(a,b,c,d):
    # Calcul ordre de c et d autour de a en partant de b
    signeABC = orientation(a,b,c)
    signeABD = orientation(a,b,d)

    if signeABC == 0: 
        return True
    if signeABD == 0:
        return False

    if signeABC > 0:
        if signeABD > 0: 
            # ++ 
            signeADB = orientation(a,d,b)
            if signeADB > 0:
                return True
            else : 
                return False
        else: 
            # +- 
            return True
    else: 
        if signeABD > 0: 
            # -+ 
            return False
        else: 
            # -- 
            signeADB = orientation(a,d,b)
            if signeADB > 0:
                return True
            else : 
                return False

# Renvois une copie de la liste triee par angle autour du point centrale en partant du second point donne
def triBulle(points, centre):
    pts = points[:]
    for i in range(len(pts)):
        for j in range(i):
            #compare les 2 pts
            if comparaison(pts[j],pts[j+1], centre[0], centre[1]):
                temp = pts[j]
                pts[j] = pts[j+1]
                pts[j+1] = temp
    return pts

# Genere une image de taille size contenant les points de la liste points
def genererImage(size, points, nom):
    # Dessine une image noir de taille size
    image = np.zeros((size, size, 3), np.uint8)
    for i in range(0,len(points)):
        image[points[i].x,points[i].y] = [255, 255, 255]
    cv2.imwrite(nom + ".png", image)

# Genere n point repartis de facon aleatoire avec la loi uniforme dans l'intervale [0,size]²
def gerererUniforme(size, n):
    # Liste des points 
    listePoint = []
    # Genere les n points 
    for i in range(0,n):
        p = Vecteur()
        p.x = int(np.random.uniform(0, 1) * size)
        p.y = int(np.random.uniform(0, 1) * size)
        p.num = i + 1 
        listePoint.append(p)
    # Retour de la liste de points
    return listePoint

# Genere n point repartis de facon aleatoire avec la loi normale dans l'intervale [0,size]²
def gerererNormal(size, n):
    # Liste des points 
    listePoint = []
    # Genere les n points 
    for i in range(0,n):
        p = Vecteur()
        p.x = int(np.random.normal(0, 1) * size)
        p.y = int(np.random.normal(0, 1) * size)
        p.num = i + 1 
        listePoint.append(p)
    # Retour de la liste de points
    return listePoint

# Genere n point repartis de facon aleatoire avec la loi du Ginibre tronque dans l'intervale [0,size]²
def genererGinibre(size,n):
    # Genere la matrice de taille n x n remplis de nombre complexe aleatoire ( N(0,1) + N(0,1)i )
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
        p.x = int(vp[i].real / np.sqrt(n) * size / 4 + size / 2)
        p.y = int(vp[i].imag / np.sqrt(n) * size / 4 + size / 2)
        p.num = i + 1 
        listePoint.append(p)
    return listePoint

# Retourne la signature minimale du la liste de points points
def signature(points):
    # Initialisation du mot 
    minmot = "z"

    for k in range(0,len(points)):
        centre = [points[k] , points[1]]
        points = triBulle(points, centre)
        for i in range(0,len(points)):
            points[i].num = i + 1
        # On initialise le mot 
        mot = ""
        # On cree le mot pour chaque point de depart 
        for i in range(0,len(points)):
            if i == 0 :
                centre = [points[0] , points[1]]
            else :
                centre = [points[i], points[0]]
            lpSorted = triBulle(points, centre)
            for j in range(0,len(lpSorted)):
                if i + 1 != lpSorted[j].num :
                    mot = mot + " " + str(lpSorted[j].num)
            mot += "\n"
        if minmot > mot:
            minmot = mot

    return minmot
    # Actual min 2 3 4 5 1 3 4 5 1 2 4 5 1 3 2 5 1 3 2 4

# Affiche les coordonee des points
def printPoints(points):
    for k in range(0,len(points)):
        print("P",points[k].num,": (",points[k].x,",",points[k].y,")")

# -------------------------------------------- Main --------------------------------------------------------- #

# Taille des images
size = 100
# Nombre de point a creer
n = 5
# Exemple de generation d'une image et de retour de signature 
lp = genererGinibre(size,n)
genererImage(size,lp,"Ginibre")
print(signature(lp))
