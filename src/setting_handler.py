# game setup
WIDTH    = 1280    
HEIGTH   = 720
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0
}

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = './graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'


#region additional
from enum import Enum
from typing import Dict
from pathlib import Path

from player import Player
from game_essentails.level_handling.resource_loader import SettingLoader


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