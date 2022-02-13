from dataclasses import dataclass, field
from player import Player

from ui.ui import UI


@dataclass
class GamePauser:
    __state: bool = field(default=False) 

    def isPaused(self) -> bool:
        return self.__state

    def toggle(self) -> None:
        self.__state = not self.__state

@dataclass
class GameState:
    __game_alive: bool = field(default=False)
    __game_pauser: GamePauser = field(default_factory = GamePauser)
    __ui: UI = field(default_factory = UI)

    def makeGameAlive(self) -> None:
        self.__game_alive = True

    def isAlive(self) -> bool:
        return self.__game_alive
    
    def kill(self) -> None:
        self.__game_alive = False

    def updateUi(self, player: Player):
        self.__ui.display(player)

    def getGamePauser(self) -> GamePauser:
        return self.__game_pauser

    def toggleGameState(self) -> None:
        self.__game_pauser.toggle()        

    def showMenu(self) -> None:
        self.__ui.toggleMenu()
        self.toggleGameState()