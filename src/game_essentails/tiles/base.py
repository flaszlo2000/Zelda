from pygame.sprite import Sprite
from pygame import Surface
from abc import ABC, abstractmethod
from typing import List

from .. sprite_groups import SpriteGroups
from settings import HITBOX_OFFSET, TILESIZE

class AbstractBaseTile(Sprite, ABC):
    def __init__(self, sprite_groups: SpriteGroups, _position: List[int], image_surface: Surface):
        super().__init__(self.getRelatedGroups(sprite_groups))

        self.position = [position * TILESIZE for position in _position]
        self.image = image_surface

    @abstractmethod
    def getRelatedGroups(self, sprite_groups: object) -> list:... # FIXME: type hint

    def setHitbox(self) -> None:
        if hasattr(self, "rect") and hasattr(self, "__sprite_name__"):
            y_offset = HITBOX_OFFSET[self.__sprite_name__]
            self.hitbox = self.rect.inflate(0, y_offset)
        else:
            raise ValueError("self.rect or __sprite_name__ is missing!")

# NOTE: int list from the csvs

from enum import Enum

class TileIdEnum(Enum):
    EMPTY = "-1"


    GRASS1 = 8
    GRASS2 = 9
    GRASS3 = 10


    PLAYER = 394