from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from game_essentails.events import key_broadcast_subject
from pygame.color import Color
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame.surface import Surface
from scripts.observer import EventObserverMsg, KeyObserver


class BasicUiElement(ABC):
    def __init__(self, visibility: bool = False, *, parent_is_visible: Optional[Callable[..., Any]] = None):
        self.__parent_is_visible = parent_is_visible # for sub-ui elements like buttons
        self.visible = visibility # for main ui elements like menus
    
    def isVisible(self) -> bool:
        return self.visible

    @abstractmethod
    def draw(self, _surface: Optional[Surface] = None) -> None:...

    def parentIsVisible(self) -> bool:
        return self.__parent_is_visible is not None and self.__parent_is_visible()

class ClickableUiElement(BasicUiElement, KeyObserver[EventObserverMsg]):
    def __init__(self, visibility: bool = False, parent_is_visible: Optional[Callable[..., Any]] = None):
        super().__init__(visibility, parent_is_visible=parent_is_visible)

        self._clicked = False
        self.__registerForKeys()

    def __registerForKeys(self) -> None:
        key_broadcast_subject.attach(self, MOUSEBUTTONDOWN)
        key_broadcast_subject.attach(self, MOUSEBUTTONUP)

    @abstractmethod
    def getStateColor(self) -> Color:...


class HoverUiElement(BasicUiElement, KeyObserver[EventObserverMsg]):
    def __init__(self, visibility: bool = False, parent_is_visible: Optional[Callable[..., Any]] = None):
        super().__init__(visibility, parent_is_visible=parent_is_visible)

        self.__registerForKeys()
    
    def __registerForKeys(self) -> None:
        key_broadcast_subject.attach(self, MOUSEMOTION)
