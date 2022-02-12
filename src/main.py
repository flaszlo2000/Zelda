import pygame
import sys, signal

import settings
from level import Level


class Game:
    def __init__(self):
        self.alive = False

        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGTH))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()

        self.level = Level() # TODO: make this dynamic

        self._fetchBindings()

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
            pygame.K_m: self.level.toggle_menu,
            pygame.K_ESCAPE: self.showMenu
        }

    def _quit(self) -> None:
        pygame.quit()
        sys.exit()

    def showMenu(self) -> None:
        print("show menu")

    def run(self):
        self.alive = True

        handled_events = self.event_dict.keys()
        key_bindings = self.key_binding_dict.keys()

        while self.alive:
            for event in pygame.event.get():
                if event.type in handled_events:
                    self.event_dict[event.type]()
                
                if event.type == pygame.KEYDOWN and event.key in key_bindings:
                    self.key_binding_dict[event.key]()

            self.screen.fill(settings.WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(settings.FPS)

    def sigint(self, signum, frame) -> None:
        self.alive = False
    
    def sigterm(self, signum, frame) -> None:
        self.alive = False

 
if __name__ == '__main__':
    game = Game()
    signal.signal(signal.SIGINT, game.sigint)
    signal.signal(signal.SIGTERM, game.sigterm)

    game.run()