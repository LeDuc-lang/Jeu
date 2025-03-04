import pyxel
from utils.timer import Timer

pyxel.init(160, 120, fps=60)

timer = Timer(180)
event_c = 0

def update():
    global event_c
    Timer.time_update()
    if timer.event():
        event_c += 1

def draw():
    pyxel.cls(0)
    pyxel.text(60, 60, str(timer.event()), 3)
    pyxel.text(100, 60, str(timer.frame), 6)
    pyxel.text(120, 60, str(timer.time), 8)
    pyxel.text(120, 30, str(event_c), 8)

pyxel.run(update, draw)