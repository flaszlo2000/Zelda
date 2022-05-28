from datetime import datetime  # TODO: remove this
from typing import Any, Dict

from game_essentails.data.models.effect import EffectData


class Effect(EffectData):
    def __init__(self, effect_data: EffectData):
        super().__init__(
            **self.__getParamsForInit(effect_data)
        )

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
            print("perTick")

        if self.hasReachedEnd():
            # self.effect.end(on = self.entity_that_has_been_cast_on)
            print(datetime.now())

class Curse(Effect):...
class NormalEffect(Effect):...
