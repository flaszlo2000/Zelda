from dataclasses import dataclass, field
from typing import Union

from . base import GameData


@dataclass
class CommonConfData(GameData):
    value: Union[str, int]
    is_numeric: bool = field(default = False)