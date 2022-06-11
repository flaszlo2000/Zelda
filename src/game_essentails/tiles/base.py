from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, cast

from game_essentails.data.models.effect import EffectData
from game_essentails.data.models.hitbox_offset import HitboxOffset
from game_essentails.effect.effects import Effect
from game_essentails.effect.handler import EffectHandler
from game_essentails.effect.main import EffectAdapter
from game_essentails.sprite_groups import SpriteGroups
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from setting_handler import setting_loader


class AbstractBaseTile(Sprite, ABC):
    """This class is the base of all game objects (Objects, Player, etc) which has to inherit from Sprite and has a hitbox"""
    def __init__(
        self,
        sprite_groups: SpriteGroups,
        _position: Tuple[int, int],
        image_surface: Surface,
        effect_handler: Optional[EffectHandler] = None
    ):
        super().__init__(self.getRelatedGroups(sprite_groups)) # type: ignore # pygame error

        tile_size = setting_loader.getSingleValueFrom("common", "tile_size")
        self.position = [position * tile_size for position in _position] # FIXME: is this used?

        # every child of this class is able to get affected by effects
        self.effect_handler = EffectHandler() if effect_handler is None else effect_handler

        # Fix mypy dataclass and abc issue
        self.image: Surface = image_surface
        self.__post_init__()

    @abstractmethod
    def __post_init__(self) -> None:...

    @abstractmethod
    def getRelatedGroups(self, sprite_groups: SpriteGroups) -> List[Group]:...

    @staticmethod
    def findHitboxOffset(__sprite_name: str) -> int:
        # NOTE: List[GameData] is coming back from setting_loader.__getitem__ 
        # but I am sure i can cast it into HitboxOffset
        hitbox_offsets: List[HitboxOffset] = cast(List[HitboxOffset], setting_loader["hitbox_offset"])

        for hitbox_offset in hitbox_offsets:
            if hitbox_offset.name == __sprite_name:
                return hitbox_offset.value
        else:
            raise KeyError(f"couldn't find hitbox for *{__sprite_name}*")

    def setHitbox(self, x_offset: int = 0) -> None:
        if not hasattr(self, "rect") or not hasattr(self, "__sprite_name__"):
            # NOTE: all of the subclasses has to implements these!
            raise ValueError("self.rect or __sprite_name__ is missing!")

        y_offset = AbstractBaseTile.findHitboxOffset(self.__sprite_name__) # type: ignore
        self.hitbox: Rect = self.rect.inflate(x_offset, y_offset) # type: ignore
    
    def changeInflateX(self, new_x_offset: int = 0) -> None:
        # This method is needed because some child class might have different x offsets
        self.setHitbox(new_x_offset)

    def moveTo(self, x: int, y: int):
        if self.rect is None: raise ValueError(f"Unsuccessful move, rect is None at {self}")

        self.rect.left = x
        self.rect.top = y
        self.position = [x, y]
        self.setHitbox()

    def update(self, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        self.effect_handler.update(*args, **kwargs)

    def _getEffectForCast(self, effect_data: EffectData) -> Effect:
        effect : Effect = EffectAdapter.convert(effect_data)
        effect.owner_sprite = self

        return effect

    def castEffectOn(self, effect_data: EffectData) -> None:
        self.effect_handler += self._getEffectForCast(effect_data)
