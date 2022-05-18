from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from entities.base_entity import LivingEntity
from game_essentails.data.models.stat import StatBase


#region effects
class Effect(ABC):
    @abstractmethod
    def perTick(self, on: LivingEntity) -> None:...
    @abstractmethod
    def end(self, on: LivingEntity) -> None:...

class Curse(Effect):...
class DeathCurse(Curse):
    def perTick(self, on: LivingEntity) -> None:
        return 

    def end(self, on: LivingEntity) -> None:
        on.die()
#endregion

@dataclass
class EffectAdapter(StatBase):
    entity_that_has_been_cast_on: LivingEntity = field(init = False) 
    effect: Effect = field(init = False)

    #region builder pattern to solve dataclass inheritance issue
    def attachEntity(self, entity: LivingEntity) -> "EffectAdapter":
        self.entity_that_has_been_cast_on = entity
        return self

    def attachEffect(self, effect: Effect) -> "EffectAdapter":
        self.effect = effect
        return self
    #endregion

    def hasReachedEnd(self) -> bool:
        return self.base >= self.max

    def regen(self) -> None:
        super().regen()
        self.effect.perTick(self.entity_that_has_been_cast_on)

        if self.hasReachedEnd():
            self.effect.end(self.entity_that_has_been_cast_on)
