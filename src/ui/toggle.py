from dataclasses import dataclass, field
from typing import Optional

from pygame.rect import Rect
from pygame.surface import Surface
from scripts.observer import EventObserverMsg

from .basic_ui_element import ClickableUiElement


@dataclass
class Toggle(Rect, ClickableUiElement):
    state: bool = field(default = False)

    def draw(self, _surface: Optional[Surface] = None) -> None:
        raise NotImplementedError()

    def updateByNotification(self, msg: EventObserverMsg) -> None:
        raise NotImplementedError()
