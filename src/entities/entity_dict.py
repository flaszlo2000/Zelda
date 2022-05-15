from typing import Dict, Type

from .base_entity import LivingEntity
from .enemies.bamboo import Bamboo
from .enemies.racoon import Racoon
from .enemies.spirit import Spirit
from .enemies.squid import Squid
from .player import Player

ENTITY_DICT: Dict[str, Type[LivingEntity]] = {
    # "-1": None,

    "390": Bamboo,
    "391": Spirit,
    "392": Racoon,
    "393": Squid,
    "394": Player
}
