from entity.entity import Entity
import game_state as gs
from entity.player import Player
import pyxel

class XP(Entity):
    def __init__(self, x, y):
        self.speed = 8
        super().__init__(x, y, self.speed, 4)
        self.alive = True

    def update(self):
        if self.distance_to(gs.player) < 100:
            self.move_to(gs.player)
            self.getcollect()

    def draw(self):
        pyxel.circ(self._x, self._y, 4, 10)

    def getcollect(self):
        for collision in self.collisions():
            if isinstance(collision, Player):
                gs.xp += 1
                self.alive = False
                gs.map.remove(self)

