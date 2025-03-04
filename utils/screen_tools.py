from math import atan2, pi

import game_state as gs
import pyxel

def on_screen_x(x):
    return x - (gs.player.x_pos - gs.SCREEN_CENTER[0])

def on_screen_y(y):
    return y - (gs.player.y_pos - gs.SCREEN_CENTER[1])

# def get_angle(x1, y1, x2, y2):
#     dx = x1 - x2
#     dy = y1 - y2
#     angle_rad = atan2(dy, dx)
#     if angle_rad < 0:
#         angle_rad += 2 * pi
#     return angle_rad

def normalize_mouse_pos():
    """
    Calcule la position normalisée de la souris en fonction du joueur et du centre de l'écran.

    Returns:
        Point ou tuple: Position normalisée de la souris en tant que Point ou (x, y).
    """
    # Coordonnées du centre de l'écran
    c_x, c_y = gs.SCREEN_CENTER

    # Position normalisée en tenant compte de la position du joueur
    x = pyxel.mouse_x + gs.player.x_pos - (c_x)
    y = pyxel.mouse_y + gs.player.y_pos - (c_y)

    return (x, y)