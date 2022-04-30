from typing import Optional

from player import Player
from pygame.sprite import Group

from .cameras import Renderer, YSortCameraRenderer


class SpriteGroups:
    "Collect levels sprite groups with the camera as well"
    def __init__(self, visible_sprites: Optional[Renderer] = None):
        if visible_sprites is None:
            self._visible_sprites_by_camera: Renderer = YSortCameraRenderer()
        else:
            self._visible_sprites_by_camera = visible_sprites

        self._obstacle_sprites = Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = Group()
        self._attackable_sprites = Group()

    @property
    def visible_sprites(self) -> Renderer:
        return self._visible_sprites_by_camera

    @property
    def obstacle_sprites(self) -> Group:
        return self._obstacle_sprites

    @property
    def attackable_sprites(self) -> Group:
        return self._attackable_sprites

    def renderWithPlayer(self, player: Player) -> None:
        self._visible_sprites_by_camera.renderScreenWithPlayer(player)
