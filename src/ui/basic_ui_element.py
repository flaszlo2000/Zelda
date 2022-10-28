from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from game_essentails.events import HOVER_TICK, key_broadcast_subject
from pygame.color import Color
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.time import set_timer
from scripts.observer import EventObserverMsg, KeyObserver
from setting_handler import get_common_setting


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

@dataclass
class HoverBehaviourData:
    mouse_on_it: bool = field(default = False)
    event_sent: bool = field(default = False)
    call_happened: bool = field(default = False)
    showup_delay: int = field(default = get_common_setting("effect_showup_ms_delay"))

    def setMouse(self, new_state: bool) -> None:
        self.mouse_on_it = new_state

    def dispatch(self) -> None:
        if self.event_sent: return # warning/exception ?

        set_timer(int(HOVER_TICK), self.showup_delay, 1)
        self.event_sent = True

    def reset(self) -> None:
        self.event_sent = False
        self.call_happened = False

    def wasAbleToCall(self) -> None:
        self.call_happened = True

class HoverUiElement(BasicUiElement, KeyObserver[EventObserverMsg]):
    def __init__(
        self,
        visibility: bool = False,
        parent_is_visible: Optional[Callable[..., Any]] = None,
        behaviour_data: Optional[HoverBehaviourData] = None
    ):
        super().__init__(visibility, parent_is_visible = parent_is_visible)
        self.behaviour_data = HoverBehaviourData() if behaviour_data is None else behaviour_data

        self.box: Optional[Rect] = None

        self.__registerKeys()

    @abstractmethod
    def hoverOn(self) -> None:...

    @abstractmethod
    def hoverOff(self) -> None:...

    def __registerKeys(self) -> None:
        key_broadcast_subject.attach(self, MOUSEMOTION) # global registration to catch mouse motion
        key_broadcast_subject.attach(self, int(HOVER_TICK))

    def updateByNotification(self, msg: EventObserverMsg) -> None:
        if self.box is None: return

        if msg.value.type == int(HOVER_TICK):
            if self.behaviour_data.mouse_on_it:
                # if the required time elapsed and the cursor is still in place
                self.behaviour_data.wasAbleToCall()
                self.hoverOn()
        else:
            self.hover(msg)

    def hover(self, msg: EventObserverMsg) -> None:
        if self.box is None: raise AttributeError("[*] ERROR: box must be not None to check hover!")

        self.behaviour_data.setMouse(self.box.collidepoint(msg.value.pos))

        if self.behaviour_data.mouse_on_it:
            if not self.behaviour_data.event_sent:
                self.behaviour_data.dispatch()
        else:
            if self.behaviour_data.call_happened:
                self.hoverOff()

            self.behaviour_data.reset()
