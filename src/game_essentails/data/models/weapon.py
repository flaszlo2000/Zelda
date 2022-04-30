from dataclasses import dataclass, field

from .base import GameData


@dataclass
class WeaponData(GameData):
    cooldown: int
    damage: int
    graphics_src: str = field(init = True)
