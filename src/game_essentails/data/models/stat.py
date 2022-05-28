from dataclasses import dataclass, field
from typing import Tuple, cast


@dataclass
class StatBase:
    base: float = field(default = 0)
    max: int = field(default = 0)

    can_be_regened: bool = field(default = False)
    regen_rate_in_sec: float = field(default = .5) # 1 == 1call/s, .5 == 2call/s, 20 == 1call/20s
    regen_amount_percentage: float = field(default = 1)
    regen_max_percentage: float = field(default = 100) # determines how much a stat can be regen automatically
    depends_on: Tuple[str] = field(default= cast(Tuple[str], tuple())) # specify some other stat which will alter the regen amount

    # non-file related params
    should_be_shown: bool = field(init = False, default = False)
    frame_c: int = field(default = 0, init = False)

    def __post_init__(self) -> None:
        self.should_be_shown = self.base != self.max

    def regen(self) -> None:
        if not self.can_be_regened: raise ValueError("This stat can't be regened automatically!")
        if self.base >= (self.max * (self.regen_max_percentage / 100)): return

        self.frame_c += 1
        if self.frame_c >= (60 * self.regen_rate_in_sec): #! FIXME: magic number! should be game fps!
            self.base += (self.max * (self.regen_amount_percentage / 100))

            if self.base > self.max:
                self.base = self.max
    
            self.frame_c = 0

    def updateRegenAmount(self, dependent_stat: "StatData") -> None:
        # NOTE: this should be called after init and at level ups
        # fpr instance self.regen_amount_percentage is dependent on the player's magic stat,
        # here i can filter it dynamically 
        if not self.depends_on: raise AttributeError("There is no outer dependency on this stat, so it does not require an update-amount!")
        self.regen_amount_percentage *= dependent_stat.base


@dataclass
class StatData(StatBase):
    initial_upgrade_cost: int = field(default = 1)
    
