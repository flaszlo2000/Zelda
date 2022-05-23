from dataclasses import dataclass, field
from typing import List

from scripts.dataclass_typeconvert import type_check

from .base import GameData
from .stat import StatData


@dataclass
class PlayerData(GameData):
    attack_cooldown: int
    switch_duration_cooldown: int

    health: StatData
    energy: StatData
    attack: StatData
    magic: StatData
    speed: StatData

    __stat_count: int = field(default = 0) #! TODO: remove this after, fixin Upgrade  

    # list to make easier real stat existance checking
    __stat_key_list: List[str] = field(default_factory = list, init = False)

    @type_check
    def __post_init__(self) -> None:
        for param, value in self.__dict__.items():
            if isinstance(value, StatData):
                self.__stat_count += 1
                self.__stat_key_list.append(param)

        # some stat can have dependency, provide them       
        stats_with_dependency = filter(lambda stat: stat.depends_on, self.getRegenerableStats())
        for stat_with_dependency in stats_with_dependency:
            for dependency in stat_with_dependency.depends_on:
                stat_with_dependency.updateRegenAmount(self.getStat(dependency))

    @property
    def stat_count(self) -> int:
        return self.__stat_count

    def getStat(self, stat_name: str) -> StatData:
        "Search for only StatData and returns it"
        if stat_name not in self.__stat_key_list:
            error_msg = f"The given *{stat_name}* stat was not found!"
            if stat_name in self.__dict__:
                error_msg = f"The given *{stat_name}* stat was found, but it is not real StatData!"

            raise AttributeError(error_msg)
        
        return self.__dict__[stat_name]

    def getRealStats(self) -> List[StatData]:
        return [self.__dict__[stat_name] for stat_name in self.__stat_key_list]

    def getRegenerableStats(self) -> List[StatData]:
        return list(filter(lambda stat: stat.can_be_regened, self.getRealStats()))
