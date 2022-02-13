from . base_tile import NormalTile
from .. sprite_groups import SpriteGroups


class GrassTile(NormalTile):
    __sprite_name__ = "grass"

    def getRelatedGroups(self, sprite_groups: SpriteGroups) -> list:
        groups = [sprite_groups.visible_sprites, sprite_groups.obstacle_sprites, sprite_groups.attackable_sprites]

        return groups