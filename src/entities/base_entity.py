from pygame.math import Vector2
from pygame.time import get_ticks
from pygame.surface import Surface
from math import sin
from typing import List
from abc import ABC, abstractmethod

from game_essentails.tiles.base_tile import NormalTile
from game_essentails.sprite_groups import SpriteGroups


class BaseEntity(NormalTile, ABC):
    def __init__(self, sprite_groups: SpriteGroups, _position: List[int], image_surface: Surface):
        super().__init__(sprite_groups, _position, image_surface)
        self._is_player = False

    def setPlayer(self, new_state: bool) -> None:
        self._is_player = new_state

    def isPlayer(self) -> bool:
        return self._is_player

    # FIXME: check speed and direction is needed
    @abstractmethod
    def move(self, speed) -> None:...

    @abstractmethod
    def collision(self, direction: str) -> None:...

class LivingEntity(BaseEntity):
    def __init__(self, sprite_groups: SpriteGroups, _position: List[int], image_surface: Surface):
        super().__init__(sprite_groups, _position, image_surface)

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