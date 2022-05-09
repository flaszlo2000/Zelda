from typing import List

from game_essentails.events import LOAD, LOAD_REQ, key_broadcast_subject
from scripts.observer import CallbackObserver, StrObserverMsg


def data_request(requested_data: str) -> str:
    result: List[str] = [] # dirty trick to set value with lambda, pls don't judge me

    observer = CallbackObserver[StrObserverMsg](lambda msg: result.append(msg))  # FIXME: what if there is an other LOAD at the same time
    key_broadcast_subject.attach(observer, LOAD)
    key_broadcast_subject.notify(LOAD_REQ, StrObserverMsg(requested_data)) 
    key_broadcast_subject.detachFrom(observer, LOAD)

    return result[0]
