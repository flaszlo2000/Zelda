from dataclasses import dataclass, field
from typing import List

@dataclass
class BaseTile:
    position: List[int] = field(default_factory=[0, 0])

    def getResolutionBySize(self, size: int) -> List[int]:
        return [elem*size for elem in self.position]


# class 


from enum import IntEnum

class TileIdEnum(IntEnum):
    EMPTY = -1


    GRASS1 = 8
    GRASS2 = 9
    GRASS3 = 10