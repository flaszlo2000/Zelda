from dataclasses import dataclass, field

from scripts.observer import StrObserverMsg

from game_essentails.events import PAUSE_TOGGLE, key_broadcast_subject


@dataclass
class GamePauser:
    __state: bool = field(default = False) 

    def isPaused(self) -> bool:
        return self.__state

    def toggle(self) -> None:
        self.__state = not self.__state
        key_broadcast_subject.notify(PAUSE_TOGGLE, StrObserverMsg(self.__state))
