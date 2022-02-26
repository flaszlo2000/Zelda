from typing import Dict

from . base import GameData
from . monster import MonsterData


# during the setting loading phase this global is used to find out which dataclass can represent a data file
HANDLER_MAP: Dict[str, GameData] = {
    "monsters": MonsterData
}