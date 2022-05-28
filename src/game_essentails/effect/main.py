from typing import Type

from game_essentails.data.models.effect import EffectData

from .effects import Curse, Effect, NormalEffect


class ItIsJustAnAdapter(Exception):...

class EffectAdapter:
    def __init__(self):
        raise ItIsJustAnAdapter("This can't be instantiated!")

    @staticmethod
    def get_appropriate_class(name: str) -> Type[Effect]:
        effect_list = [NormalEffect, Curse]

        return effect_list["curse" in name]

    @classmethod
    def convert(cls, effect_data: EffectData) -> Effect:
        result: Effect = cls.get_appropriate_class(effect_data.name)(effect_data)

        return result
