import pygame
import sys, signal

import settings
from level import Level


class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGTH))
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()

		self.level = Level() # TODO: make this dynamic

		# sound 
		main_sound = pygame.mixer.Sound('../audio/main.ogg')
		main_sound.set_volume(0.5)
		main_sound.play(loops = -1)
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()

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