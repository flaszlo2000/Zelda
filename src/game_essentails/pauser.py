from dataclasses import dataclass, field


@dataclass
class GamePauser:
    __state: bool = field(default = False) 

    def isPaused(self) -> bool:
        return self.__state

    def toggle(self) -> None:
        self.__state = not self.__state
