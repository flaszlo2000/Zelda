from .base import AbstractBaseTile
from src.settings import TILESIZE, HITBOX_OFFSET


class ObjectTile(AbstractBaseTile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rect = self.image.get_rect(topleft = (self.positionos[0], self.positionpos[1] - TILESIZE))
        super().setHitbox()

class NormalTile(AbstractBaseTile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rect = self.image.get_rect(topleft = self.position)
        super().setHitbox()
