from abc import ABC, abstractmethod
from typing import Optional

from game_essentails.events import key_broadcast_subject
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.surface import Surface
from scripts.observer import EventObserverMsg, KeyObserver


class BasicUiElement(ABC):
    def __init__(self, visibility: bool = False):
        self.visible = visibility
    
    def isVisible(self) -> bool:
        return self.visible

    @abstractmethod
    def draw(self, _surface: Optional[Surface] = None) -> None:...

class ClickableUiElement(BasicUiElement, KeyObserver[EventObserverMsg]):
    def __init__(self, visibility: bool = False):
        super().__init__(visibility)

        self._clicked = False
        self.__registerForKeys()

    def __registerForKeys(self) -> None:
        key_broadcast_subject.attach(self, MOUSEBUTTONDOWN)
        key_broadcast_subject.attach(self, MOUSEBUTTONUP)
