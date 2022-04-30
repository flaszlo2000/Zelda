from dataclasses import dataclass, field
from typing import Any, List

import pygame
import setting_handler as settings
from entities.player import Player
from game_essentails.data.models.base import GameData
from pygame.surface import Surface
from scripts.image_provider import image_provider
from setting_handler import setting_loader

from .menu import Menu


def get_setting(setting_name: str, _of: str = "common") -> Any:
    return setting_loader.getSingleValueFrom(_of, setting_name)

@dataclass
class UI:
    display_surface: Surface = field(default_factory = pygame.display.get_surface)
    menu: Menu = field(default_factory = Menu)

    def __post_init__(self):
        # general 
        self.font = pygame.font.Font(
            get_setting("ui_font"),
            get_setting("ui_font_size")
        )

        # bar setup         
        self.health_bar_rect = pygame.Rect(10, 10, get_setting("health_bar_width"), get_setting("bar_height"))
        self.energy_bar_rect = pygame.Rect(10, 34, get_setting("energy_bar_width"), get_setting("bar_height"))

        # convert weapon and magic dictionary
        self.weapon_graphics: List[Surface] = UI.getGraphicsListOf(setting_loader["weapons"])
        self.magic_graphics: List[Surface] = UI.getGraphicsListOf(setting_loader["magic"])

    @staticmethod
    def getGraphicsListOf(data_list: List[GameData]) -> List[Surface]:
        result_list: List[Surface] = list()

        for data_object in data_list:
            if data_object.graphics_src is None:
                raise ValueError(f"{data_object} should have initialized graphics_src!")

            converted_image = image_provider.provideWithAlphaConvert(data_object.graphics_src)
            result_list.append(converted_image)

        return result_list

    def show_bar(self, current,max_amount,bg_rect,color):
        # draw bg 
        pygame.draw.rect(self.display_surface, settings.UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface, settings.UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self,exp):
        text_surf = self.font.render(str(int(exp)), False, settings.TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface, settings.UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface, settings.UI_BORDER_COLOR, text_rect.inflate(20,20),3)

    def selection_box(self,left,top, has_switched):
        bg_rect = pygame.Rect(left,top, settings.ITEM_BOX_SIZE, settings.ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, settings.UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, settings.UI_BORDER_COLOR_ACTIVE, bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface, settings.UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self,weapon_index,has_switched):
        bg_rect = self.selection_box(10,630,has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf,weapon_rect)

    def magic_overlay(self,magic_index,has_switched):
        bg_rect = self.selection_box(80,635,has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(magic_surf,magic_rect)

    def display(self, player: Player):
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect, settings.HEALTH_COLOR)
        self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect, settings.ENERGY_COLOR)

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
        self.magic_overlay(player.magic_index,not player.can_switch_magic)

        self.menu.draw()

    def toggleMenu(self) -> None:
        self.menu.toggle()
