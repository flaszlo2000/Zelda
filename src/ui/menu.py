import settings
from pygame import Rect
from pygame.display import get_surface
from pygame.draw import rect as draw_rect
from pygame.font import Font
from pygame.constants import QUIT
from typing import List

from ui.button import ButtonText, ButtonFactory, ButtonGroup, ButtonData
from game_essentails.events import key_broadcast_subject


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

    def toggle(self) -> None:
        self.visible = not self.visible

    def draw(self) -> None:
        if not self.visible: return

        surface = get_surface()
        screen_size = surface.get_size()

        self.font = Font(settings.UI_FONT, settings.UI_FONT_SIZE)
        menu_body = draw_rect(surface, "#00abff", Rect(120, 50, 1000, 600))
        text_surface = self.font.render("Menu", False, settings.TEXT_COLOR)
        surface.blit(text_surface, menu_body)

        self._button_group.draw()

if __name__ == "__main__":
    test_menu = Menu()
    print(test_menu)