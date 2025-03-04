from typing import Tuple

import pyxel
import game_state as gs
import utils.screen_tools as st
import gui.nice_font
from gui.nice_font import nice_font_number


def show():
    mag_display()
    xp_bar(37, (25, 100))

def mag_display():
    mag = gs.player.weapon.magazine
    cap = gs.player.weapon.capacity

    padding_x = len(f'{mag}/{cap}')*37

    bottom_corner_x = gs.player.x_pos + (gs.SCREEN_CENTER[0]) - padding_x
    bottom_corner_y = gs.player.y_pos + (gs.SCREEN_CENTER[1]) - 48

    # pyxel.text(gs.player.x_pos - 6, gs.player.y_pos - 15 , f'{mag}/{cap}', 8)
    nice_font_number(bottom_corner_x, bottom_corner_y, f'{mag}/{cap}')

def xp_bar(xp_level, xp: Tuple[int, int]):
    top_corner_x = gs.player.x_pos - (gs.SCREEN_CENTER[0])
    top_corner_y = gs.player.y_pos - (gs.SCREEN_CENTER[1])

    # Dessin du fond de la barre
    pyxel.rect(top_corner_x, top_corner_y, gs.SCREEN_WIDTH, 16, 1)  # Fond de la barre (noir)

    # Calcul du pourcentage d'XP
    current_xp, xp_needed = gs.xp, gs.max_xp
    xp_percentage = current_xp / xp_needed if xp_needed > 0 else 0

    # Dessin de la partie remplie de la barre
    bar_width = gs.SCREEN_WIDTH * xp_percentage
    pyxel.rect(top_corner_x, top_corner_y, bar_width, 16, 8)  # Partie remplie (orange)

    # Contour de la barre
    pyxel.rectb(top_corner_x, top_corner_y, gs.SCREEN_WIDTH, 16, 14)  # Contour (jaune)

    # Affichage du niveau d'XP
    size = len(str(xp_level)) * 37  # Taille de la boîte du niveau
    nice_font_number(gs.player.x_pos - (size / 2), top_corner_y, f'{xp_level}')




