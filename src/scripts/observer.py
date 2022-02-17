from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from pygame.event import Event

#region ObserverMsg
class ObserverMsg:
    @property
    @abstractmethod
    def value(self) -> object:...

    def __str__(self) -> str:
        return str(self.value)

@dataclass
class StrObserverMsg(ObserverMsg):
    _value: str = field(default = "")

    @property
    def value(self) -> str:
        return self._value

@dataclass
class EventObserverMsg(ObserverMsg):
    _value: Event

    @property
    def value(self) -> Event:
        return self._value
#endregion

class Observer(ABC):
    @abstractmethod
    def updateByNotification(self, msg: ObserverMsg) -> None:...

class CallbackObserver(Observer):
    def __init__(self, callback: Callable[[ObserverMsg], Any]):
        self.__callback = callback

    def updateByNotification(self, msg: ObserverMsg) -> None:
        self.__callback(msg)

class KeyObserver(Observer):...
    # def updateByNotification(self, msg: ObserverMsg) -> None:
    #     print(f"I {self} have been updated with this msg: {msg}")

class Subject(ABC):
    def __init__(self, observers: Dict[int, List[Observer]] = dict()):
        self._observers: Dict[int, List[Observer]] = observers

    @abstractmethod
    def attach(self, observer: Observer, event: int) -> None:...

    @abstractmethod
    def detach(self, observer: Observer) -> None:...

    @abstractmethod
    def detachFrom(self, observer: Observer, event: int) -> None:...

    @abstractmethod
    def notify(self, event: int, msg: Optional[str] = None) -> None:...

class KeySubject(Subject):
    def attach(self, observer: Observer, event: int) -> None:
        self._observers[event] = [*self._observers.get(event, []), observer]

    def detach(self, observer: Observer) -> None:
        for event, attached_observer_list in self._observers.items():
            if observer in attached_observer_list:
                self._observers[event].remove(observer)

    def detachFrom(self, observer: Observer, event: int):
        if event not in self._observers.keys():
            raise KeyError(f"{event} is not present between the keys of the events")

        if observer not in self._observers[event]:
            raise ValueError(f"The given event's list does not contain the given observer!")

        self._observers[event].remove(observer)

    def notify(self, event: int, msg: ObserverMsg = StrObserverMsg()) -> None:
        if not event in self._observers.keys():
            raise KeyError(f"{event} is not present between the keys of the events")
        
        for attached_observer in self._observers[event]:
            attached_observer.updateByNotification(msg)

    def getEventList(self) -> List[int]:
        return self._observers.keys()

if __name__ == "__main__":
    # Testing
    import pygame

    key_observers = [KeyObserver() for _ in range(3)]
    key_subject = KeySubject()
    
    key_subject.attach(key_observers[0], pygame.K_ESCAPE)
    key_subject.attach(key_observers[1], pygame.K_ESCAPE)
    key_subject.attach(key_observers[2], pygame.K_0)
    key_subject.attach(key_observers[2], pygame.K_ESCAPE)

    key_subject.notify(pygame.K_ESCAPE)

    key_subject.detach(key_observers[2])
    print("remove")

    key_subject.notify(pygame.K_ESCAPE)
    key_subject.notify(pygame.K_0)

    key_subject.detachFrom(key_observers[0], pygame.K_ESCAPE)
    print("remove from")

    key_subject.notify(pygame.K_ESCAPE)
