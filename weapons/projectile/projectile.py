import game_state as gs
from entity.entity import Entity
from utils.my_quadtree import Rect, Point
from utils.timer import Timer


class Projectile(Entity):
    def __init__(
            self, x: int, y: int, radius: int, angle: tuple | Point, speed, damage, dispawn_delay=60
    ) -> None:
        super().__init__(x, y, speed)
        self._radius = radius
        self.angle = angle
        self.alive = True
        self.owner = 'player'
        self.damage = damage
        self.timer = Timer(dispawn_delay)

    def _is_alive(self):
        if self.timer.event():
            print('removing')
            gs.map.remove(self)
            self.alive = False
            return False
        return True

    def update(self) -> None:
        if self._is_alive():
            self.move_to(self.angle)
        else:
            print('Idling')
