from pygame.sprite import Sprite
from pygame import Surface
from abc import ABC, abstractmethod
from typing import List

from game_essentails.sprite_groups import SpriteGroups
from game_essentails.data.models.hitbox_offset import HitboxOffset
from setting_handler import setting_loader


class AbstractBaseTile(Sprite, ABC):
    """This class is the base of all game objects (Objects, Player, etc) which has to inherit from Sprite and has a hitbox"""
    def __init__(self, sprite_groups: SpriteGroups, _position: List[int], image_surface: Surface):
        super().__init__(self.getRelatedGroups(sprite_groups))

        tile_size = setting_loader.getSingleValueFrom("common", "tile_size")
        self.position = [position * tile_size for position in _position]
        self.image = image_surface

    @abstractmethod
    def getRelatedGroups(self, sprite_groups: object) -> list:... # FIXME: type hint

    @staticmethod
    def findHitboxOffset(__sprite_name: str) -> int:
        hitbox_offsets: List[HitboxOffset] = setting_loader["hitbox_offset"]

        for hitbox_offset in hitbox_offsets:
            if hitbox_offset.name == __sprite_name:
                return hitbox_offset.value
        else:
            raise KeyError(f"couldn't find hitbox for *{__sprite_name}*")

    def setHitbox(self, x_offset: int = 0) -> None:
        if hasattr(self, "rect") and hasattr(self, "__sprite_name__"):
            y_offset = AbstractBaseTile.findHitboxOffset(self.__sprite_name__)
            self.hitbox = self.rect.inflate(x_offset, y_offset)
        else:
            raise ValueError("self.rect or __sprite_name__ is missing!")

    def changeInflateX(self, new_x_offset: int = 0) -> None:
        # This method is needed because some child class might have different x offsets
        self.setHitbox(new_x_offset)