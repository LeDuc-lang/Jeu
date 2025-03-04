import numpy as np
import pyxel


# TO-DO Fix divide limit


class Point:
    """Représente un point en 2D situé aux coordonnées (x, y).

    Un objet Point peut être associé à une charge utile (payload) optionnelle.
    """

    def __init__(self, x: int | float, y: int | float, payload=None):
        self._x, self._y = x, y
        self.payload = payload

    @property
    def x_pos(self):
        return self._x

    @x_pos.setter
    def x_pos(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError("x_pos must be float or int")
        self._x = x

    @property
    def y_pos(self):
        return self._y

    @y_pos.setter
    def y_pos(self, y):
        if not isinstance(y, (int, float)):
            raise ValueError("y_pos must be float or int")
        self._y = y

    def __repr__(self):
        return f"{self._x, self._y}: {repr(self.payload)}"

    def __str__(self):
        return f"{self._x:.2f}, {self._y:.2f}"

    def __eq__(self, other):
        return id(self) == id(other)

    def distance_to(self, other):
        """Calcule la distance entre ce point et un autre point.

        Args:
            other (Point): L'autre point avec lequel calculer la distance.

        Returns:
            float: La distance entre les deux points selon le théorème de Pythagore.
        """
        try:
            other_x, other_y = other._x, other._y
        except AttributeError:
            other_x, other_y = other
        return np.hypot(self._x - other_x, self._y - other_y)


class Rect:
    hauteur_ = """Représente un rectangle avec une position centrale (x, y), une largeur et une hauteur."""

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._w = width
        self._h = height
        self.w_edge, self.e_edge = x, x + width  # west edge and east edge
        self.n_edge, self.s_edge = y, y + height  # north edge and south edge

    @property
    def x_pos(self):
        return self._x

    @x_pos.setter
    def x_pos(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError("x_pos must be float or int")
        self._x = x
        self._update_edges()

    @property
    def y_pos(self):
        return self._y

    @y_pos.setter
    def y_pos(self, y):
        if not isinstance(y, (int, float)):
            raise TypeError("y_pos must be float or int")
        self._y = y
        self._update_edges()

    @property
    def width(self):
        return self._w

    @width.setter
    def width(self, width):
        if not isinstance(width, (int, float)):
            raise TypeError("width must be float or int")
        self._w = width
        self._update_edges()

    @property
    def height(self):
        return self._h

    @height.setter
    def height(self, height):
        if not isinstance(height, (int, float)):
            raise TypeError("height must be float or int")
        self._h = height
        self._update_edges()

    def _update_edges(self):
        """Mise à jour des bords du rectangle en fonction de la position et des dimensions."""
        self.w_edge, self.e_edge = self._x, self._x + self._w  # Bords ouest et est
        self.n_edge, self.s_edge = self._y, self._y + self._h  # Bords nord et sud

    def __repr__(self):
        return str((self.w_edge, self.e_edge, self.n_edge, self.s_edge))

    def __str__(self):
        return f"({self.w_edge:.2f}, {self.n_edge:.2f}, {self.e_edge:.2f}, \
            {self.s_edge:.2f})"

    def contains(self, point: Point) -> bool:
        """Vérifie si un point (objet Point ou tuple (x, y)) est à l'intérieur du rectangle.

        Args:
            point (Point or tuple): Un point sous la forme d'un objet Point ou d'un tuple (x, y).

        Returns:
            bool: True si le point est dans le rectangle, sinon False.
        """

        if not isinstance(point, Point):
            raise TypeError("point must be Point or tuple")

        try:
            point_x, point_y = point.x_pos, point.y_pos
        except AttributeError:
            point_x, point_y = point

        return (
                self.w_edge <= point_x < self.e_edge
                and self.n_edge <= point_y < self.s_edge
        )

    def intersects(self, other_rect) -> bool:
        """Vérifie si un autre rectangle intersecte ce rectangle.

        Args:
            other_rect (Rect): L'autre rectangle à vérifier.

        Returns:
            bool: True si les rectangles se chevauchent, sinon False.
        """
        if not isinstance(other_rect, Rect):
            raise TypeError("other must be Rect")

        return not (
                other_rect.w_edge > self.e_edge
                or other_rect.e_edge < self.w_edge
                or other_rect.n_edge > self.s_edge
                or other_rect.s_edge < self.n_edge
        )

    def draw(self, drawfunc=None):
        """Dessine le contour du rectangle.

        Args:
            drawfunc (callable, optional): Une fonction de dessin personnalisée.
            Si aucune fonction n'est fournie, pyxel.rectb est utilisée.
        """
        if drawfunc is not None:
            drawfunc(self._x, self._y, self._w, self._h)
        else:
            pyxel.rectb(self._x, self._y, self._w, self._h, 6)


class QuadTree:
    """Implémente une structure de quadtree pour diviser l'espace en sous-régions."""

    max_points = 4
    max_depth = 8

    def __init__(self, boundary: Rect, depth=0, max_points=4, max_depth=8) -> None:
        """Initialise un nœud de quadtree.

        Args :
            boundary (Rect): Le rectangle qui délimite la région du nœud.
            max_points (int, optional): Le nombre maximum de points avant de diviser le nœud.
                Par défaut, 4.
            depth (int, optional): La profondeur actuelle du nœud dans l'arbre. Par défaut, 0.
        """
        self.boundary = boundary
        self.points = []
        self.depth = depth
        self.divided = False
        self.max_points = max_points
        self.max_depth = max_depth

    def remove(self, point: Point):
        """Supprime un point du quadtree récursivement.

        Args:
            point (Point): Le point à supprimer du quadtree.
        """
        if not self.boundary.contains(point):
            return  # Si le point est en dehors de la zone du rectangle de ce noeud, on ne fait rien.

        # Suppression dans les sous-quadrants si l'arbre est divisé
        if self.divided:
            self.nw.remove(point)
            self.ne.remove(point)
            self.sw.remove(point)
            self.se.remove(point)

        # Suppression du point dans le nœud actuel si le point est trouvé
        if point in self.points:
            self.points.remove(point)

        # Si le nœud contient moins de points que le maximum autorisé, on peut le fusionner
        if not self.divided and len(self.points) < self.max_points:
            self.divided = False  # Fusionner ce nœud avec ses enfants s'il y en avait
            self.clear_empty_subtrees()

    def clear_empty_subtrees(self):
        """Supprime les sous-arbres vides pour éviter les nœuds inutiles."""
        if self.divided:
            if len(self.nw.points) == 0 and len(self.ne.points) == 0 and len(self.sw.points) == 0 and len(
                    self.se.points) == 0:
                self.divided = False
                self.nw = self.ne = self.sw = self.se = None


    def __str__(self):
        """Retourne une représentation textuelle de ce nœud et ses points."""
        sp = " " * self.depth * 2
        s = str(self.boundary) + "\n"
        s += sp + ", ".join(str(point) for point in self.points)
        if not self.divided:
            return s
        return f'\n\nQuadtree level : {self.depth} \n {str(self.boundary)}\nNw : \n{str(self.nw)}\nNe: \n{str(self.ne)}\nSe : \n{str(self.se)}\nSw :  \n{str(self.sw)}'

    def draw(self):
        """Dessine les contours du quadtree et de ses nœuds."""
        if self.divided:
            self.nw.draw()
            self.ne.draw()
            self.sw.draw()
            self.se.draw()
        else:
            self.boundary.draw()

    def _subqtree(self, boundary):
        return QuadTree(boundary, depth=self.depth + 1)

    def divide(self):
        """Divise le quadtree en quatre sous-nœuds."""
        cx, cy = self.boundary._x, self.boundary._y
        w, h = self.boundary._w / 2, self.boundary._h / 2

        self.nw = self._subqtree(Rect(cx, cy, w, h))
        self.ne = self._subqtree(Rect(cx + w, cy, w, h))
        self.sw = self._subqtree(Rect(cx, cy + h, w, h))
        self.se = self._subqtree(Rect(cx + w, cy + h, w, h))

        self.divided = True

    def insert(self, point: Point):
        """Insère un point dans le quadtree."""
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.max_points and not self.divided:
            self.points.append(point)
            return True

        if not self.divided:
            self.divide()

        if (
                self.ne.insert(point)
                or self.nw.insert(point)
                or self.se.insert(point)
                or self.sw.insert(point)
        ):
            return True

        return False

    def clear(self):
        """Vide tous les points du quadtree, y compris des sous-nœuds."""
        self.points = []
        if self.divided:
            self.nw.clear()
            self.ne.clear()
            self.sw.clear()
            self.se.clear()

    def collect_points(self):
        """Récupère tous les points du quadtree récursivement."""
        if not self.divided:
            # Retourne les points du nœud courant s'il n'est pas divisé
            return self.points
        else:
            # Récupère les points de tous les sous-nœuds
            return (
                    self.points
                    + self.nw.collect_points()
                    + self.ne.collect_points()
                    + self.sw.collect_points()
                    + self.se.collect_points()
            )

    def update(self):
        """Mise à jour des points dans le quadtree."""
        # Récupère tous les points de l'arbre
        all_points = self.collect_points()

        # Réinitialise le quadtree en supprimant tous les points et en réinitialisant les sous-nœuds
        self.clear()
        self.divided = False

        # Réinsère tous les points dans le quadtree
        for point in all_points:
            self.insert(point)

    def query(self, boundary, found_points):
        """Trouve tous les points du quadtree qui se trouvent dans une région donnée.

        Args:
            boundary (Rect): La région à interroger.
            found_points (list): La liste dans laquelle stocker les points trouvés.

        Returns:
            list: La liste des points qui se trouvent dans la région spécifiée.
        """
        if not self.boundary.intersects(boundary):
            return found_points

        for point in self.points:
            if boundary.contains(point):
                found_points.append(point)

        if self.divided:
             self.nw.query(boundary, found_points)
             self.ne.query(boundary, found_points)
             self.se.query(boundary, found_points)
             self.sw.query(boundary, found_points)
        return found_points

    def query_circle(self, boundary, centre, radius, found_points):
        """Trouve tous les points du quadtree qui se trouvent à l'intérieur d'un cercle donné.

        Args:
            boundary (Rect): Le rectangle qui entoure le cercle de recherche.
            centre (Point): Le centre du cercle.
            radius (float): Le rayon du cercle.
            found_points (list): La liste dans laquelle stocker les points trouvés.

        Returns:
            list: La liste des points qui se trouvent dans le cercle spécifié.
        """
        if not self.boundary.intersects(boundary):
            return found_points

        for point in self.points:
            if boundary.contains(point) and point.distance_to(centre) <= radius:
                found_points.append(point)

        if self.divided:
            self.nw.query_circle(boundary, centre, radius, found_points)
            self.ne.query_circle(boundary, centre, radius, found_points)
            self.se.query_circle(boundary, centre, radius, found_points)
            self.sw.query_circle(boundary, centre, radius, found_points)
        return found_points

    def query_radius(self, centre, radius, found_points):
        """Trouve tous les points du quadtree dans un rayon autour d'un centre donné.

        Args:
            centre (Point): Le centre du cercle de recherche.
            radius (float): Le rayon autour du centre pour la recherche.
            found_points (list): La liste dans laquelle stocker les points trouvés.

        Returns:
            list: La liste des points qui se trouvent dans le cercle spécifié.
        """
        boundary = Rect(*centre, 2 * radius, 2 * radius)
        return self.query_circle(boundary, centre, radius, found_points)

    def __len__(self):
        """Retourne le nombre total de points dans l'arbre."""
        # Comptons d'abord les points dans le nœud courant
        total_points = len(self.points)

        # Si ce nœud est divisé, il faut ajouter les points des sous-nœuds
        if self.divided:
            total_points += len(self.nw)
            total_points += len(self.ne)
            total_points += len(self.sw)
            total_points += len(self.se)

        return total_points


def _expand_quadtree(qd: QuadTree, region: Rect, as_which: str):
    """Helper function to expand the QuadTree and assign the old one to the specified quadrant"""
    n_QuadTree = QuadTree(region, depth=qd.depth - 1)
    n_QuadTree.divide()
    setattr(n_QuadTree, as_which, qd)
    return n_QuadTree


def dynamic_update(qd: QuadTree, points: list[Point]):
    """Update a QuadTree to permit a self-upgrade to cover a bigger region"""
    for point in points:
        px, py = point.x_pos, point.y_pos
        x, y = qd.boundary.x_pos, qd.boundary.y_pos
        cx, cy = x + qd.boundary.width, y + qd.boundary.height

        extended_regions = {
            'se': Rect(x, y, qd.boundary.width * 2, qd.boundary.height * 2),
            'sw': Rect(x - qd.boundary.width, y, qd.boundary.width * 2, qd.boundary.height * 2),
            'ne': Rect(x, y - qd.boundary.height, qd.boundary.width * 2, qd.boundary.height * 2),
            'nw': Rect(x - qd.boundary.width, y - qd.boundary.height, qd.boundary.width * 2, qd.boundary.height * 2)
        }

        if not qd.boundary.contains(point):
            if extended_regions['nw'].contains(point):
                qd = _expand_quadtree(qd, extended_regions['nw'], 'se')
                continue
            if extended_regions['se'].contains(point):
                qd = _expand_quadtree(qd, extended_regions['se'], 'nw')
                continue
            if extended_regions['sw'].contains(point):
                qd = _expand_quadtree(qd, extended_regions['sw'], 'ne')
                continue
            if extended_regions['ne'].contains(point):
                qd = _expand_quadtree(qd, extended_regions['ne'], 'sw')
                continue

    qd.update()
    return qd
