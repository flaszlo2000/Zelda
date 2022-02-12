from dataclasses import dataclass, field
from typing import List


@dataclass
class BaseTile:
    position: List[int] = field(default=[0, 0])
