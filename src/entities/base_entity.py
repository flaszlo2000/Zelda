class BaseEntity:
    def __init__(self, is_player: bool):
        self._is_player = is_player

    def isPlayer(self) -> bool:
        return self._is_player