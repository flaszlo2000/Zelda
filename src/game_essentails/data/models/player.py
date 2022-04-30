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
        self.should_be_shown = self.base != self.max

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
        # NOTE: at the data loading stage StatData is parsed as dict so I have to convert it

        print(self.__annotations__)
        for param, value in self.__dict__.items():
            try:
                # we don't want to convert all of the dict like objects, only StatData
                subclass_check = not issubclass(dict, self.__annotations__[param])
            except (TypeError, KeyError):
                # NOTE: issubclass throws "TypeError: Subscripted generics cannot be used with class and instance checks"
                # error if self.__annotations__[param] is a kind of typing type (like Dict[str, str])
                # KeyError could be thrown because of the inheritance
                continue
            else:
                if isinstance(value, dict) and subclass_check:
                    self.__dict__[param] = StatData(**value) # type: ignore
