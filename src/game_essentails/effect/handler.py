from dataclasses import dataclass, field
from typing import List

from game_essentails.effect.effects import Effect
from game_essentails.events import PAUSE_TOGGLE, key_broadcast_subject
from scripts.observer import CallbackObserver, StrObserverMsg
from ui.effect_view import EffectView


# TODO: find out is it player or not?
@dataclass
class EffectHandler:
    # TODO: use Dict instead of List to create an Inventory like grid
    effect_view_list: List[EffectView] = field(default_factory = list)
    _game_paused: bool = field(default = False)

    def __post_init__(self):
        self._callback_observer = CallbackObserver(self.gameStateChange)
        key_broadcast_subject.attach(
            self._callback_observer,
            PAUSE_TOGGLE
        )

    def __iadd__(self, new: Effect) -> "EffectHandler":
        new_effect_view = EffectView(new, self.endCallback)
        self.effect_view_list.append(new_effect_view)

        return self

    def add(self, new: Effect) -> None:
        self += new

    def update(self) -> None:
        for effect_view in self.effect_view_list:
            if not self._game_paused:
                effect_view.effectTick()
            effect_view.draw()

    def endCallback(self, effect: EffectView) -> None:
        self.effect_view_list.remove(effect)

    def gameStateChange(self, msg: StrObserverMsg) -> None:
        self._game_paused = msg == "True"

    def withdrawObserverAttachment(self) -> None: # __delete__ ?
        key_broadcast_subject.detach(self._callback_observer)
