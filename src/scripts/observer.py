from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import (Any, Callable, Dict, Generic, List, Optional, SupportsInt,
                    Tuple, TypeVar)

from pygame.event import Event


#region ObserverMsg
class ObserverMsg:
    @property
    @abstractmethod
    def value(self) -> object:...

    def __str__(self) -> str:
        return str(self.value)

class StrObserverMsg(str, ObserverMsg):
    @property
    def value(self) -> str:
        return super().__str__() # NOTE: thx for the __mro__

@dataclass
class EventObserverMsg(ObserverMsg):
    _value: Event

    @property
    def value(self) -> Event:
        return self._value

@dataclass
class KeyValueObserverMsg(ObserverMsg):
    key: Any
    data: Any

    @property
    def value(self) -> Tuple[Any, Any]:
        return (self.key, self.data)
#endregion

T = TypeVar("T", bound=ObserverMsg)
class Observer(ABC, Generic[T]):
    @abstractmethod
    def updateByNotification(self, msg: T) -> None:...

class CallbackObserver(Observer[T]):
    def __init__(self, callback: Callable[[T], Any]):
        self.__callback = callback

    def updateByNotification(self, msg: T) -> None:
        self.__callback(msg)

class KeyObserver(Observer[T]):...
    # def updateByNotification(self, msg: ObserverMsg) -> None:
    #     print(f"I {self} have been updated with this msg: {msg}")

class Subject(ABC):
    def __init__(self, observers: Optional[Dict[SupportsInt, List[Observer[Any]]]] = None):
        self._observers: Dict[SupportsInt, List[Observer[Any]]] = observers if observers is not None else dict()

    @abstractmethod
    def attach(self, observer: Observer[Any], event: SupportsInt) -> None:...

    @abstractmethod
    def detach(self, observer: Observer[Any]) -> None:...

    @abstractmethod
    def detachFrom(self, observer: Observer[Any], event: SupportsInt) -> None:...

    @abstractmethod
    def notify(self, event: SupportsInt, msg: Optional[ObserverMsg] = None) -> None:...

class KeySubject(Subject):
    def attach(self, observer: Observer[Any], event: SupportsInt) -> None:
        self._observers[event] = [*self._observers.get(event, []), observer]

    def detach(self, observer: Observer[Any]) -> None:
        for event, attached_observer_list in self._observers.items():
            if observer in attached_observer_list:
                self._observers[event].remove(observer)

    def detachFrom(self, observer: Observer[Any], event: SupportsInt):
        if event not in self._observers.keys():
            raise KeyError(f"{event} is not present between the keys of the events")

        if observer not in self._observers[event]:
            raise ValueError(f"The given event's list does not contain the given observer!")

        self._observers[event].remove(observer)

    def notify(self, event: SupportsInt, msg: Optional[ObserverMsg] = None) -> None:
        if msg is None:
            msg = StrObserverMsg()

        if not event in self._observers.keys():
            raise KeyError(f"{event} is not present between the keys of the events")
        
        for attached_observer in self._observers[event]:
            attached_observer.updateByNotification(msg)

    def getEventList(self) -> List[int]:
        return list(map(int, self._observers.keys()))
