import pyxel

from entity.monsters.mob import Mob
from entity.player import Player
from utils.sprite import Sprites, Sprite
from utils.timer import Timer
from entity.entity import Entity
import game_state as gs
from utils.my_quadtree import Point
from weapons.map import Map  # On importe la classe Map pour gérer les entités

# Initialisation de Pyxel
pyxel.init(256, 256)
pyxel.load("../rsc/3.pyxres")

# Variables pour la rotation et le sprite
rotation = 0
spr = Sprites([Sprite(0, 24, 16, 16), Sprite(16, 24, 16, 16)])
flip_u = Timer(180)

# Initialisation de la carte et des entités
game_map = Map()

# Ajout d'exemples d'entités (deux entités pour tester les collisions)
entity1 = Mob(50, 50, 2, 16)  # Entité avec une position et une hitbox
entity2 = Mob(80, 80, 4, 16)
gs.player = Player()

game_map.insert(entity1)
game_map.insert(entity2)
game_map.insert(gs.player)


def draw():
    pyxel.cls(0)

    # Dessiner les entités sur la carte
    for entity in game_map.items:
        pyxel.rectb(entity.x_pos, entity.y_pos, entity.hitbox.width, entity.hitbox.height, 7)  # Exemple de dessin d'une hitbox
        entity.draw()
    # Dessiner les autres éléments (sprites)
    spr.draw(34, 34)
    pyxel.blt(80, 80, 0, 0, 24, 16, 16, 5)
    pyxel.blt(128, 128, 0, 0, 24, 16, 16, 5, rotate=rotation)


def update():
    global rotation

    game_map.update()

    spr.next()
    if flip_u.event():
        spr.flip_east()
        print("FLIP")

    rotation = rotation + 15
    spr.rotate(rotation)
    rotation %= 360

    Timer.time_update()

pyxel.run(update, draw)
