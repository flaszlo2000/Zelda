from dataclasses import dataclass
from . base import GameData

@dataclass
class WeaponData(GameData):
    cooldown: int
    damage: int
    graphics_src: str