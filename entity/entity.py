import math

import game_state as gs
from utils.my_quadtree import Rect, Point


class Entity(Point):
    def __init__(self, x: int, y: int, speed: int, hitbox_radius=8):
        super().__init__(x, y)
        self.hitbox_radius = hitbox_radius
        self.speed = speed
        self.alive = True

    def collide(self, entity):
        """
        Determine if a given entity collides with the current object.

        This method calculates the distance between the current object and
        the specified entity. If the distance is less than or equal to
        the hitbox radius of the current object, the two entities are considered
        to have collided.

        :param entity: An object representing another entity to check collision with.
            The entity must have properties or methods that allow for calculation
            of distance relative to the current object.
        :return: A boolean indicating whether a collision has occurred.
        :rtype: bool
        """
        return self.distance_to(entity) <= self.hitbox_radius

    def collisions(self) -> list:
        """Renvoie une liste d'entités qui entrent en collision avec le rectangle donné."""

        x_research_area = self.hitbox_radius - self.hitbox_radius * 2
        y_research_area = self.hitbox_radius - self.hitbox_radius * 2
        width_research_area = self._x + self.hitbox_radius * 5
        height_research_area = self._y + self.hitbox_radius * 5
        research_area = Rect(x_research_area, y_research_area, width_research_area, height_research_area)

        entity_list = gs.map.query_circle(research_area, self, self.hitbox_radius, [])
        return [entity for entity in entity_list if entity is not self and self.collide(entity)]

    def _bounce_adjust_collision(self, vector, collision, bounce_factor=1.0):
        """
        Ajuste le vecteur de mouvement pour simuler un rebond en cas de collision.
        Ajoute une étape pour repositionner l'entité en dehors de la zone de collision.

        Args:
            vector (tuple): Le vecteur de mouvement initial (vx, vy).
            collision (Point): La position du point de collision.
            bounce_factor (float): Facteur de rebond (1.0 = rebond parfaitement élastique, <1.0 = amorti).

        Returns:
            tuple: Un nouveau vecteur (vx, vy) ajusté pour simuler le rebond.
        """
        # Décomposer le vecteur de mouvement
        vx, vy = vector

        # Calculer le vecteur normal (entité -> collision)
        normal_x = self._x - collision._x
        normal_y = self._y - collision._y

        # Calculer la distance et normaliser la normale
        distance = math.sqrt(normal_x ** 2 + normal_y ** 2)
        if distance == 0:
            # Cas limite : collision au même point
            return -vx * bounce_factor, -vy * bounce_factor

        normal_x /= distance
        normal_y /= distance

        # Repositionner l'entité en dehors de la zone de collision
        overlap = self.hitbox_radius + collision.hitbox_radius - distance
        if overlap > 0:
            self._x += normal_x * overlap
            self._y += normal_y * overlap

        # Produit scalaire entre le vecteur de mouvement et la normale
        dot_product = vx * normal_x + vy * normal_y

        # Calculer le vecteur réfléchi : R = V - 2 * (V . N) * N
        reflected_vx = vx - 2 * dot_product * normal_x
        reflected_vy = vy - 2 * dot_product * normal_y

        # Appliquer le facteur de rebond
        reflected_vx *= bounce_factor
        reflected_vy *= bounce_factor

        return reflected_vx, reflected_vy

    def prevent_overlap(self, vector, other):
        """
        Calcule un vecteur ajusté pour éviter le chevauchement.
        - vector : un tuple (vx, vy) représentant le déplacement initial.
        - other : une autre entité.
        Retourne un vecteur ajusté (dx, dy).
        """
        # Simule les nouvelles positions après déplacement
        new_x = self._x + vector[0]
        new_y = self._y + vector[1]

        # Vérifie s'il y a collision après le déplacement
        distance = math.sqrt((new_x - other.x_pos) ** 2 + (new_y - other.y_pos) ** 2)
        min_distance = self.hitbox_radius + other.hitbox_radius

        if distance < min_distance:
            # Calculer le vecteur de correction
            overlap = min_distance - distance
            if distance != 0:  # Éviter une division par zéro
                dx = (new_x - other.x_pos) / distance * overlap
                dy = (new_y - other.y_pos) / distance * overlap
                return vector[0] + dx, vector[1] + dy
            else:
                # Si les entités sont au même endroit
                return vector[0] + self.hitbox_radius, vector[1] + self.hitbox_radius
        else:
            # Pas de collision, retour du vecteur initial
            return vector

    def collisions_handler(self, vector):
        """Ajuste le vecteur de mouvement en fonction des collisions détectées."""
        for collision in self.collisions():
            vector = self.collision_effect(collision, vector)
        return vector

    def collision_effect(self, collision, vector):
        """Applique les effets de collision au vecteur de mouvement."""
        return vector

    def move(self, dx, dy):
        """Déplace l'entité en ajustant pour les collisions."""
        # Ajuster le vecteur de déplacement en fonction des collisions
        vector = (dx, dy)
        vector = self.collisions_handler(vector)
        dx, dy = vector

        self._x += dx
        self._y += dy

    def update(self):
        """Met à jour l'état de l'entité."""
        pass

    def move_to(self, point: Point | tuple):
        """Déplace l'entité vers un point donné en tenant compte des collisions."""
        target_x, target_y = point.x_pos, point.y_pos if isinstance(point, Point) else point

        delta_x = target_x - self._x
        delta_y = target_y - self._y
        distance = self.distance_to(point)

        if distance == 0:
            return

        if distance <= self.speed:
            self.move(delta_x, delta_y)
        else:
            # Normalisation du vecteur de direction
            direction_x = delta_x / distance
            direction_y = delta_y / distance

            # Calcul du mouvement en fonction de la vitesse maximale
            vector_x = direction_x * self.speed
            vector_y = direction_y * self.speed

            self.move(vector_x, vector_y)
        math.ceil(self.x_pos)
        math.ceil(self.y_pos)
