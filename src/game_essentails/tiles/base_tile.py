from pygame.rect import Rect
from setting_handler import setting_loader

from .base import AbstractBaseTile


class ObjectTile(AbstractBaseTile):
    __sprite_name__ = "object"

    def __post_init__(self):
        tilesize = setting_loader.getSingleValueFrom("common", "tilesize")
        self.rect: Rect = self.image.get_rect(topleft = (self.position[0], self.position[1] - tilesize))
        super().setHitbox()

class NormalTile(AbstractBaseTile):
    """"""
    def __post_init__(self):
        self.rect: Rect = self.image.get_rect(topleft = self.position)
        super().setHitbox()
