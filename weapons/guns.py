import pyxel

from weapons.projectile.bullets import Bullet
from utils.my_quadtree import Point
from utils.timer import Timer
from utils.sprite import Sprite, Sprites
import game_state as gs


class Weapon:
    def __init__(self, attack_speed) -> None:
        self.shoot_sprites = Sprites([Sprite(n, 16, 8, 8) for n in range(32, 57, 8)])
        self.cooldown = Timer(attack_speed)

    def flip_west(self, x):
        self.shoot_sprites.flip_west()
        # x += 9

    def flip_east(self, x):
        self.shoot_sprites.flip_east()
        # x -= 9

    def get_target_direction(self) -> Point:
        return Point(pyxel.mouse_x, pyxel.mouse_y)


class Rifle(Weapon):
    bullet = Bullet
    damage = 20

    def __init__(self) -> None:
        super().__init__(8)
        self.reach = 30
        self.capacity = 24
        self.magazine = self.capacity
        self.reloadtime = 60
        self.reloading = False

    def reload(self):
        if not self.reloading:
            self.reloadTimer = Timer(self.reloadtime)
            self.reloading = True
            print("Reloading...")

        if self.reloading and self.reloadTimer.event():
            self.magazine = self.capacity  # Remet la capacité maximale
            self.reloading = False
            self.reloadTimer = None
            print("Reload complete!")

    def shoot(self, x, y, direction) -> None:
        if self.reloading:
            self.reload()  # Continue le rechargement
            return

        if self.magazine <= 0:
            print("Magazine empty, reloading...")
            self.reload()
            return

        if self.cooldown.event():  # Vérifie le cooldown avant de tirer
            self.shoot_sprites.next()
            self.shoot_sprites.draw(x-8, 8+y)
            speed = 10

            # Création et insertion de la balle
            bullet = self.bullet(x, y, 2, direction, speed, self.damage, dispawn_delay=self.reach)
            gs.map.insert(bullet)

            self.magazine -= 1  # Réduit les munitions disponibles

# class Shotgun(Weapon):
#     bullet = Balle
#
#     def __init__(self, x, y) -> None:
#         super().__init__(x, y, 15)
#         self.reach = 10
#
#     def shoot(self) -> None:
#         if self.cooldown.event():
#             self.shoot_sprites.next()
#             self.shoot_sprites.draw()
#             balle1 = self.bullet(
#                 self.x,
#                 self.y,
#                 2,
#                 self.get_target_direction(),
#                 5,
#                 dispawn_taille_maximum=self.reach,
#             )
#             balle2 = self.bullet(
#                 self._position_x_arme(),
#                 self._position_y_arme() - 5,
#                 self.get_target_direction() + cos(5),
#                 5,
#                 dispawn_taille_maximum=self.reach,
#             )
#             balle3 = self.bullet(
#                 self._position_x_arme(),
#                 self._position_y_arme() + 5,
#                 self.get_target_direction() - cos(5),
#                 5,
#                 dispawn_taille_maximum=10,
#             )
#             self.balle_tiree.append(balle1)
#             self.balle_tiree.append(balle2)
#             self.balle_tiree.append(balle3)
#             self.dernier_tire = game_clock
#             self.shoot_sprites.expansion_update()
