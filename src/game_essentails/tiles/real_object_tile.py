from . base_tile import ObjectTile
from .. sprite_groups import SpriteGroups


class RealObjectTile(ObjectTile):
    def getRelatedGroups(self, sprite_groups: SpriteGroups) -> list:
        groups = [sprite_groups.visible_sprites, sprite_groups.obstacle_sprites]

        return groups