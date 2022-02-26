from dataclasses import dataclass
from typing import Any

from . base import GameData


@dataclass
class CommonConfData(GameData):
    value: Any