from pathlib import Path

from pygame.mixer import Sound

from game_essentails.events import MAIN_SOUND_TOGGLE, key_broadcast_subject
from scripts.observer import CallbackObserver, StrObserverMsg


class SoundWithState(Sound):
    def __init__(self, file_path: Path, init_state: bool = False):
        if not file_path.exists(): raise AttributeError(f"Given *{file_path}* file does not exist!")
        super().__init__(file_path) # type: ignore # pygame
        
        self.started: bool
        self.setState(init_state)

    def checkState(self) -> None:
        if self.started:
            self.play(loops = -1)
        else:
            self.stop()

    def toggle(self) -> None:
        self.started = not self.started
        self.checkState()

    def setState(self, state: bool) -> None:
        self.started = state
        self.checkState()

class SoundHandler:
    def __init__(self):
        self.main_sound = SoundWithState(Path('./audio/main.ogg'))
        self.main_sound.set_volume(0.5)

        self._sound_toggle_observer = CallbackObserver[StrObserverMsg](lambda _: self.main_sound.toggle())
        key_broadcast_subject.attach(self._sound_toggle_observer, MAIN_SOUND_TOGGLE)

    def setMainSoundState(self, state: bool) -> None:
        self.main_sound.setState(state)
