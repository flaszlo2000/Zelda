#! test, remove this
from datetime import datetime
from math import ceil
from typing import Callable, Optional

from game_essentails.effect.main import EffectAdapter
from pygame.display import get_surface
from pygame.surface import Surface
from setting_handler import get_common_setting

from .basic_ui_element import BasicUiElement
from .button import UiText


def calculate_remaining_time(effect_adapter: EffectAdapter) -> str:

    regen_multiplier = effect_adapter.regen_amount_percentage / effect_adapter.regen_rate_in_sec 
    remaining_percentage = (effect_adapter.max - effect_adapter.base) / (effect_adapter.max / 100) 

    remaining_seconds = remaining_percentage/regen_multiplier
    result = f"{round(remaining_seconds)}s"

    if remaining_seconds > 60*60:
        result = f"{round(remaining_seconds/(60*60), 1)}h"
    elif remaining_seconds > 60:
        result = f"{round(remaining_seconds/60, 1)}m"

    return result

class EffectView(BasicUiElement):
    count = 0 # helps to display shifted boxes
    gap_between_effects = 10
    size = get_common_setting("effect_box_size")
    height = get_common_setting("effect_box_height")
    alpha = get_common_setting("effect_alpha")
    max_count_in_line = 5

    def __init__(self, effect: EffectAdapter, end_callback: Callable[["EffectView"], None]):
        self.effect = effect
        self.end_callback = end_callback

        self.font = UiText()

        self.id = EffectView.count
        EffectView.count += 1
        self.surface = Surface((EffectView.size, EffectView.size))
        self.surface.set_alpha(EffectView.alpha)
        self.surface.fill("#ffffff")

        print(datetime.now())

    def effectTick(self) -> None:
        self.effect.regen()

    def draw(self, _surface: Optional[Surface] = None) -> None:
        if self.effect.hasReachedEnd():
            self.end_callback(self)
            EffectView.count -= 1 #! FIXME: this is going to make issues!!
            return

        if _surface is None:
            surface = get_surface()
        else:
            surface = _surface

        # display box with line and column shift
        box = surface.blit(
            self.surface,
            (
                EffectView.gap_between_effects + (
                    (self.id % EffectView.max_count_in_line) * (EffectView.size + EffectView.gap_between_effects)
                ),
                EffectView.height + (int(self.id / EffectView.max_count_in_line) * EffectView.height)
            )
        )

        self.font.text = calculate_remaining_time(self.effect)
        surface.blit(self.font.renderFont(), box)

