from pygame.constants import USEREVENT
from scripts.observer import KeySubject

# Custom Event constants for extend the options of pygame.constants
# NOTE: use 10_xxx prefix to avoid id confusion


class EventId:
    static_c = USEREVENT

    def __init__(self):
        self._value: int = EventId.static_c
        EventId.static_c += 1

    def __int__(self) -> int:
        return self._value

SAVE = EventId()
LOAD = EventId()
LOAD_REQ = EventId() # request to send out a specific saved value
MAIN_SOUND_TOGGLE = EventId()
SAVE_GAME = EventId()
LOAD_GAME = EventId()
PAUSE_TOGGLE = EventId()

HOVER_ON = EventId() # see HoverUiElement
HOVER_OFF = EventId() # see HoverUiElemen
HOVER_TICK = EventId()


key_broadcast_subject = KeySubject()
