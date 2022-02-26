from dataclasses import dataclass, field
from typing import Optional

from . base import GameData


@dataclass
class WeaponData(GameData):
    cooldown: int
    damage: int
    graphics_src: Optional[str] = field(init = True)