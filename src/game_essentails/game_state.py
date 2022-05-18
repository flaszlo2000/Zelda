from dataclasses import dataclass, field

from entities.player import Player
from ui.ui import UI

from game_essentails.effect.handler import EffectHandler

from .pauser import GamePauser


@dataclass
class GameState:
    _game_alive: bool = field(default = False)
    _game_pauser: GamePauser = field(default_factory = GamePauser)
    _ui: UI = field(default_factory = UI)
    effect_handler: EffectHandler = field(init = False)

    def __post_init__(self):
        self.effect_handler = EffectHandler(self._game_pauser)

    def makeGameAlive(self) -> None:
        self._game_alive = True

    def isAlive(self) -> bool:
        return self._game_alive
    
    def kill(self) -> None:
        self._game_alive = False

    def updateUi(self, player: Player):
        self.effect_handler.update()
        self._ui.display(player)

    def getGamePauser(self) -> GamePauser:
        return self._game_pauser

    def toggleGameState(self) -> None:
        self._game_pauser.toggle()        

    def showMenu(self) -> None:
        self._ui.toggleMenu()
        self.toggleGameState()
