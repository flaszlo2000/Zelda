from typing import Callable, Optional

from game_essentails.effect.main import EffectAdapter
from pygame.display import get_surface
from pygame.surface import Surface
from setting_handler import get_common_setting

from .basic_ui_element import BasicUiElement


class EffectView(BasicUiElement):
    count = 0 # helps to display shifted boxes
    gap_between_effects = 10
    size = get_common_setting("effect_box_size")
    alpha = get_common_setting("effect_alpha")

    def __init__(self, effect: EffectAdapter, end_callback: Callable[["EffectView"], None]):
        self.effect = effect
        self.end_end_callback = end_callback

        self.id = EffectView.count
        EffectView.count += 1
        self.surface = Surface((EffectView.size, EffectView.size))
        self.surface.set_alpha(EffectView.alpha)
        self.surface.fill("#ffffff")

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

        surface.blit(
            self.surface,
            (
                EffectView.gap_between_effects + (self.id * (EffectView.size + EffectView.gap_between_effects)),
                60
            )
        )


