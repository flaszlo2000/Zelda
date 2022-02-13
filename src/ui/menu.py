import settings
from pygame import Rect
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.display import get_surface
from pygame.draw import rect as draw_rect
from pygame.font import Font

from scripts.observer import KeyObserver, EventObserverMsg
from game_essentails.events import key_broadcast_subject


class Menu(KeyObserver):
    def __init__(self, _visible: bool = False):
        self.visible = _visible

        self.colors = ["#ff0000", "#00ff00"]
        self.clicked = False

        self._registerForKeys()

    def updateByNotification(self, msg: EventObserverMsg) -> None:
        if self.visible:
            if msg.value.type == MOUSEBUTTONDOWN:
                if self.button.collidepoint(msg.value.pos):
                    self.clicked = True
            else:
                if self.clicked:
                    if self.button.collidepoint(msg.value.pos):
                        print("exit")

                    self.clicked = False

    def _registerForKeys(self) -> None:
        key_broadcast_subject.attach(self, MOUSEBUTTONDOWN)
        key_broadcast_subject.attach(self, MOUSEBUTTONUP)

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

        self.button = Rect(150, 100, 50, 50)
        draw_rect(surface, self.colors[self.clicked], self.button)

if __name__ == "__main__":
    test_menu = Menu()
    print(test_menu)