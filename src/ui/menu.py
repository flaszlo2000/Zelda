from typing import List

from game_essentails.events import key_broadcast_subject
from pygame import Rect
from pygame.constants import QUIT, K_e
from pygame.display import get_surface
from pygame.draw import rect as draw_rect
from pygame.font import Font
from setting_handler import get_common_setting, setting_loader

from ui.button import ButtonData, ButtonFactory, ButtonGroup, ButtonText


class BasicUiElement: # TODO: move this to a separate file and use it as parent class everywhere
    def __init__(self, visibility = False):
        self.visible = visibility
    
    def isVisible(self) -> bool:
        return self.visible

class Menu(BasicUiElement):
    def __init__(self):
        super().__init__()

        button_factory = ButtonFactory(self.isVisible)
        button_data: List[ButtonData] = [
            ButtonData(ButtonText("exit"), lambda: key_broadcast_subject.notify(QUIT), [150, 100, 50, 50]),
            ButtonData(ButtonText("save"), lambda: print("save"), [250, 100, 50, 50]),
            ButtonData(ButtonText("load"), lambda: print("load"), [350, 100, 50, 50]),
        ]

        self._button_group = ButtonGroup(button_data, button_factory)
        self.__setKeyBindings()

    def __setKeyBindings(self) -> None:
        exit_button = self._button_group.getButton("exit")
        exit_button.setKeybinding(K_e)

    def toggle(self) -> None:
        self.visible = not self.visible

    def draw(self) -> None:
        if not self.visible: return

        surface = get_surface()
        screen_size = surface.get_size()

        self.font = Font(get_common_setting("ui_font"), get_common_setting("ui_font_size"))
        menu_body = draw_rect(surface, "#00abff", Rect(120, 50, 1000, 600))
        text_surface = self.font.render("Menu", False, get_common_setting("text_color"))
        surface.blit(text_surface, menu_body)

        self._button_group.draw()

if __name__ == "__main__":
    test_menu = Menu()
    print(test_menu)
