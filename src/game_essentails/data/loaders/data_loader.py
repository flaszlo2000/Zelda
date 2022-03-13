from distutils.command.config import config
import json, configparser
from abc import ABC, abstractmethod
from typing import List, overload
from pathlib import Path

from game_essentails.data.models.base import GameData
from game_essentails.data.models import (
    MonsterData, WeaponData, MagicData
)


class DataLoader(ABC):
    #region loadData overload
    @overload
    def loadData(self, file_path: Path, dataclass_to_represent: MonsterData) -> List[MonsterData]:...
    @overload
    def loadData(self, file_path: Path, dataclass_to_represent: WeaponData) -> List[WeaponData]:...
    @overload
    def loadData(self, file_path: Path, dataclass_to_represent: MagicData) -> List[MagicData]:... 
    #endregion

    @abstractmethod
    def loadData(self, file_path: Path, dataclass_to_represent: GameData) -> List[GameData]:...

class JsonDataLoader(DataLoader):
    def loadData(self, file_path: Path, dataclass_to_represent: GameData) -> List[GameData]:
        result = list()

        with open(file_path, 'r') as file:
            data = json.load(file)

            for entity_name, entity_data in data.items():
                try:
                    current_entity = dataclass_to_represent(entity_name, **entity_data)
                    result.append(current_entity)
                except TypeError as exc:
                    # if the loaded setting file has any missing parameters
                    print(f"[*] ERROR: data loading: {dataclass_to_represent=}: {exc} at {file_path}")

        return result

class ConfDataLoader(DataLoader):
    @staticmethod
    def clearValue(input_value: str) -> str:
        "Removes surrounding ' or \" chars generated by ConfigParser"
        return input_value[1:-1]

    "This is a representation of a conf or ini file"
    def loadData(self, file_path: Path, dataclass_to_represent: GameData) -> List[GameData]:
        result = list()
        config_parser = configparser.ConfigParser()
        config_parser.read(file_path)

        for section_name in config_parser.sections():
            for key, _value in config_parser.items(section_name):
                is_numeric = _value.isnumeric()

                if is_numeric:
                    _value = int(_value)
                else:
                    if _value.startswith("'") or _value.endswith('"'):
                        # the ConfigParser will read strings like this '"apple"' or "'apple'" so we check this and if needed then remove
                        _value = ConfDataLoader.clearValue(_value)

                result.append(dataclass_to_represent(name = key, value = _value, is_numeric = is_numeric))

        return result

# TODO: toml, yaml ?