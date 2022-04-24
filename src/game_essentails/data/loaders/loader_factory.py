from functools import lru_cache
from typing import Any

from . import DATA_LOADERS
from .data_loader import DataLoader


class DataLoaderFactory:
    @staticmethod
    @lru_cache
    def getLoaderTo(file_extension: str) -> DataLoader[Any]:
        if file_extension not in DATA_LOADERS.keys():
            raise NotImplementedError(f"*{file_extension}* file extension is not supported!")

        return DATA_LOADERS[file_extension]()
