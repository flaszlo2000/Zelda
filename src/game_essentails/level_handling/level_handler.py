from dataclasses import dataclass, field
from typing import Optional

from game_essentails.events import LOAD_GAME, SAVE_GAME, key_broadcast_subject
from game_essentails.save_handling.main import SaveSystemAdapter
from level import Level
from pygame.rect import Rect
from scripts.observer import CallbackObserver, StrObserverMsg

from ..game_state import GameState


@dataclass
class LevelHandler:
    _level: Level
    _game_state: GameState = field(default_factory = GameState)
    save_handler: SaveSystemAdapter = field(default_factory = SaveSystemAdapter)

    def __post_init__(self) -> None:
        save_game_callback = CallbackObserver[StrObserverMsg](self.saveGame)
        key_broadcast_subject.attach(save_game_callback, SAVE_GAME)

        load_game_callback = CallbackObserver[StrObserverMsg](self.loadGame)
        key_broadcast_subject.attach(load_game_callback, LOAD_GAME)

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

    def saveGame(self, msg: StrObserverMsg) -> None:
        #! FIXME: save the whole game, not just the position of the player
        player = self._level.getPlayer()
        player_pos = (player.rect.left, player.rect.top, player.rect.width, player.rect.height)

        self.save_handler.savePlayerPosition(player_pos)
        print("[*] NOTE: position saved!")
    
    def loadGame(self, msg: StrObserverMsg) -> None:
        #! FIXME: save the whole game, not just the position of the player
        saved_position = self.save_handler.getPlayerPosition()
        if saved_position is None:
            print("[*] WARNING: There is no saved position!")
            return
        
        player = self._level.getPlayer()
        
        # dumpsterfire parse
        saved_pos= tuple(map(int, saved_position.replace('(', '').replace(')', '').split(", ")))
        player.moveTo(saved_pos[0], saved_pos[1])
        print("[*] NOTE: position loaded!")
