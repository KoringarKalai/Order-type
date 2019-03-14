import numpy as np
import cv2

class Point:

class Vecteur:

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


# Dessine une image noir de taille size
size = 100
image = np.zeros((size, size, 3), np.uint8)
image2 = np.zeros((size, size, 3), np.uint8)

# Dessine n point blanc repartis de facon aleatoire
n = 5
for i in range(0,n):
    x = int(np.random.uniform(0, 1) * size)
    y = int(np.random.uniform(0, 1) * size)
    image[x,y] = [255, 255, 255]

# Genere la matrice de taille n x n remplis de nombre complexe aleatoire ( N(0,1) + N(0,1)i )
n = 5
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
    p = Point()
    p.x = int(vp[i].real / np.sqrt(n) * size / 4 + size / 2)
    p.y = int(vp[i].imag / np.sqrt(n) * size / 4 + size / 2)
    p.num = i + 1 
    listePoint.append(p)

for i in range(0,len(listePoint)):
    p = listePoint[i]
    image2[p.x,p.y] = [255,255,255]


# Initialisation du mot 
minmot = "z"
for k in range(0,len(listePoint)):
    centre = [listePoint[k] , listePoint[1]]
    listePoint = triBulle(listePoint, centre)
    for i in range(0,len(listePoint)):
        listePoint[i].num = i + 1
    # On initialise le mot 
    mot = ""
    # On cree le mot pour chaque point de depart 
    for i in range(0,len(listePoint)):
        if i == 0 :
            centre = [listePoint[0] , listePoint[1]]
        else :
            centre = [listePoint[i], listePoint[0]]
        lpSorted = triBulle(listePoint, centre)
        for j in range(0,len(lpSorted)):
            if i + 1 != lpSorted[j].num :
                mot = mot + " " + str(lpSorted[j].num)
        mot += "\n"
    if minmot > mot:
        minmot = mot

print(minmot)
# Actual min 2 3 4 5 1 3 4 5 1 4 2 5 1 3 5 2 1 3 4 2

for k in range(0,len(listePoint)):
    print("P",listePoint[k].num,": (",listePoint[k].x,",",listePoint[k].y,")")
# Sauvegarde de l'image en png
cv2.imwrite("result.png", image)
cv2.imwrite("result2.png", image2)