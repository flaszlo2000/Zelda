from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GameData:
    name: str
    graphics_src: Optional[str] = field(default = None, init = False)