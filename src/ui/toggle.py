from dataclasses import dataclass, field
from typing import Callable, Optional, Tuple

from pygame.color import Color
from pygame.constants import MOUSEBUTTONUP
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
        state: Optional[ToggleState] = None,
        visibility: bool = False
    ):
        ClickableUiElement.__init__(self, visibility)
        Rect.__init__(self, rect_pos)

        if state is None:
            self.state = ToggleState()
        else:
            self.state = state

    def __getColor(self) -> Color:
        return self.state.colors[(not self.state.on)]

    def draw(self, _surface: Optional[Surface] = None) -> None:
        if _surface is None:
            surface = get_surface()
        else:
            surface = _surface

        draw_rect(surface, self.__getColor(), self)

    def updateByNotification(self, msg: EventObserverMsg) -> None:
        if msg.value.type != MOUSEBUTTONUP: return

        if self.state.command is not None:
            self.state.command()
        else:
            print("[*] WARNING: command is uninitalized!")

    def addCommand(self, command: Callable[..., None]) -> None:
        self.state.command = command
