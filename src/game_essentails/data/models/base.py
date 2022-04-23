from dataclasses import dataclass, field
from typing import Optional, List, Any


@dataclass
class GameData:
    name: str
    graphics_src: Optional[str] = field(default = None, init = False)

@dataclass
class SingleValueData(GameData):
    value: Any