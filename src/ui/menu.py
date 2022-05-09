from typing import List, Optional

from game_essentails.events import (MAIN_SOUND_TOGGLE, SAVE,
                                    key_broadcast_subject)
from game_essentails.save_handling.constants import MUSIC_ON_STARTUP
from game_essentails.save_handling.data_request import data_request
from pygame import Rect
from pygame.constants import QUIT, K_e
from pygame.display import get_surface
from pygame.draw import rect as draw_rect
from pygame.font import Font
from pygame.surface import Surface
from scripts.observer import KeyValueObserverMsg
from setting_handler import get_common_setting

from .basic_ui_element import BasicUiElement
from .button import ButtonData, ButtonFactory, ButtonGroup, ButtonText
from .toggle import Toggle


class Menu(BasicUiElement):
    def __init__(self):
        super().__init__()

        button_factory = ButtonFactory(self.isVisible)
        button_data: List[ButtonData] = [
            ButtonData(ButtonText("exit"), lambda: key_broadcast_subject.notify(QUIT), (150, 100, 50, 50)),
            ButtonData(ButtonText("save"), lambda: print("save"), (250, 100, 50, 50)),
            ButtonData(ButtonText("load"), lambda: print("load"), (350, 100, 50, 50)),
        ]

        self._button_group = ButtonGroup(button_data, button_factory)
        self.__setKeyBindings()

        self.first_open = True #! FIXME: find a better way to be able to do this 
        self.music_toggle = Toggle((1020, 590, 65, 35), self.isVisible)
        self.music_toggle.addCommand(self.changeStateOfMusicStartup)

    def __setKeyBindings(self) -> None:
        exit_button = self._button_group.getButton("exit")
        exit_button.setKeybinding(K_e)

    def toggle(self) -> None:
        if self.first_open:
            # NOTE: at the first open we are asking for the initial state of music startup
            # because if i do this in the constructor then it will fail because SaveSystem is 
            # not present yet and can't do it's functionality
            self.music_toggle.state = self.__getInitialStateOfMusicStartup()
            self.first_open = False

        self.visible = not self.visible

    def draw(self, _surface: Optional[Surface] = None) -> None:
        if not self.visible: return

        if _surface is None:
            surface = get_surface()
        else:
            surface = _surface

        screen_size = surface.get_size()

        self.font = Font(get_common_setting("ui_font"), get_common_setting("ui_font_size"))
        menu_body = draw_rect(surface, "#00abff", Rect(120, 50, 1000, 600))
        text_surface = self.font.render("Menu", False, get_common_setting("text_color"))
        surface.blit(text_surface, menu_body)

        self._button_group.draw()
        self.music_toggle.draw()

    def changeStateOfMusicStartup(self) -> None:
        key_broadcast_subject.notify(SAVE, KeyValueObserverMsg(MUSIC_ON_STARTUP, self.music_toggle.state))
        key_broadcast_subject.notify(MAIN_SOUND_TOGGLE)

    def __getInitialStateOfMusicStartup(self) -> bool:
        return data_request(MUSIC_ON_STARTUP) == "True"

if __name__ == "__main__":
    test_menu = Menu()
    print(test_menu)
