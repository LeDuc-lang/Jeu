import pyxel

from entity.entity import Entity
from entity.player import Player
from utils.sprite import Sprite, Sprites
from weapons.projectile.bullets import Bullet
from rsc.sprites import mob_sprites
from game_state import player_spawn_x, player_spawn_y
import game_state as gs
from entity.xp_orb import XP


class Mob(Entity):
    def __init__(
            self, x: int, y: int, speed: int, hitbox_radius: int = 8
    ):
        super().__init__(x, y, speed, hitbox_radius)
        self.sprites = Sprites([Sprite(16, 120, 16, 16), Sprite(0, 120, 16, 16)])
        self.life = 3

    def _face_towards_player(self) -> None:
        player_x, player_y = gs.player.x_pos, gs.player.y_pos
        if self._x < player_x:
            self.sprites.flip_west()
        if self._x > player_x:
            self.sprites.flip_east()

    def collisions_handler(self, vector):
        for collision in self.collisions():
            # if isinstance(collision, Mob):
            #     vector = self.prevent_overlap(vector, collision)
            # else:
            #     vector = self._bounce_adjust_collision(vector, collision, bounce_factor=1.0)
            if isinstance(collision, Bullet) and collision.owner == 'player' :
                self.take_damage(collision.damage)
                collision.get_removed()
            if isinstance(collision, Mob) or isinstance(collision, Player):
                vector = self.prevent_overlap(vector, collision)
        return vector

    def draw(self):
        self._face_towards_player()
        pyxel.circb(self._x, self._y, self.hitbox_radius, 5 )
        self.sprites.draw(self._x-self.hitbox_radius, self._y-self.hitbox_radius)

    def take_damage(self, damage: int) -> None:
        self.life -= damage

    def is_alive(self):
        if self.life <= 0:
            new_xp = XP(self._x, self._y)
            gs.map.insert(new_xp)
            self.alive = False
            gs.map.remove(self)


    def update(self) -> None:
        self.move_to(gs.player)
        self.is_alive()
