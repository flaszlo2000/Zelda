import settings
from pygame import Rect
from pygame.display import get_surface
from pygame.draw import rect as draw_rect
from pygame.font import Font
from typing import Dict

from ui.button import Button, ButtonFactory


class BasicUiElement: # TODO: move this to a separate file and use it as parent class everywhere
    def __init__(self, visibility = False):
        self.visible = visibility
    
    def isVisible(self) -> bool:
        return self.visible

class Menu(BasicUiElement):
    def __init__(self):
        super().__init__()

        button_factory = ButtonFactory(self.isVisible)

        self.button_group: Dict[Button] = {
            "exit": button_factory.create(lambda: print("exit"), [150, 100, 50, 50]),
            "save": button_factory.create(lambda: print("save"), [250, 100, 50, 50]),
            "load": button_factory.create(lambda: print("load"), [350, 100, 50, 50]),
        }

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

        for button in self.button_group.values():
            draw_rect(surface, button.getStateColor(), button)

if __name__ == "__main__":
    test_menu = Menu()
    print(test_menu)