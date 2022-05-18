from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from game_essentails.events import key_broadcast_subject
from pygame.color import Color
from pygame.constants import MOUSEBUTTONDOWN
from pygame.display import get_surface
from pygame.draw import rect as draw_rect
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface
from scripts.observer import CallbackObserver, EventObserverMsg
from setting_handler import get_common_setting

from ui.basic_ui_element import ClickableUiElement


@dataclass
class UiText: #! TODO: move this to a separate file
    "Text ontop the button"
    text: str = field(default = "")
    font: Optional[Font] = field(default = None) 
    antialias: bool = field(default = False)
    color: str = field(default = get_common_setting("text_color"))
    should_capitalize: bool = field(default = True)

    def __post_init__(self) -> None:
        if self.font is None:
            self.font = Font(
                get_common_setting("ui_font"),
                get_common_setting("ui_font_size")
            )

    def renderFont(self) -> Surface:
        if self.font is None: raise ValueError("Font should not be None at this point!")

        text = self.text

        if self.should_capitalize:
            text = text.capitalize()

        return self.font.render(text, self.antialias, self.color)

@dataclass
class ButtonData:
    "Representation of a Button initial parameters"
    button_text: UiText
    command: Callable[..., None]
    rect_pos: Tuple[int, int, int, int]
    colors: Tuple[Color, Color] = field(default= (Color("#ff0000"), Color("#00ff00")))

    def getButtonTextStr(self) -> str:
        return self.button_text.text

class ButtonBase(Rect, ClickableUiElement):
    def __init__(self, rect_pos: Tuple[int, int, int, int], parent_is_visible: Callable[..., Any]):
        Rect.__init__(self, rect_pos)
        ClickableUiElement.__init__(self, parent_is_visible=parent_is_visible)

        self._keybind: Optional[CallbackObserver[Any]] = None

    @abstractmethod
    def setKeybinding(self, event_to_react_with: int) -> None:...

class Button(ButtonBase):
    def __init__(self, parent_is_visible: Callable[[], bool], data: ButtonData):
        super().__init__(data.rect_pos, parent_is_visible)
        self._data = data

    def updateByNotification(self, msg: EventObserverMsg) -> None:
        if self.parentIsVisible():
            if msg.value.type == MOUSEBUTTONDOWN:
                if self.collidepoint(msg.value.pos):
                    self._clicked = True
            else:
                if self._clicked:
                    if self.collidepoint(msg.value.pos):
                        self._data.command()

                    self._clicked = False

    def __keyBindingNotification(self) -> None:
        if self.parentIsVisible():
            self._data.command()

    def setKeybinding(self, event_to_react_with: int) -> None:
        if self._keybind is not None:
            # if the keybinding has been already set then unsubscribe
            key_broadcast_subject.detach(self._keybind)

        self._keybind = CallbackObserver(lambda msg: self.__keyBindingNotification())
        key_broadcast_subject.attach(self._keybind, event_to_react_with)

    def getStateColor(self) -> Color:
        return self._data.colors[self._clicked]

    def setColors(self, new_colors: Tuple[Color, Color]) -> None:
        if len(new_colors) != 2: raise ValueError("Incorrect parameter, the new_colors tuple must contain two elements!")

        self._data.colors = new_colors

    def setCommand(self, new_command: Callable[..., None]) -> None:
        self._data.command = new_command

    def draw(self, display: Optional[Surface] = None) -> None:
        if display is None:
            display = get_surface()

        drawn_rect = draw_rect(display, self.getStateColor(), self)
        final_text = self._data.button_text.renderFont()

        display.blit(final_text, drawn_rect)

class ButtonFactory:
    "Factory to create more than one Buttons within the same UI element"
    def __init__(self, parent_is_visible: Callable[[], bool]):
        self.__parent_is_visible = parent_is_visible

    def create(self, button_data: ButtonData) -> ButtonBase:
        return Button(self.__parent_is_visible, button_data)

class ButtonGroup:
    def __init__(self, button_data_list: List[ButtonData], button_factory: ButtonFactory):
        self._buttons: Dict[str, Button] = {}
        self.display_surface = get_surface()

        for button_data in button_data_list:
            self._buttons[button_data.getButtonTextStr()] = button_factory.create(button_data)

    def draw(self) -> None:
        for button in self._buttons.values():
            button.draw(self.display_surface)

    def getButton(self, key: str) -> Button:
        return self._buttons[key]
