from . base_tile import NormalTile
from .. sprite_groups import SpriteGroups

class BoundaryTile(NormalTile):
    __sprite_name__ = "invisible"

    def getRelatedGroups(self, sprite_groups: SpriteGroups) -> list:
        groups = [sprite_groups.obstacle_sprites]

        return groups
