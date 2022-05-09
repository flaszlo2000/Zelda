from typing import Any, Callable, Dict, Protocol

from game_essentails.events import LOAD, LOAD_REQ, SAVE, key_broadcast_subject
from scripts.observer import (CallbackObserver, KeyValueObserverMsg,
                              StrObserverMsg)

from .constants import MUSIC_ON_STARTUP


class ISaveSystemAdapter(Protocol):
    def getMusicOnStartUpState(self) -> bool:...
    def updateMusicOnStartUp(self, state: bool) -> None:...

class DbRequestHandler:
    def __init__(self, master: ISaveSystemAdapter) -> None:
        self.subscribeToEvents()
        
        self.__LOAD_REQ_DICT: Dict[str, Callable[..., Any]] = {
            MUSIC_ON_STARTUP: master.getMusicOnStartUpState
        }

        self.__SAVE_DICT: Dict[str, Callable[..., Any]] = {
            MUSIC_ON_STARTUP: master.updateMusicOnStartUp
        }

    def subscribeToEvents(self) -> None:
        key_broadcast_subject.attach(
            CallbackObserver[StrObserverMsg](self.__handleRequest), LOAD_REQ
        )
        
        key_broadcast_subject.attach(
            CallbackObserver[KeyValueObserverMsg](self.handleSave), SAVE
        )

    def __handleRequest(self, msg: StrObserverMsg) -> None:
        # TODO: error handling
        result = self.__LOAD_REQ_DICT[str(msg)]()
        key_broadcast_subject.notify(LOAD, StrObserverMsg(result))


    def handleSave(self, msg: KeyValueObserverMsg) -> None:
        # TODO: error handling
        self.__SAVE_DICT[msg.key](msg.data)
