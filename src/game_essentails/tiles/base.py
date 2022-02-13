from pygame.sprite import Sprite
from pygame import Surface
from abc import ABC, abstractmethod
from typing import List

from .. sprite_groups import SpriteGroups
from src.settings import HITBOX_OFFSET

class AbstractBaseTile(Sprite, ABC):
    def __init__(self, sprite_groups: SpriteGroups, position: List[int], image_surface: Surface):
        super().__init__(self.getRelatedGroups(sprite_groups))

        self.position = position
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

from enum import IntEnum

class TileIdEnum(IntEnum):
    EMPTY = -1


    GRASS1 = 8
    GRASS2 = 9
    GRASS3 = 10