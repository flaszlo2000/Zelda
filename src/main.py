import signal
import sys
from typing import Any, Final, List, Optional, SupportsInt, cast

import pygame

from game_essentails.data.models.effect import EffectData
from game_essentails.events import HOVER_TICK, key_broadcast_subject
from game_essentails.game_state import GameState
from game_essentails.level_handling.level_handler import LevelHandler
from game_essentails.save_handling.constants import MUSIC_ON_STARTUP
from game_essentails.save_handling.data_request import data_request
from level import Level
from scripts.observer import CallbackObserver, EventObserverMsg
from setting_handler import get_common_setting, setting_loader
from sound import SoundHandler
from ui.ui import UI


class Game:
    def __init__(self, level_handler: Optional[LevelHandler] = None):
        self.__pygameInit()

        self.ui = UI()
        self.game_state = GameState(_ui = self.ui)
        
        initial_level = Level(self.game_state.getGamePauser()) # TODO: make this dynamic
        if level_handler is None:
            self.level_handler = LevelHandler(initial_level, self.game_state)
        else:
            self.level_handler = level_handler

        self._fetchBindings()
        
        # event listeners
        self._quit_observer = CallbackObserver[Any](lambda arg: self._quit()) # TODO: make this more flexible
        key_broadcast_subject.attach(self._quit_observer, pygame.QUIT)

        # post init db related stuff
        music_on_startup = data_request(MUSIC_ON_STARTUP) == "True"
        self.sound_handler.setMainSoundState(music_on_startup)

    def __pygameInit(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((get_common_setting("width"), get_common_setting("height")))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()

        # sound 
        self.sound_handler = SoundHandler()

    def _fetchBindings(self) -> None:
        # TODO: read this from file
        self.event_dict = {
            pygame.QUIT: self._quit
        }

        self.key_binding_dict = {
            pygame.K_m: self.level_handler.toggleMenu,
            pygame.K_ESCAPE: self.showMenu,
            pygame.K_0: lambda: self.level_handler.changeLevel("test"),
            pygame.K_1: self.castAllEffectOnPlayer
        }

    def _quit(self) -> None:
        print("Exit by calling quit!")
        pygame.quit()
        sys.exit()

    def showMenu(self) -> None:
        self.game_state.showMenu()

    def run(self):
        self.game_state.makeGameAlive()

        handled_events = self.event_dict.keys()
        key_bindings = self.key_binding_dict.keys()
        NEEDED_EVENTS: Final[List[SupportsInt]] = [
            pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, # mouse
            HOVER_TICK # hovering
        ] # for observer (menu)

        while self.game_state.isAlive():
            for event in pygame.event.get():
                if event.type in handled_events:
                    self.event_dict[event.type]()
                
                if event.type == pygame.KEYDOWN and event.key in key_bindings:
                    self.key_binding_dict[event.key]()

                # observer notification
                if event.type == pygame.KEYDOWN or event.type in map(int, NEEDED_EVENTS):
                    event_id: int = event.type
                    
                    if event.type == pygame.KEYDOWN:
                        event_id = event.key

                    if event_id == int(HOVER_TICK):
                        print("")

                    if event_id in key_broadcast_subject.getEventList():
                        key_broadcast_subject.notify(event_id, EventObserverMsg(event))

            self.screen.fill(get_common_setting("water_color"))
            self.level_handler.updateLevel()
            pygame.display.update()
            self.clock.tick(get_common_setting("fps"))

        self._quit()

    def castAllEffectOnPlayer(self) -> None:
        #! test purpose, remove this
        # this is only for testing the entity system and to create a good and extendable effect system

        player = self.level_handler._level.getPlayer()

        # for effect_data in setting_loader["effects"]:
        #     player.castEffectOn(cast(EffectData, effect_data))

        death_effect = list(filter(lambda element: element.name == "death",setting_loader["effects"]))[0]

        player.castEffectOn(cast(EffectData, death_effect))

    def sigint(self) -> None:
        self.game_state.kill()
    
    def sigterm(self) -> None:
        self.game_state.kill()
 
if __name__ == '__main__':
    game = Game()
    signal.signal(signal.SIGINT, lambda _, __: game.sigint())
    signal.signal(signal.SIGTERM, lambda _, __: game.sigterm())

    game.run()
