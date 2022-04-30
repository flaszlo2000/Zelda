from dataclasses import dataclass, field

from .base import GameData


@dataclass
class MagicData(GameData):
    strength: int
    cost: int
    graphics_src: str = field(init = True)
