import pygame
from typing import List, Callable

from scripts.observer import KeyObserver, EventObserverMsg
from game_essentails.events import key_broadcast_subject


class Button(pygame.Rect, KeyObserver):
    def __init__(self, parent_is_visible: Callable[[], bool], command: Callable, rect_pos: List[int], *args, **kwargs):
        super().__init__(*rect_pos, *args, **kwargs)

        self.__clicked = False
        self.__parent_is_visible = parent_is_visible
        self._command = command

        self._colors = ["#ff0000", "#00ff00"]

        self._registerForKeys()

    def _registerForKeys(self) -> None:
        key_broadcast_subject.attach(self, pygame.MOUSEBUTTONDOWN)
        key_broadcast_subject.attach(self, pygame.MOUSEBUTTONUP)

    def updateByNotification(self, msg: EventObserverMsg) -> None:
        if self.__parent_is_visible():
            if msg.value.type == pygame.MOUSEBUTTONDOWN:
                if self.collidepoint(msg.value.pos):
                    self.__clicked = True
            else:
                if self.__clicked:
                    if self.collidepoint(msg.value.pos):
                        self._command()

                    self.__clicked = False

    def getStateColor(self) -> str:
        return self._colors[self.__clicked]

    def changeColors(self, new_colors: List[str]) -> None:
        if len(new_colors) != 2: raise ValueError("Incorrect parameter, the new_colors list must contain two elements!")

        self._colors = new_colors

    def changeCommand(self, new_command: Callable) -> None:
        self._command = new_command

class ButtonFactory:
    "Factory to create more than one Buttons within the same UI element"
    def __init__(self, parent_is_visible: Callable[[], bool]):
        self.__parent_is_visible = parent_is_visible

    def create(self, command: Callable, rect_pos: List[int], *args, **kwargs) -> Button:
        return Button(self.__parent_is_visible, command, rect_pos, *args, **kwargs)
