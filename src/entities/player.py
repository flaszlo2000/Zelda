from . base_entity import BaseEntity


class Player(BaseEntity):
    def __init__(self):
        super().__init__(is_player = True)