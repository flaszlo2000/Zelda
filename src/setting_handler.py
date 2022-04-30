from enum import Enum
from pathlib import Path
from typing import Any

from game_essentails.level_handling.resource_loader import SettingLoader


#region testing stuff
class TileIdEnum(Enum):
    EMPTY = "-1"


    GRASS1 = 8
    GRASS2 = 9
    GRASS3 = 10


    PLAYER = 394


#endregion

def get_common_setting(needed_setting_name: str) -> Any:
    return setting_loader.getSingleValueFrom("common", needed_setting_name)

if __name__ != "__main__":
    setting_loader = SettingLoader(Path("./settings"))
    setting_loader.importSettings()
