from dataclasses import dataclass
from . base import SingleValueData


@dataclass
class HitboxOffset(SingleValueData):
    value: int