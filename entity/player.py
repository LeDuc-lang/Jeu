import pyxel

import game_state
from game_state import player_spawn_x, player_spawn_y, player_default_life, player_speed
from entity.entity import Entity
from utils.sprite import Sprites, Sprite
from weapons.guns import Rifle
from utils.screen_tools import normalize_mouse_pos as n_mouse
from utils.my_quadtree import Point

class Player(Entity):
    def __init__(self, default_life=player_default_life, hitbox_radius=8, weapon=Rifle()):
        init_x, init_y = game_state.SCREEN_CENTER
        init_x -= hitbox_radius
        init_y -= hitbox_radius
        super().__init__(init_x, init_y, player_speed, hitbox_radius)
        self.sprites = Sprites([Sprite(0, 24, 16, 16), Sprite(16, 24, 16, 16)])
        self.life = default_life
        self.weapon = weapon
        # self.weapon = Rifle(self._x, self._y + boite_collision / 2)

    def _face_towards_mouse(self):
        if self._x < pyxel.mouse_x:
            self.sprites.flip_west()
            self.weapon.flip_west(self._x)
        if self._x > pyxel.mouse_x:
            self.sprites.flip_east()
            self.weapon.flip_east(self._x)

    def movement(self) -> None:
        if pyxel.btnp(pyxel.KEY_DOWN, hold=True, repeat=True):
            self.move(0, self.speed)
            # self._y += self.speed
            self.sprites.next()
        if pyxel.btnp(pyxel.KEY_UP, hold=True, repeat=True):
            # self._y -= self.speed
            self.move(0, -self.speed)
            self.sprites.next()
        if pyxel.btnp(pyxel.KEY_LEFT, hold=True, repeat=True):
            # self._x -= self.speed
            self.move(-self.speed, 0)
            self.sprites.next()
        if pyxel.btnp(pyxel.KEY_RIGHT, hold=True, repeat=True):
            # self._x += self.speed
            self.move(self.speed, 0)
            self.sprites.next()

    def shoot_handler(self):
        if pyxel.btnp(pyxel.KEY_E, hold=True, repeat=True):
            direction_x, direction_y = n_mouse()
            self.weapon.shoot(self._x, self._y, Point(direction_x, direction_y))

    def draw(self) -> None:
        self._face_towards_mouse()
        self.sprites.draw(self._x - self.hitbox_radius, self._y - self.hitbox_radius )
        pyxel.circb(self._x, self._y, self.hitbox_radius, 5 )

    #   test point
        x,y = n_mouse()
        pyxel.circb(x, y, self.hitbox_radius, 8 )


    def update(self):
        self.movement()
        self.shoot_handler()
