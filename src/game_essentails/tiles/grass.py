from typing import List

from pygame.sprite import Group

from ..sprite_groups import SpriteGroups
from .base_tile import NormalTile


class GrassTile(NormalTile):
    __sprite_name__ = "grass"

    def getRelatedGroups(self, sprite_groups: SpriteGroups) -> List[Group]:
        groups = [sprite_groups.visible_sprites, sprite_groups.obstacle_sprites, sprite_groups.attackable_sprites]

        return groups
