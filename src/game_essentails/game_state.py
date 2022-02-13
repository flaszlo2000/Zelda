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
    _game_alive: bool = field(default = False)
    _game_pauser: GamePauser = field(default_factory = GamePauser)
    _ui: UI = field(default_factory = UI)

    def makeGameAlive(self) -> None:
        self._game_alive = True

    def isAlive(self) -> bool:
        return self._game_alive
    
    def kill(self) -> None:
        self._game_alive = False

    def updateUi(self, player: Player):
        self._ui.display(player)

    def getGamePauser(self) -> GamePauser:
        return self._game_pauser

    def toggleGameState(self) -> None:
        self._game_pauser.toggle()        

    def showMenu(self) -> None:
        self._ui.toggleMenu()
        self.toggleGameState()