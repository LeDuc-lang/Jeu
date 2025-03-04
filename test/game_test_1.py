import os
import pyxel
import random as rd
from entity.player import Player
from utils.my_quadtree import *
from entity.monsters.mob import *
import weapons.guns as wp
import game_state as gs
import gui.overlay as overlay
from utils.timer import Timer
from entity.xp_orb import XP

# Définir le décorateur pause en dehors de la classe Game
def pause_listener(funct):
    def wrapper(self, *args, **kwargs):
        if pyxel.btnp(pyxel.KEY_U):  # Appuyer sur 'U' pour mettre en pause
            self.pause = not self.pause
            print(gs.map.collect_points())
        if not self.pause:
            return funct(self, *args, **kwargs)
    return wrapper

class Game:
    def __init__(self):
        self.pause = False  # Initialiser l'état de pause
        self. screen_width, self.screen_height = gs.SCREEN_WIDTH, gs.SCREEN_HEIGHT
        pyxel.init(self.screen_width, self.screen_height)
        pyxel.load("../rsc/3.pyxres")
        gs.map = QuadTree(Rect(0, 0, self.screen_width, self.screen_height), max_points=2)
        self.map = gs.map
        gs.player = Player()
        self.player = gs.player
        self.items = [Mob(50, 50, 2), Mob(256, 256, 2), gs.player]
        self.items += [Mob(rd.randint(0, 256), rd.randint(0, 256), 2) for _ in range(120)]
        for item in self.items:
            gs.map.insert(item)

    @pause_listener
    def update(self):
        # Collecte les points avant de commencer l'itération pour ne pas modifier la liste pendant l'itération
        current_items = gs.map.collect_points()

        self.items = current_items  # Met à jour les éléments à partir de la collecte actuelle

        for item in self.items:
            item.update()

        gs.map = dynamic_update(gs.map, self.items)
        Timer.time_update()
        pyxel.camera(gs.player.x_pos - (self.screen_width / 2 - 8), gs.player.y_pos - (self.screen_height / 2 - 8))

    @pause_listener
    def draw(self):
        pyxel.cls(0)
        gs.map.draw()
        for item in self.items:
            item.draw()
        pyxel.mouse(True)
        gs.player.draw()
        overlay.show()



    def run(self):
        pyxel.run(self.update, self.draw)

if __name__ == '__main__':
    Game().run()
