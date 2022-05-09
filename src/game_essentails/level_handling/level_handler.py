from dataclasses import dataclass, field
from typing import Optional

from game_essentails.save_handling.main import SaveSystemAdapter
from level import Level

from ..game_state import GameState


@dataclass
class LevelHandler:
    _level: Level
    _game_state: GameState = field(default_factory = GameState)
    save_handler: SaveSystemAdapter = field(default_factory = SaveSystemAdapter)

    def updateLevel(self) -> None:
        # NOTE: this is called from the main loop so basically you could add input or something similar
        # but consider to use EventObserver instead
        self._level.run() # this creates the map and the player with it
        self._game_state.updateUi(self._level.getPlayer())

    def changeLevel(self, new_level: Level) -> Optional[bool]:
        print("called")
        self._level.getPlayer().testOuter()
        return None
    
    def toggleMenu(self) -> None:
        self._game_state.toggleGameState()
