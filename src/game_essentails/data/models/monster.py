from dataclasses import dataclass, field
from pathlib import Path

from .base import GameData
from .graphics_base import GraphicsFolder, obtain_folder_content


@dataclass
class MonsterData(GameData):
    # basic stats
    health: int
    damage: int
    resistance: int
    speed: int

    # attack related stats
    exp: int
    attack_type: str
    attack_radius: int

    # ai
    notice_radius: int

    # source related infos
    attack_sound_src: str
    graphics_folder_src: str
    graphics_folder: GraphicsFolder = field(init = False)

    def __post_init__(self):
        self.graphics_folder = obtain_folder_content(Path(self.graphics_folder_src))
