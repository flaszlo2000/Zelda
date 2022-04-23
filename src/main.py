import pygame
import sys, signal

from game_essentails.level_handling.level_handler import LevelHandler
from game_essentails.game_state import GameState
from ui.ui import UI
from level import Level
from game_essentails.events import key_broadcast_subject
from scripts.observer import EventObserverMsg, CallbackObserver
from setting_handler import setting_loader


class Game:
    def __init__(self, level_handler: LevelHandler = None):
        self.__pygameInit()

        self.ui = UI()
        self.game_state = GameState(_ui = self.ui)
        
        initial_level = Level(self.game_state.getGamePauser()) # TODO: make this dynamic
        if level_handler is None:
            self.level_handler = LevelHandler(initial_level, self.game_state)
        else:
            self.level_handler = level_handler

        self._fetchBindings()
        self._event_observer = CallbackObserver(lambda arg: self._quit()) # TODO: make this more flexible
        key_broadcast_subject.attach(self._event_observer, pygame.QUIT)

    def __pygameInit(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((setting_loader.getSingleValueFrom("common", "width"), setting_loader.getSingleValueFrom("common", "height")))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()

        # sound 
        main_sound = pygame.mixer.Sound('./audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops = -1)

    def _fetchBindings(self) -> None:
        # TODO: read this from file
        self.event_dict = {
            pygame.QUIT: self._quit
        }

        self.key_binding_dict = {
            pygame.K_m: self.level_handler.toggleMenu,
            pygame.K_ESCAPE: self.showMenu,
            pygame.K_0: lambda: self.level_handler.changeLevel("test")
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
        needed_mouse_event = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP] # for observer (menu)

        while self.game_state.isAlive():
            for event in pygame.event.get():
                if event.type in handled_events:
                    self.event_dict[event.type]()
                
                if event.type == pygame.KEYDOWN and event.key in key_bindings:
                    self.key_binding_dict[event.key]()

                # observer notification
                if event.type == pygame.KEYDOWN or event.type in needed_mouse_event:
                    event_id: int = event.type
                    
                    if event.type == pygame.KEYDOWN:
                        event_id = event.key

                    if event_id in key_broadcast_subject.getEventList():
                        key_broadcast_subject.notify(event_id, EventObserverMsg(event))

            self.screen.fill(settings.WATER_COLOR)
            self.level_handler.updateLevel()
            pygame.display.update()
            self.clock.tick(settings.FPS)

        self._quit()

    def sigint(self, signum, frame) -> None:
        self.game_state.kill()
    
    def sigterm(self, signum, frame) -> None:
        self.game_state.kill()
 
if __name__ == '__main__':
    game = Game()
    signal.signal(signal.SIGINT, game.sigint)
    signal.signal(signal.SIGTERM, game.sigterm)

    game.run()