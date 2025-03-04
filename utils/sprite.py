import pyxel

class Sprite:
    colkey = 5

    def __init__(self, u, v, w, h, rotation=0, img=0):
        self._u = u
        self._v = v
        self._w = w
        self._h = h
        self._img = img
        self._rotation = rotation

    def draw(self, x, y):
        pyxel.blt(x, y, self._img, self._u, self._v, self._w, self._h, colkey=self.colkey, rotate=self._rotation)

    def flip_north(self):
        if not self._h < 0:
            self._h *= -1

    def flip_south(self):
        if not self._h > 0:
            self._h *= -1

    def flip_east(self):
        if not self._w < 0:
            self._w *= -1

    def flip_west(self):
        if not self._w > 0:
            self._w *= -1

    def flip(self):
        self._h *= -1
        self._w *= -1

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, angle):
        if not 0 <= angle < 360:
            raise ValueError(f'angle must be between 0 and 360')
        self._rotation = angle

    def rotate(self, angle):
        self._rotation += angle
        self._rotation %= 360


class Sprites:
    def __init__(self, sprites: list[Sprite]):
        self._sprites = sprites
        self.index = 0

    def next(self):
        self.index += 1
        if self.index >= len(self._sprites):
            self.index = 0
            return True

    def back(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self._sprites)
            return True

    def _current_sprite(self):
        return self._sprites[self.index]

    def flip(self):
        for sprite in self._sprites:
            sprite.flip()

    def flip_north(self):
        for sprite in self._sprites:
            sprite.flip_north()

    def flip_south(self):
        for sprite in self._sprites:
            sprite.flip_south()

    def flip_east(self):
        for sprite in self._sprites:
            sprite.flip_east()

    def flip_west(self):
        for sprite in self._sprites:
            sprite.flip_west()

    def rotate(self, angle):
        for sprite in self._sprites:
            sprite.rotate(angle)

    def __getattr__(self, item):
        # Accéder à l'attribut de l'objet courant
        return getattr(self._current_sprite(), item)