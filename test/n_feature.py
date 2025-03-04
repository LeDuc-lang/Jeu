import pyxel

from weapons.guns import Rifle

pyxel.init(256, 256)
pyxel.load("../rsc/3.pyxres")
from utils.sprite import Sprites, Sprite
from utils.timer import Timer

rotation = 0
spr = Sprites([Sprite(0, 24, 16, 16), Sprite(16, 24, 16, 16)])
flip_u = Timer(180)

def draw():
    pyxel.cls(0)
    spr.draw(34,34)
    pyxel.blt(80, 80, 0, 0, 24, 16, 16, 5)
    pyxel.blt(128, 128, 0, 0, 24, 16, 16, 5, rotate=rotation)

def update():
    global rotation
    spr.next()
    if flip_u.event():
        spr.flip_east()
        print("FLIIP")
    rotation = rotation + 15
    spr.rotate(rotation)
    rotation %= 360
    Timer.time_update()

pyxel.run(update, draw)