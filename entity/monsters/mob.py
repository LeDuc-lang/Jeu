import pyxel
import math 

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

    def _face_toward_mob(self, other) -> None:
        if isinstance(other, Mob):
            return


    def collisions_handler(self, vector):
        for collision in self.collisions():
            if isinstance(collision, Bullet) and collision.owner == 'player':
                self.take_damage(collision.damage)
                collision.get_removed()
            # Gestion spécifique pour les collisions entre mobs :
            elif isinstance(collision, Mob):
                # Calcul de la distance entre les centres
                dx = self._x - collision._x
                dy = self._y - collision._y
                distance = math.sqrt(dx * dx + dy * dy)
                print("Un message de test qui va tout faire laggé car les print c'est de la merde")
                # La distance désirée pour que les mobs soient juste en contact
                desired_distance = self.hitbox_radius + collision.hitbox_radius
                if distance > 0 and distance < desired_distance:
                    # Calcul de la correction à appliquer
                    overlap = desired_distance - distance
                    # Calcul du vecteur unitaire allant de collision vers self
                    norm_dx = dx / distance
                    norm_dy = dy / distance
                    # Option 1 : Ajuster uniquement la position du mob courant
                    self._x += norm_dx * overlap
                    self._y += norm_dy * overlap

                    # Option 2 (alternative) : Partager la correction entre les deux mobs
                    # self._x += norm_dx * (overlap / 2)
                    # self._y += norm_dy * (overlap / 2)
                    # collision._x -= norm_dx * (overlap / 2)
                    # collision._y -= norm_dy * (overlap / 2)
            # On laisse la gestion des collisions avec le Player (si nécessaire)
            elif isinstance(collision, Player):
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
