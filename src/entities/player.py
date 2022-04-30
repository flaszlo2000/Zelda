from pathlib import Path
from typing import List, Tuple

from game_essentails.sprite_groups import SpriteGroups
from pygame.sprite import Group
from scripts.image_provider import image_provider

from .base_entity import LivingEntity


class Player(LivingEntity):
    __sprite_name__ = "player"

    def __init__(self, sprite_groups: SpriteGroups, position: Tuple[int, int]):
        player_image = image_provider.provideWithAlphaConvert(Path("./graphics/monsters/spirit/idle/0.png")) # FIXME: change png
        super().__init__(sprite_groups, position, player_image)        

        self.changeInflateX(-6) # in the original code, this was used for some reason so I stay with it
        self.setPlayer(False) # FIXME: this is only for testing purposes
    
    def getRelatedGroups(self, sprite_groups: SpriteGroups) -> List[Group]:
        groups: List[Group] = [sprite_groups.visible_sprites]

        return groups
