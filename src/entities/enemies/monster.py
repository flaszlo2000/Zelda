
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple, cast

from game_essentails.data.models.monster import MonsterData
from game_essentails.sprite_groups import SpriteGroups
from pygame.sprite import Group
from scripts.image_provider import image_provider
from setting_handler import setting_loader

from ..base_entity import LivingEntity


class SubclassBadConfig(Exception):...

class BaseMonster(LivingEntity, ABC):
    __sprite_name__ = "monster"

    def __init__(self, sprite_groups: SpriteGroups, position: Tuple[int, int]):
        retrieved_settings = list(
            filter(
                lambda monster_data: monster_data.name == self.monster_name(),
                setting_loader["monsters"]
            )
        )

        if not retrieved_settings:
            raise SubclassBadConfig("Subclass provided monster_name but it was not found!")
        if len(retrieved_settings) > 1:
            raise ValueError(f"GameData.name should be unique but multiple was found by this name: {self.monster_name()}")

        self._stats: MonsterData = cast(MonsterData, retrieved_settings[0])

        #! FIXME: remove this and use animations
        if self._stats.graphics_folder.idle is not None:
            placeholder_sprite = self._stats.graphics_folder.idle[0]
        else:
            placeholder_sprite = Path("./graphics/monsters/spirit/idle/0.png")

        super().__init__(
            sprite_groups,
            position,
            image_provider.provideWithAlphaConvert(placeholder_sprite)
        )
    
    @staticmethod
    @abstractmethod
    def monster_name() -> str:...

    def getRelatedGroups(self, sprite_groups: SpriteGroups) -> List[Group]:
        realted_groups = [
            sprite_groups.visible_sprites,
            sprite_groups.attack_sprites
        ]

        return realted_groups
