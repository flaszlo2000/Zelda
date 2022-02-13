import pygame 
from pygame.surface import Surface
from player import Player
from debug import debug
from data_loader import *
from random import choice, randint
from weapon import Weapon
from ui.ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade

from abc import ABC, abstractmethod

from settings import TILESIZE

from game_essentails.game_state import GamePauser
from game_essentails.tiles.grass import GrassTile
from game_essentails.tiles.real_object_tile import RealObjectTile
from game_essentails.tiles.boundary import BoundaryTile
from game_essentails.sprite_groups import SpriteGroups

#region future baseclasses

class BaseLevel(ABC):
    def __init__(self, game_pauser: GamePauser, sprite_groups: SpriteGroups = None):
        self.display_surface = pygame.display.get_surface()
        self._layouts = BaseLevel._fetchLayouts()
        self._graphics = BaseLevel._fetchGraphics()

        self.game_pauser = game_pauser

        if sprite_groups is None:
            self.sprite_groups = SpriteGroups()
        else:
            self.sprite_groups = sprite_groups

    @staticmethod
    @abstractmethod
    def _fetchLayouts() -> dict:...

    @staticmethod
    @abstractmethod
    def _fetchGraphics() -> dict:...

    @abstractmethod
    def createMap(self) -> None:...

    def getPlayer(self) -> Player:
        return self.player # NOTE: atm this has been created in create_map
#endregion


class Level:
    def __init__(self, game_pauser: GamePauser, sprite_groups: SpriteGroups = None):
        self.display_surface = pygame.display.get_surface()

        if sprite_groups is None:
            self.sprite_groups = SpriteGroups()
        else:
            self.sprite_groups = sprite_groups

        self.game_pauser = game_pauser
        
        # sprite setup
        self.create_map()

        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    @staticmethod
    def _fetchLayouts() -> dict:
        layouts = {
            'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./map/map_Grass.csv'),
            'object': import_csv_layout('./map/map_Objects.csv'),
            'entities': import_csv_layout('./map/map_Entities.csv')
        }

        return layouts

    @staticmethod
    def _fetchGraphics() -> dict:
        # FIXME: use ImageProvider
        graphics = {
            'grass': import_folder('./graphics/grass'),
            'objects': import_folder('./graphics/objects')
        }

        return graphics

    def create_map(self):
        layouts = Level._fetchLayouts()
        graphics = Level._fetchGraphics()

        # return
        for layout_name, grid in layouts.items():
            for y, row in enumerate(grid):
                for x, col in enumerate(row):
                    if col == "-1": continue

                    # NOTE: is it ok to not store anywhere these objects?
                    if layout_name == 'boundary':
                        BoundaryTile(self.sprite_groups, [x, y], Surface((TILESIZE,TILESIZE)))

                    if layout_name == 'grass':
                        random_grass_image = choice(graphics['grass'])
                        GrassTile(self.sprite_groups, [x, y], random_grass_image) 

                    if layout_name == 'object':
                        surface_image = graphics['objects'][int(col)]
                        RealObjectTile(self.sprite_groups, [x, y], surface_image)

                    if layout_name == 'entities':
                        if col == '394':
                            self.player = Player(
                                (x * TILESIZE, y * TILESIZE),
                                [self.sprite_groups.visible_sprites],
                                self.sprite_groups.obstacle_sprites,
                                self.create_attack,
                                self.destroy_attack,
                                self.create_magic)
                        else:
                            continue # FIXME
                            if col == '390': monster_name = 'bamboo'
                            elif col == '391': monster_name = 'spirit'
                            elif col == '392': monster_name ='raccoon'
                            else: monster_name = 'squid'
                            Enemy(
                                monster_name,
                                (x,y),
                                [self.visible_sprites,self.attackable_sprites],
                                self.obstacle_sprites,
                                self.damage_player,
                                self.trigger_death_particles,
                                self.add_exp)

    #region TODO: move this to player level
    def create_attack(self):
        
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

    def create_magic(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    #endregion

    def player_attack_logic(self):
        return
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

    def trigger_death_particles(self,pos,particle_type):

        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

    def add_exp(self,amount):

        self.player.exp += amount

    def run(self):
        self.sprite_groups.renderWithPlayer(self.player)
        
        if self.game_pauser.isPaused():
            #self.upgrade.displayUpgradeMenu() # FIXME: do not depend on the game state, use visible attribut instead
            pass
        else:
            # FIXME: LOD
            self.sprite_groups.visible_sprites.update()
            self.sprite_groups.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
    
    def getPlayer(self) -> Player:
        return self.player