from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Tuple

from pygame.color import Color
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.display import get_surface
from pygame.draw import rect as draw_rect
from pygame.rect import Rect
from pygame.surface import Surface
from scripts.observer import EventObserverMsg

from .basic_ui_element import ClickableUiElement


@dataclass
class ToggleState:
    on: bool = field(default = False)
    colors: Tuple[Color, Color] = field(default = (Color("#00ff00"), Color("#ff0000"))) # on, off
    
    # NOTE: appendal of a command is only allowed after init  
    command: Optional[Callable[..., None]] = field(default = None, init = False)


class Toggle(ClickableUiElement, Rect):
    def __init__(
        self,
        rect_pos: Tuple[int, int, int, int],
        parent_is_visible: Callable[..., Any],
        state: Optional[ToggleState] = None,
        visibility: bool = False,
    ):
        ClickableUiElement.__init__(self, visibility, parent_is_visible=parent_is_visible)
        Rect.__init__(self, rect_pos)

        if state is None:
            self.inner_state = ToggleState()
        else:
            self.inner_state = state

    def getStateColor(self) -> Color:
        return self.inner_state.colors[(not self.inner_state.on)]

    def draw(self, _surface: Optional[Surface] = None) -> None:
        if _surface is None:
            surface = get_surface()
        else:
            surface = _surface

        draw_rect(surface, self.getStateColor(), self)

    def updateByNotification(self, msg: EventObserverMsg) -> None:
        if not self.parentIsVisible(): return
        if self.inner_state.command is None:
            print("[*] WARNING: command is uninitalized!")
            return 

        #! FIXME: remove code duplication between ClickableUiElements
        if msg.value.type == MOUSEBUTTONDOWN:
            if self.collidepoint(msg.value.pos):
                self._clicked = True
        elif msg.value.type == MOUSEBUTTONUP:
            if self._clicked:
                if self.collidepoint(msg.value.pos):
                    self.inner_state.on = not self.inner_state.on
                    self.inner_state.command()
                
                self._clicked = False

    def addCommand(self, command: Callable[..., None]) -> None:
        self.inner_state.command = command

    @property
    def state(self) -> bool:
        return self.inner_state.on

    @state.setter
    def state(self, new_value: bool) -> None:
        self.inner_state.on = new_value
