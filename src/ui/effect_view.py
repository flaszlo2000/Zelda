from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime  # ! test, remove this
from typing import Callable, Optional

from game_essentails.effect.effects import Effect
from pygame.display import get_surface
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface
from scripts.image_provider import image_provider
from scripts.observer import EventObserverMsg
from setting_handler import get_common_setting

from .basic_ui_element import HoverUiElement
from .button import UiText


def calculate_remaining_time(effect_adapter: Effect) -> str:
    regen_multiplier = effect_adapter.regen_amount_percentage / effect_adapter.regen_rate_in_sec 
    remaining_percentage = (effect_adapter.max - effect_adapter.base) / (effect_adapter.max / 100) 

    remaining_seconds = remaining_percentage/regen_multiplier
    result = f"{round(remaining_seconds)}s"

    if remaining_seconds > 60*60:
        result = f"{round(remaining_seconds/(60*60), 1)}h"
    elif remaining_seconds > 60:
        result = f"{round(remaining_seconds/60, 1)}m"

    return result

@dataclass
class EffectViewSettings:
    gap_between_effects: int = field(default = 10)
    size: int = field(default = get_common_setting("effect_box_size"))
    height: int = field(default = get_common_setting("effect_box_height"))
    alpha: int = field(default = get_common_setting("effect_alpha"))
    max_count_in_line: int = field(default = 5)


#region strategy pattern for showing effects
class ViewStrategy(ABC):
    @staticmethod
    @abstractmethod
    def show(
        main_surface: Surface,
        view_surface: Surface,
        settings: EffectViewSettings,
        _id: int,

        owner_sprite: Optional[Sprite] = None # for non-ui
    ) -> Rect:...

class PlayerView(ViewStrategy):
    @staticmethod
    def show(
        main_surface: Surface,
        view_surface: Surface,
        settings: EffectViewSettings,
        _id: int,
        owner_sprite: Optional[Sprite] = None
    ) -> Rect:
        "Show effect on the main UI"
        return main_surface.blit(
            view_surface,
            (
                settings.gap_between_effects + (
                    (_id % settings.max_count_in_line) * (settings.size + settings.gap_between_effects)
                ),
                settings.height + (int(_id / settings.max_count_in_line) * settings.height)
            )
        )

class NonUiRelatedView(ViewStrategy):
    @staticmethod
    def show(
        main_surface: Surface,
        view_surface: Surface,
        settings: EffectViewSettings,
        _id: int,
        owner_sprite: Optional[Sprite] = None
    ) -> Rect:
        if owner_sprite is None: raise AttributeError("To use this strategy, owner_rect must be specified!")

        return owner_sprite.rect # TODO: refactor this
#endregion


class EffectView(HoverUiElement):
    count = 0 # static counter to help display shifted boxes    

    def __init__(
        self, 
        effect: Effect, 
        end_callback: Callable[["EffectView"], None],
        use_ui_view: bool = False,
        settings: Optional[EffectViewSettings] = None
    ):
        super().__init__()
        self._effect = effect 
        self.end_callback = end_callback
        self._should_use_ui_view = use_ui_view
        self.view_strategy = NonUiRelatedView() if not self._should_use_ui_view else PlayerView()
        self.settings = EffectViewSettings() if settings is None else settings 

        self.font = UiText()

        self.id = EffectView.count
        EffectView.count += 1

        # main transparent box
        self.surface = Surface((self.settings.size, self.settings.size))
        self.surface.set_alpha(self.settings.alpha)
        self.surface.fill("#ffffff")

        self.sprite = Sprite()

        print(datetime.now())

    def effectTick(self) -> None:
        self._effect.regen()

    def draw(self, _surface: Optional[Surface] = None) -> None:
        if self._effect.hasReachedEnd():
            self.end_callback(self)
            EffectView.count -= 1 #! FIXME: this is going to make issues!!
            return

        if _surface is None:
            surface = get_surface()
        else:
            surface = _surface


        # display box with line and column shift
        box = self.view_strategy.show(
            surface,
            self.surface,
            self.settings,
            self.id,
            self._effect.owner_sprite
        )

        self.font.text = calculate_remaining_time(self._effect)

        if self._should_use_ui_view:
            self.sprite.image = image_provider.provideWithAlphaConvert("./graphics/particles/aura/0.png")
            surface.blit(self.font.renderFont(), box)
        else:
            self.sprite.image = self.font.renderFont()
            self.sprite.rect = box
            self.sprite.image.set_colorkey("#ffffff")
            self._effect.owner_sprite.groups()[0].add(self.sprite)

    def updateByNotification(self, msg: EventObserverMsg) -> None:
        print(msg.value)
        # self.surface.get_rect().collidepoint()
