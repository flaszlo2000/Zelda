from dataclasses import dataclass
from . base import GameData


@dataclass
class MonsterData(GameData):
    # basic stats
    health: int
    damage: int
    resistance: int
    speed: int

    # attack related stats
    exp: int
    attack_type: str
    attack_radius: int

    # ai
    notice_radius: int

    # source related infos
    attack_sound_src: str
