import pygame

from level import Level
from . game_state import GameState


class LevelHandler:
    def __init__(self, inital_level: Level, game_state: GameState):
        self._level = inital_level
        self._game_state = game_state

    def updateLevel(self) -> None:
        self._level.run()
        self._game_state.updateUi(self._level.getPlayer())

    def changeLevel(self, new_level: Level) -> bool:
        print("called")
    
    def toggleMenu(self) -> None:
        self._level.toggle_menu()