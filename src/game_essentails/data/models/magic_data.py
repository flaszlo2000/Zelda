from dataclasses import dataclass, field
from typing import Optional

from . base import GameData


@dataclass
class MagicData(GameData):
    strength: int
    cost: int
    graphics_src: Optional[str] = field(init = True)