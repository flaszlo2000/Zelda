from dataclasses import dataclass, field
from typing import List, Optional

from .base import GameData


@dataclass
class StatData:
    base: float
    max: int
    initial_upgrade_cost: int

    can_be_regened: bool = field(default = False)
    regen_rate_in_sec: float = field(default = .5)
    regen_amount_percentage: float = field(default = .01)
    regen_max_percentage: float = field(default=100) # determines how much a stat can be regen automatically
    depends_on: Optional[str] = field(default = None) # specify an other stat which will alter the regen amount

    # non-file related params
    should_be_shown: bool = field(init = False)
    frame_c: int = field(default = 0, init = False)

    def __post_init__(self) -> None:
        self.should_be_shown = self.base != self.max

    def regen(self) -> None:
        if not self.can_be_regened: raise ValueError("This stat can't be regened automatically!")
        if self.base >= (self.max * (self.regen_max_percentage / 100)): return

        self.frame_c += 1
        if self.frame_c >= (60 * self.regen_rate_in_sec): #! FIXME: magic number! should be game fps!
            self.base += (self.max * self.regen_amount_percentage)
            self.frame_c = 0

    def updateRegenAmount(self, dependent_stat: "StatData") -> None:
        # NOTE: this should be called after init and at level ups
        # fpr instance self.regen_amount_percentage is dependent on the player's magic stat,
        # here i can filter it dynamically 
        if self.depends_on is None: raise AttributeError("There is no outer dependency on this stat, so it does not require an update-amount!")
        print(self.regen_rate_in_sec, self.regen_amount_percentage)
        self.regen_amount_percentage *= dependent_stat.base


@dataclass
class PlayerData(GameData):
    attack_cooldown: int
    switch_duration_cooldown: int

    health: StatData
    energy: StatData
    attack: StatData
    magic: StatData
    speed: StatData

    __stat_count: int = field(default = 0)

    # list to make easier real stat existance checking
    __stat_key_list: List[str] = field(default_factory = list, init = False)

    def __post_init__(self) -> None:
        # NOTE: at the data loading stage StatData is parsed as dict so I have to convert it
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
                    self.__stat_count += 1
                    self.__dict__[param] = StatData(**value) # type: ignore
                    self.__stat_key_list.append(param)

        # some stat can have dependency, provide them       
        stats_with_dependency = filter(lambda stat: stat.depends_on is not None, self.getRegenerableStats())
        for stat_with_dependency in stats_with_dependency:
            if stat_with_dependency.depends_on is None: continue # should not happen bc of the filter but mypy can't understand that
            stat_with_dependency.updateRegenAmount(self.getStat(stat_with_dependency.depends_on))

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
