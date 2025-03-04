from utils.sprite import Sprite, Sprites

player_sprite_1 = Sprite(0, 24, 16, 16)
player_sprite_2 = Sprite(16, 24, 16, 16)
player_sprites = Sprites([player_sprite_1, player_sprite_2])
# self.sprites = Sprites([Sprite(0, 24, 16, 16), Sprite(16, 24, 16, 16)])

mob_sprite_1 = Sprite(16, 120, 16, 16)
mob_sprite_2 = Sprite(0, 120, 16, 16)
mob_sprites = Sprites([mob_sprite_1, mob_sprite_2])

simple_shoot_effect = Sprites([Sprite(n, 16, 8, 8) for n in range(32, 57, 8)])

# sprites= Sprites([Sprite(16, 120, 16, 16), Sprite(0, 120, 16, 16)])