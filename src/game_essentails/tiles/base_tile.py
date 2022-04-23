from . base import AbstractBaseTile
from setting_handler import setting_loader


class ObjectTile(AbstractBaseTile):
    __sprite_name__ = "object"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tilesize = setting_loader.getSingleValueFrom("common", "tilesize")
        self.rect = self.image.get_rect(topleft = (self.position[0], self.position[1] - tilesize))
        super().setHitbox()

class NormalTile(AbstractBaseTile):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rect = self.image.get_rect(topleft = self.position)
        super().setHitbox()
