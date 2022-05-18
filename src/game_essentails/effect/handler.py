from dataclasses import dataclass, field
from typing import List

from src.game_essentails.pauser import GamePauser
from ui.effect_view import EffectView

from .main import EffectAdapter


@dataclass
class EffectHandler:
    _game_pauser: GamePauser
    effect_view_list: List[EffectView] = field(default_factory = list)

    def __iadd__(self, new: EffectAdapter) -> "EffectHandler":
        new_effect_view = EffectView(new, self.endCallback)
        self.effect_view_list.append(new_effect_view)

        return self

    def add(self, new: EffectAdapter) -> None:
        self += new

    def update(self) -> None:
        for effect_view in self.effect_view_list:
            if not self._game_pauser.isPaused():
                effect_view.effectTick()
            effect_view.draw()

    def endCallback(self, effect: EffectView) -> None:
        self.effect_view_list.remove(effect)
