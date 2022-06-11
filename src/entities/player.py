from pathlib import Path
from typing import Any, List, Optional, Tuple, cast

from game_essentails.data.models.player import PlayerData, StatData
from game_essentails.sprite_groups import SpriteGroups
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP
from pygame.key import get_pressed
from pygame.sprite import Group
from scripts.image_provider import image_provider
from setting_handler import setting_loader
from src.game_essentails.data.models.effect import EffectData

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

    def input(self) -> None:
        #  if not self.attacking:
        keys = get_pressed()

        # movement input
        if keys[K_UP]:
            self.direction.y = -1
            # self.status = 'up'
        elif keys[K_DOWN]:
            self.direction.y = 1
            # self.status = 'down'
        else:
            self.direction.y = 0

        if keys[K_RIGHT]:
            self.direction.x = 1
            # self.status = 'right'
        elif keys[K_LEFT]:
            self.direction.x = -1
            # self.status = 'left'
        else:
            self.direction.x = 0

    def regenStats(self) -> None:
        "Regenerate those stats which can be regened"
        for stat in self._stats.getRegenerableStats():
            stat.regen()

    def update(self, *args: List[Any]) -> None:
        super().update(*args)
        # NOTE: called by pygame as a default behaviour because all Sprite has this method
        self.input()
        self.move(self._stats.speed.base)
        self.regenStats()

    def getStat(self, stat: str) -> StatData:
        "Returns a stat of the player"
        return self._stats.getStat(stat)

    def castEffectOn(self, effect_data: EffectData) -> None:
        effect = self._getEffectForCast(effect_data)

        self.effect_handler.add(effect, is_player = True)
