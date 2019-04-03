import numpy as np
from scipy import spatial
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
    #print(a.x,"\t",a.y,"\t",b.x,"\t",b.y,"\t",c.x,"\t",c.y,"\t",ab.x,"\t",ac.y,"\t",ab.y,"\t",ac.x,"\t",z)
    if z < 10 ** -11 and z > -1 * 10 ** -11:
        return 1
    if z < 0:
        return -1
    else:
        return 1

# Compare l'angle de c et d autour de a en partant de c
def comparaison(a,b,c,d):
    # Calcul ordre de c et d autour de a en partant de b
    signeABC = orientation(a,b,c)
    signeABD = orientation(a,b,d)

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
    pts = points[:]
    for i in range(0,len(points)):
        pts[i].x = int(pts[i].x * size / len(points))
        pts[i].y = int(pts[i].y * size / len(points))
    # Dessine une image noir de taille size
    image = np.zeros((size, size, 3), np.uint8)
    for i in range(0,len(pts)):
        image[pts[i].x,pts[i].y] = [255, 255, 255]
    cv2.imwrite(nom + ".png", image)

# Genere n point repartis de facon aleatoire avec la loi uniforme dans l'intervale [0,size]²
def genererUniforme(n):
    # Liste des points 
    listePoint = []
    # Genere les n points 
    for i in range(0,n):
        p = Vecteur()
        p.x = np.random.uniform(0, 1)
        p.y = np.random.uniform(0, 1)
        p.num = i + 1 
        listePoint.append(p)
    # Retour de la liste de points
    return listePoint

# Genere n point repartis de facon aleatoire avec la loi normale dans l'intervale [0,size]²
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

# Genere n point repartis de facon aleatoire avec la loi du Ginibre tronque dans l'intervale [0,size]²
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
            #mot += "\n"
            if mot > minmot:
                break
        if minmot > mot:
            minmot = mot

    return minmot
    # Actual min 2 3 4 5 1 3 4 5 1 2 4 5 1 3 2 5 1 3 2 4

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

        #################### LE PROBLEME VIENS D'ICI #########################
        # Normalement le 1er points autour duquel on tourne devrait etre le 1er point 
        #   dans notre tableau trie (firstsort) le probleme sera aussi present 
        #   a chaque nouveau tri.
        # Le resultat du print suivant devrait etre a b a b et non a b c d 
        print(firstSort[0].x,firstSort[0].y,points[simplex[0]].x,points[simplex[0]].y)
        ######################################################################
        #for j in range(0,len(firstSort)):
        #    if 1 != firstSort[j].num :
        #        mot = mot + " " + str(firstSort[j].num)
        for i in range(1,len(points)):
            # On recupere les deux points 
            centre = [firstSort[i], points[simplex[0]]]
            # On trie avec les deux points en centre 
            lpSorted = triBulle(firstSort,centre)
            # On ecrit la suite du mot 
            for j in range(0,len(lpSorted)):
                if i + 1 != lpSorted[j].num :
                    mot = mot + " " + str(lpSorted[j].num)
            # Si notre mot est deja moins bien que le plus petit mot on arrete de le calculer
            if minmot < mot:
                break
        # On test si le mot est le plus petit 
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
lp = genererGinibre(n)
genererImage(size,lp,"Ginibre")
print(signatureHull(lp))

map = {}
for i in range(0,100) :
    if i%1000 == 0: 
        print(i)
    lp = genererGinibre(n)
    genererImage(size,lp,"Ginibre")
    s = signatureHull(lp)
    if s in map :
        map[s] = map[s] + 1 
    else :
        map[s] = 1 

print(len(map))
print(map)
#TODO 
# 1. Signature :
#       - Corriger