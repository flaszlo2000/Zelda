from pygame.sprite import Sprite
from pygame.math import Vector2
from pygame.time import get_ticks
from math import sin


class BaseEntity(Sprite):
    def __init__(self, groups, is_player: bool):
        super().__init__(groups)
        self._is_player = is_player

    def isPlayer(self) -> bool:
        return self._is_player

class Entity(BaseEntity):
    def __init__(self, groups, is_player: bool = False):
        super().__init__(groups, is_player)

        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = Vector2()

    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction: str):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(get_ticks())
        if value >= 0: 
            return 255
        else: 
            return 0