from pathlib import Path
from typing import List, Tuple

import pygame
from pygame.sprite import Group

from entity import Entity
from game_essentails.data.models.base import GameData
from scripts.image_provider import image_provider
from setting_handler import setting_loader

#! not in use, only kept to check for features
raise NotImplementedError()

class Player(Entity):
    def __init__(self, pos: Tuple[int, int], groups: List[Group], obstacle_sprites):
        super().__init__(groups, is_player = True)
        self.image = image_provider.provideWithAlphaConvert(Path("./graphics/test/player.png"))
        self.rect = self.image.get_rect(topleft = pos)

        self.hitbox = self.rect.inflate(-6, setting_loader.getSingleValueFrom("hitbox_offset", "player"))

        # NOTE: for this line, everything is implemented

        # graphics setup
        self.import_player_assets() # NOTE: enemy.py has similar method called import_graphics
        self.status = 'down' # NOTE: needed for other entities as well

        # movement 
        self.attacking = False
        self.attack_cooldown = 400 # NOTE: needed for other entities as well
        self.attack_time = None # NOTE: needed for other entities as well
        self._obstacle_sprites = obstacle_sprites # NOTE: implemented, needed for collision

        # weapon
        # self.create_attack = create_attack
        # self.destroy_attack = destroy_attack
        self.weapon_index = 0

        # additional hotfix
        self.weapon_data = Player.getNamesFromGameData(setting_loader["weapons"])

        self.weapon = self.weapon_data[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magic 
        # self.create_magic = create_magic
        self.magic_index = 0

        # additional hotfix as well
        self.magic_data = Player.getNamesFromGameData(setting_loader["magic"])

        self.magic = self.magic_data[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 5, "test": 54}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic' : 10, 'speed': 10, "test": 540}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100, "test": 100}
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.exp = 5000
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # import a sound
        self.weapon_attack_sound = pygame.mixer.Sound('./audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

    @staticmethod
    def getNamesFromGameData(game_data: List[GameData]) -> List[str]:
        result = [data.name for data in game_data]

        return result

    @property
    def obstacle_sprites(self) -> object:
        # print("here")
        return self._obstacle_sprites

    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'up': [],'down': [],'left': [],'right': [],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        # FIXME: use eventObserver instead of this and remove this from player sprite representation
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # attack input 
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                # self.create_attack()
                print("create attack")
                self.weapon_attack_sound.play()

            # magic input 
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                # style = list(magic_data.keys())[self.magic_index]
                # strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                # cost = list(magic_data.values())[self.magic_index]['cost']
                # self.create_magic(style,strength,cost)
                print("create magic")

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                self.weapon_index = (self.weapon_index + 1) % len(self.weapon_data)

                self.weapon = self.weapon_data[self.weapon_index]

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                
                if self.magic_index < len(self.magic_data) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = self.magic_data[self.magic_index]

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + self.weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                #self.destroy_attack()
                print("destroy attack")

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        return # FIXME
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker 
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = self.weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = self.magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        # self.move(self.stats['speed']) # DONE
        self.energy_recovery()

    def testOuter(self):
        self.exp += 10000
