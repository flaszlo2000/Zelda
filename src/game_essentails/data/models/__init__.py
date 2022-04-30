from typing import Dict, Type

from .base import GameData
from .common_conf import CommonConfData
from .hitbox_offset import HitboxOffset
from .magic_data import MagicData
from .monster import MonsterData
from .player import PlayerData
from .weapon import WeaponData

# during the setting loading phase this global is used to find out which dataclass can represent a data file
HANDLER_MAP: Dict[str, Type[GameData]] = {
    "monsters": MonsterData,
    "weapons": WeaponData,
    "magic": MagicData,
    "common": CommonConfData,
    "hitbox_offset": HitboxOffset,
    "players": PlayerData,
}
