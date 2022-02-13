from pygame.sprite import Group
from pygame.display import get_surface
from pygame.math import Vector2
from abc import ABC, abstractmethod
from pathlib import Path

from src.player import Player
from scripts.image_provider import image_provider



class Renderer(ABC, Group):
    @abstractmethod
    def renderScreenWithPlayer(self, player: Player) -> None:...

class YSortCameraRenderer(Renderer):
    def __init__(self):
        super().__init__()
        self.display_surface = get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = Vector2()

        # creating the floor
        # TODO: draw background
        self.floor_surf = image_provider.provideWithConvert(Path("./graphics/tilemap/ground.png"))
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def renderScreenWithPlayer(self, player: Player) -> None:
        # getting the offset of the player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        # TODO: draw background
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        # get ALL sprites in the parent Group and then sort them by centery
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
