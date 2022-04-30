from typing import List

from pygame.sprite import Group

from ..sprite_groups import SpriteGroups
from .base_tile import ObjectTile


class RealObjectTile(ObjectTile):
    def getRelatedGroups(self, sprite_groups: SpriteGroups) -> List[Group]:
        groups = [sprite_groups.visible_sprites, sprite_groups.obstacle_sprites]

        return groups
