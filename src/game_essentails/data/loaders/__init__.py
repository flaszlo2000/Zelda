from typing import Dict
from . data_loader import DataLoader, JsonDataLoader


# this is needed to be able to list supported settting files
# has been separated because continuous circular import errors
DATA_LOADERS: Dict[str, DataLoader] = {
    "json": JsonDataLoader
}