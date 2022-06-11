from datetime import datetime  # TODO: remove this
from typing import Any, Dict, Optional

from game_essentails.data.models.effect import EffectData
from pygame.sprite import Sprite


class Effect(EffectData):
    def __init__(self, effect_data: EffectData, owner_rect: Optional[Sprite] = None):
        super().__init__(
            **self.__getParamsForInit(effect_data)
        )

        self._owner_sprite: Optional[Sprite] = owner_rect

    def __getParamsForInit(self, effect_data: EffectData) -> Dict[str, Any]: # copy constructor?
        result: Dict[str, Any] = dict()

        for f_name, f_value in self.__dataclass_fields__.items():
            if hasattr(f_value, "init") and getattr(f_value, "init"):
                result[f_name] = effect_data.__dict__[f_name]

        return result

    def hasReachedEnd(self) -> bool:
        return self.base >= self.max

    def regen(self) -> None:
        super().regen()
        
        if self.perTick is not None:
            # print("perTick")
            pass

        if self.hasReachedEnd():
            # self.effect.end(on = self.entity_that_has_been_cast_on)
            print(datetime.now())

    @property
    def owner_sprite(self) -> Sprite:
        if self._owner_sprite is None: raise ValueError("owner_rect hasn't been set yet!")

        return self._owner_sprite

    @owner_sprite.setter
    def owner_sprite(self, sprite: Optional[Sprite]) -> None:
        self._owner_sprite = sprite

class Curse(Effect):...
class NormalEffect(Effect):...
