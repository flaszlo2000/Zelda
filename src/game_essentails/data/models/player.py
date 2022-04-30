from dataclasses import dataclass, field
from typing import Optional

from .base import GameData


@dataclass
class StatData:
    base: int
    max: int
    initial_upgrade_cost: int
    should_be_shown: Optional[bool] = field(default = None)

    def __post_init__(self) -> None:
        self.should_be_shown = self.base == self.max

@dataclass
class PlayerData(GameData):
    attack_cooldown: int
    switch_duration_cooldown: int

    health: StatData
    energy: StatData
    attack: StatData
    magic: StatData
    speed: StatData

    def __post_init__(self) -> None:
        # NOTE: at the loading stage 
        for param, value in self.__dict__.items():
            if isinstance(value, dict):
                self.__dict__[param] = StatData(**value) # type: ignore
