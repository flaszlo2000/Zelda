from enum import Enum
from typing import Dict
from pathlib import Path

from player import Player
from game_essentails.level_handling.resource_loader import SettingLoader


#region testing stuff
class TileIdEnum(Enum):
    EMPTY = "-1"


    GRASS1 = 8
    GRASS2 = 9
    GRASS3 = 10


    PLAYER = 394

ENTITY_DICT: Dict[str, object] = { # FIXME: type hint
    "-1": None,

    "394": Player
}
#endregion

if __name__ != "__main__":
    setting_loader = SettingLoader(Path("./settings"))
    setting_loader.importSettings()