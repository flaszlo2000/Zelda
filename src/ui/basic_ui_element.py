from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from game_essentails.events import key_broadcast_subject
from pygame.color import Color
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame.rect import Rect
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
    def __init__(
        self,
        visibility: bool = False,
        parent_is_visible: Optional[Callable[..., Any]] = None,
    ):
        super().__init__(visibility, parent_is_visible = parent_is_visible)
        self.mouse_on_it = False
        self.box: Optional[Rect] = None
        self.__hover_c = 0
        self.hover_call_happened = False

        self.__registerKeys()

    @abstractmethod
    def hoverOn(self) -> None:...

    @abstractmethod
    def hoverOff(self) -> None:...

    def __registerKeys(self) -> None:
        key_broadcast_subject.attach(self, MOUSEMOTION) # global registration to catch mouse motion

    def hover(self, msg: EventObserverMsg) -> None:
        #! BUG: hover works on when menu is drawn
        if self.box is None: raise AttributeError("[*] ERROR: box must be not None to check hover!")

        lookup_value = self.mouse_on_it
        self.mouse_on_it = self.box.collidepoint(msg.value.pos)

        if lookup_value == self.mouse_on_it: 
            if self.mouse_on_it:
                self.__hover_c += 1 # TODO: make this not move based

                if self.__hover_c > 10 and not self.hover_call_happened: # TODO: make this configurable
                    self.hover_call_happened = True
                    self.hoverOn()
        else:
            self.__hover_c = 0

            if not self.mouse_on_it and self.hover_call_happened:
                self.hover_call_happened = False
                self.hoverOff()
