import settings
from pygame import Rect
from pygame import event, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.display import get_surface
from pygame.draw import rect as draw_rect
from pygame.font import Font


class Menu:
    def __init__(self, _visible: bool = False):
        self.visible = _visible

        self.colors = ["#ff0000", "#00ff00"]
        self.clicked = False

    def toggle(self) -> None:
        self.visible = not self.visible

    def check_for_click(self):
        # TODO: move this to the global key checking
        for _event in event.get():
            if _event.type == MOUSEBUTTONDOWN:
                if self.button.collidepoint(_event.pos):
                    self.clicked = True
            
            if _event.type == MOUSEBUTTONUP and self.clicked:
                self.clicked = False

    def draw(self) -> None:
        if not self.visible: return

        surface = get_surface()
        screen_size = surface.get_size()

        self.font = Font(settings.UI_FONT, settings.UI_FONT_SIZE)
        menu_body = draw_rect(surface, "#00abff", Rect(120, 50, 1000, 600))
        text_surface = self.font.render("Menu", False, settings.TEXT_COLOR)
        surface.blit(text_surface, menu_body)

        self.button = Rect(150, 100, 50, 50)
        draw_rect(surface, self.colors[self.clicked], self.button)

        self.check_for_click()