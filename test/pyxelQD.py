import random as rd

import os
import numpy as np
import pyxel

import utils.my_quadtree as qd

# Initialisation de la fenêtre Pyxel
width, height = 256, 256
pyxel.init(width, height, title="Pyxel Quadtree Test")

# Crée le domaine et l'initialise avec un QuadTree
domain = qd.Rect(0, 0, width, height)
qtree = qd.QuadTree(domain, max_points=3, depth=3, max_depth=1)

# Génération des points
N = 250
coords = np.random.randn(N, 2) * height / 3 + (width / 2, height / 2)
points = [qd.Point(rd.randint(1, 255), rd.randint(1, 255)) for it in range(N)]
print(len(coords))
# points = [qd.Point(*coord) for coord in coords]

# Insertion des points dans le quadtree
for point in points:
    qtree.insert(point)

# Fonction de mise à jour (obligatoire pour Pyxel, même si elle est vide)
def update():
    global domain, qtree
    points = qtree.collect_points()
    pyxel.camera(pyxel.mouse_x, pyxel.mouse_y)


    for point in points:
        point.x_pos += rd.randint(-1, 1)
        point.y_pos += rd.randint(-1, 1)

    qtree = qd.dynamic_update(qtree, points)

# Fonction de dessin
def draw():
    # Efface l'écran
    pyxel.cls(0)

    # Dessine le quadtree et les points
    qtree.draw()

    pyxel.mouse(True)

    # Dessine chaque point
    for point in points:
        px, py = point.x_pos, point.y_pos
        pyxel.pset(int(px), int(py), 8)  # Utilise la couleur 8 pour les points

    # Définition d'une région de recherche (rectangulaire)
    region = qd.Rect(20, 76, 80, 80)

    # Liste pour les points trouvés dans la région
    found_points = []
    pyxel.rectb(int(region.x_pos), int(region.y_pos),
                int(region.width), int(region.height), 9)
    found_points = qtree.query(region, found_points)

    # Affiche les points trouvés en rouge
    for point in found_points:
        px, py = point.x_pos, point.y_pos
        pyxel.pset(int(px), int(py), 9)  # Utilise la couleur 9 pour les points trouvés

    os.system("cls")
    print('Number of found points =', len(found_points))
    # Dessine la région de recherche en rouge
    pyxel.rectb(int(region.x_pos), int(region.y_pos),
                int(region.width), int(region.height), 9)

# Démarre la boucle principale de Pyxel
pyxel.run(update, draw)