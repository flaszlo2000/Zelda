from . base import AbstractBaseTile
from settings import TILESIZE


class ObjectTile(AbstractBaseTile):
    __sprite_name__ = "object"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rect = self.image.get_rect(topleft = (self.position[0], self.position[1] - TILESIZE))
        super().setHitbox()

class NormalTile(AbstractBaseTile):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rect = self.image.get_rect(topleft = self.position)
        super().setHitbox()
