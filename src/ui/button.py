import settings
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame import Rect as PygameRect
from pygame.display import get_surface
from pygame.surface import Surface
from pygame.font import Font
from pygame.draw import rect as draw_rect
from dataclasses import dataclass, field
from typing import List, Callable, Dict, Tuple
from abc import ABC, abstractmethod

from scripts.observer import KeyObserver, EventObserverMsg
from game_essentails.events import key_broadcast_subject


@dataclass
class ButtonText:
    "Text ontop the button"
    text: str = field(default = "")
    font: Font = field(default = Font(settings.UI_FONT, settings.UI_FONT_SIZE))
    antialias: bool = field(default = False)
    color: str = field(default = settings.TEXT_COLOR)
    should_capitalize: bool = field(default = True)

    def renderFont(self) -> Surface:
        text = self.text

        if self.should_capitalize:
            text = text.capitalize()

        return self.font.render(text, self.antialias, self.color)

@dataclass
class ButtonData:
    "Representation of a Button initial parameters"
    button_text: ButtonText
    command: Callable
    rect_pos: List[int] # should contain 4 ints
    colors: Tuple[str] = field(default= ("#ff0000", "#00ff00"))

    def getButtonTextStr(self) -> str:
        return self.button_text.text

class ButtonBase(PygameRect, KeyObserver, ABC):
    @abstractmethod
    def getStateColor(self) -> str:...

    @abstractmethod
    def draw(self) -> None:...

class Button(ButtonBase):
    def __init__(self, parent_is_visible: Callable[[], bool], data: ButtonData, *args, **kwargs):
        super().__init__(*data.rect_pos, *args, **kwargs)

        self.__clicked = False
        self.__parent_is_visible = parent_is_visible
        self._data = data

        self._registerForKeys()

    def _registerForKeys(self) -> None:
        key_broadcast_subject.attach(self, MOUSEBUTTONDOWN)
        key_broadcast_subject.attach(self, MOUSEBUTTONUP)

    def updateByNotification(self, msg: EventObserverMsg) -> None:
        if self.__parent_is_visible():
            if msg.value.type == MOUSEBUTTONDOWN:
                if self.collidepoint(msg.value.pos):
                    self.__clicked = True
            else:
                if self.__clicked:
                    if self.collidepoint(msg.value.pos):
                        self._data.command()

                    self.__clicked = False

    def getStateColor(self) -> str:
        return self._data.colors[self.__clicked]

    def setColors(self, new_colors: Tuple[str]) -> None:
        if len(new_colors) != 2: raise ValueError("Incorrect parameter, the new_colors tuple must contain two elements!")

        self._data.colors = new_colors

    def setCommand(self, new_command: Callable) -> None:
        self._data.command = new_command

    def draw(self, display: Surface) -> None:
        drawn_rect = draw_rect(display, self.getStateColor(), self)
        final_text = self._data.button_text.renderFont()

        display.blit(final_text, drawn_rect)

class ButtonFactory:
    "Factory to create more than one Buttons within the same UI element"
    def __init__(self, parent_is_visible: Callable[[], bool]):
        self.__parent_is_visible = parent_is_visible

    def create(self, button_data: ButtonData, *args, **kwargs) -> ButtonBase:
        return Button(self.__parent_is_visible, button_data, *args, **kwargs)

class ButtonGroup:
    def __init__(self, button_data_list: List[ButtonData], button_factory: ButtonFactory):
        self._buttons: Dict[str, Button] = {}
        self.display_surface = get_surface()

        for button_data in button_data_list:
            self._buttons[button_data.getButtonTextStr()] = button_factory.create(button_data)

    def draw(self) -> None:
        for button in self._buttons.values():
            button.draw(self.display_surface)