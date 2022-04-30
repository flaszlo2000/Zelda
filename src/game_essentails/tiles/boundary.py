from typing import List

from pygame.sprite import Group

from ..sprite_groups import SpriteGroups
from .base_tile import NormalTile


class BoundaryTile(NormalTile):
    __sprite_name__ = "invisible"

    def getRelatedGroups(self, sprite_groups: SpriteGroups) -> List[Group]:
        groups = [sprite_groups.obstacle_sprites]

        return groups
