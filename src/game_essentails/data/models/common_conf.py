from dataclasses import dataclass, field
from typing import Union

from . base import SingleValueData


@dataclass
class CommonConfData(SingleValueData):
    value: Union[str, int]
    is_numeric: bool = field(default = False)