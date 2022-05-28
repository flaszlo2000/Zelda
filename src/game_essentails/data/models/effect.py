from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

from game_essentails.data.models.base import GameData
from scripts.dataclass_typeconvert import type_check

from .stat import StatBase


class SupportedToHaveEffect(Enum):
    LIVING_ENTITY = auto()

@dataclass
class EffectDescription:
    on: str
    stat: Optional[str] = field(default = None)
    call: Optional[str]= field(default = None)

@dataclass
class EffectData(StatBase, GameData):
    # inheritance related
    # we use base and max to count time 
    base: int = field(default = 0)
    max: int = field(default = 100)

    can_be_regened: bool = field(default = True) # the main feature of an effect is that it takes time

    # features
    perTick: Optional[EffectDescription] = field(default = None)
    end: Optional[EffectDescription] = field(default = None)
    untilEnd: Optional[EffectDescription] = field(default = None)

    @type_check
    def __post_init__(self):
        StatBase.__post_init__(self)
        if not any([self.perTick, self.end, self.untilEnd]):
            raise ValueError("Every parameter is None, at least one of them should be set!")
