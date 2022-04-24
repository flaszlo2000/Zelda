from typing import Any, Dict, Type

from .data_loader import ConfDataLoader, DataLoader, JsonDataLoader

# this is needed to be able to list supported settting files
# has been separated because continuous circular import errors


DATA_LOADERS: Dict[str, Type[DataLoader[Any]]] = {
    "json": JsonDataLoader,
    "conf": ConfDataLoader,
    "ini": ConfDataLoader
}
