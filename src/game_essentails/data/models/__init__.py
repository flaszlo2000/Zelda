from typing import Dict

from . base import GameData
from . monster import MonsterData
from . weapon import WeaponData 
from . magic_data import MagicData
from . common_conf import CommonConfData


# during the setting loading phase this global is used to find out which dataclass can represent a data file
HANDLER_MAP: Dict[str, GameData] = {
    "monsters": MonsterData,
    "weapons": WeaponData,
    "magic": MagicData,
    "common": CommonConfData,
    "hitbox_offset": None
}