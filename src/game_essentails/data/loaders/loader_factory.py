from functools import lru_cache

from . data_loader import DataLoader
from .  import DATA_LOADERS


class DataLoaderFactory:
    @staticmethod
    @lru_cache
    def getLoaderTo(file_extension: str) -> DataLoader:
        if file_extension not in DATA_LOADERS.keys():
            raise NotImplementedError(f"*{file_extension}* file extension is not supported!")

        return DATA_LOADERS[file_extension]()