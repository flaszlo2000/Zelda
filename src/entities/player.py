from pathlib import Path
from typing import List, Optional, Tuple, cast

from game_essentails.data.models.player import PlayerData
from game_essentails.sprite_groups import SpriteGroups
from pygame.sprite import Group
from scripts.image_provider import image_provider
from setting_handler import setting_loader

from .base_entity import LivingEntity


class Player(LivingEntity):
    __sprite_name__ = "player"

    def __init__(self, sprite_groups: SpriteGroups, position: Tuple[int, int], stats: Optional[PlayerData] = None):
        player_image = image_provider.provideWithAlphaConvert(Path("./graphics/monsters/spirit/idle/0.png")) # FIXME: change png
        super().__init__(sprite_groups, position, player_image)        

        self._exp = 0
        if stats is None:
            self._stats: PlayerData = cast(PlayerData, setting_loader["players"][0]) #! FIMXE: add character choosing option
        else:
            self._stats = stats

        self.changeInflateX(-6) # in the original code, this was used for some reason so I stay with it
        self.setPlayer(True) # FIXME: this is only for testing purposes

    def getRelatedGroups(self, sprite_groups: SpriteGroups) -> List[Group]:
        groups: List[Group] = [sprite_groups.visible_sprites]

        return groups

    @property
    def stats(self) -> PlayerData:
        return self._stats
    
    @property
    def exp(self) -> int:
        return self._exp

    def testOuter(self) -> None:
        #! FIXME: remove this, this is only a placeholder to test
        self._exp += 20
