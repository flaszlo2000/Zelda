from typing import Dict

import pygame
from pygame.rect import Rect


class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction: str = player.status.split('_')[0]

        # graphic
        full_path = f'../graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        

        strategy: Dict[str, Rect] = {
            "right": self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16)),
            "left": self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16)),
            "down": self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0)),
            "up": self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))
        }

        self.rect = strategy[direction]

        # # placement
        # if direction == 'right':
        #     self.rect = 
        # elif direction == 'left': 
        #     self.rect = 
        # elif direction == 'down':
        #     self.rect = 
        # else:
        #     self.rect = 
