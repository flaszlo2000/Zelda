import json
from abc import ABC, abstractmethod
from typing import List, overload
from pathlib import Path

from game_essentails.data.models.base import GameData
from game_essentails.data.models.monster import MonsterData


class DataLoader(ABC):
    #region loadData overload
    @overload
    def loadData(self, file_path: Path, dataclass_to_represent: MonsterData) -> List[MonsterData]:...
    #endregion

    @abstractmethod
    def loadData(self, file_path: Path, dataclass_to_represent: GameData) -> List[GameData]:...

class JsonDataLoader(DataLoader):
    def loadData(self, file_path: Path, dataclass_to_represent: GameData) -> List[GameData]:
        result = list()

        with open(file_path, 'r') as file:
            data = json.load(file)
            
            for entity_name, entity_data in data.items():
                current_entity = dataclass_to_represent(entity_name, **entity_data)
                result.append(current_entity)

        return result