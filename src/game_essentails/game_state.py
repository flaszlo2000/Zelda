from dataclasses import dataclass, field
from player import Player

from ui import UI


@dataclass
class GameState:
    __game_alive: bool = field(default=False)
    __game_paused: bool = field(default = False)
    __ui: UI = field(default_factory = UI)

    def makeGameAlive(self) -> None:
        self.__game_alive = True

    def isAlive(self) -> bool:
        return self.__game_alive
    
    def kill(self) -> None:
        self.__game_alive = False

    def updateUi(self, player: Player):
        self.__ui.display(player)