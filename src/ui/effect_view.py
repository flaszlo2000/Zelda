from typing import Callable, Optional

from game_essentails.effect.main import EffectAdapter
from pygame.display import get_surface
from pygame.draw import rect as draw_rect
from pygame.rect import Rect
from pygame.surface import Surface

from .basic_ui_element import BasicUiElement


class EffectView(BasicUiElement):
    count = 0 # helps to display
    gap_between_effects = 10
    size = 50

    def __init__(self, effect: EffectAdapter, end_callback: Callable[["EffectView"], None]):
        self.effect = effect
        self.end_end_callback = end_callback

        self.id = EffectView.count
        EffectView.count += 1


    def effectTick(self) -> None:
        self.effect.regen()

    def draw(self, _surface: Optional[Surface] = None) -> None:
        if self.effect.hasReachedEnd():
            self.end_end_callback(self)
            EffectView.count -= 1 #! FIXME: this is going to make issues!!
            return

        if _surface is None:
            surface = get_surface()
        else:
            surface = _surface
        
        draw_rect(
            surface,
            "#ffffff",
            Rect(
                EffectView.gap_between_effects + (self.id * (EffectView.size + EffectView.gap_between_effects)),
                60,
                EffectView.size,
                EffectView.size
            )
        )


