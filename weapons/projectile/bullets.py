import pyxel

from weapons.projectile.projectile import Projectile
import game_state as gs

class Bullet(Projectile):

    def get_removed(self):
        gs.map.remove(self)
    def draw(self):
        pyxel.circ(self._x, self._y, self._radius, 3)
