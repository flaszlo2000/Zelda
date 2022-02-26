from typing import Tuple
from pathlib import Path

from . base_entity import LivingEntity
from game_essentails.sprite_groups import SpriteGroups
from scripts.image_provider import image_provider


class Player(LivingEntity):
    __sprite_name__ = "player"

    def __init__(self, sprite_groups: SpriteGroups, position: Tuple[int, int]):
        player_image = image_provider.provideWithAlphaConvert(Path("./graphics/monsters/spirit/idle/0.png")) # FIXME: change png
        super().__init__(sprite_groups, position, player_image)        

        self.changeInflateX(-6) # in the original code, this was used for some reason so I stay with it
        self.setPlayer(False) # FIXME: this is only for testing purposes
    
    def getRelatedGroups(self, sprite_groups: SpriteGroups) -> list:
        groups = [sprite_groups.visible_sprites]

        return groups