from dataclasses import dataclass, field
from pathlib import Path
from os import listdir
from typing import Dict, List, Any

from game_essentails.data.models.base import GameData, SingleValueData
from game_essentails.data.loaders.loader_factory import DataLoaderFactory
from game_essentails.data.models import HANDLER_MAP


@dataclass
class SettingLoader:
    settings_path: Path
    __settings: Dict[str, List[GameData]] = field(default_factory = dict)

    def importSettings(self) -> None:
        for file_name in listdir(self.settings_path):
            file_extension = file_name.split('.')[-1]
            file_name_without_ext = file_name.replace(f".{file_extension}", "")
            try:
                data_loader = DataLoaderFactory.getLoaderTo(file_extension)
            except NotImplementedError as exc:
                print(f"[*] ERROR: Loading settings: {exc}")
                continue

            if file_name_without_ext not in HANDLER_MAP.keys():
                raise NotImplementedError(f"{file_name_without_ext} is not representable! Extend HANDLER_MAP") # NOTE: to avoid this extend game_essentails/models/__init__.py 's HANDLER_MAP

            self.__settings[file_name_without_ext.lower()] = data_loader.loadData(Path(f"{self.settings_path}/{file_name}"), HANDLER_MAP[file_name_without_ext])

    def __getitem__(self, __name: str) -> List[GameData]:
        return self.__settings[__name]

    def __getSingleValueDataDict(self) -> Dict[str, List[SingleValueData]]:
        result: Dict[str, List[SingleValueData]] = dict()

        for key, setting_list in self.__settings.items():
            if issubclass(type(setting_list[0]), SingleValueData):
                result[key] = setting_list

        return result

    def getSingleValueFrom(self, _from: str, __name: str) -> Any:
        "Generalized method to access single value settings"
        single_value_settings: Dict[str, List[SingleValueData]] = self.__getSingleValueDataDict()

        for single_value_setting in single_value_settings[_from]:
            if single_value_setting.name == __name:
                return single_value_setting.value
        else:
            raise KeyError(f"[*] ERROR: search for setting: *{__name}* was not found in *{_from}*!")


if __name__ == "__main__":
    setting_loader = SettingLoader(Path("./settings"))
    setting_loader.importSettings()

    print(setting_loader.getSingleValueFrom("common", "ui_font"))
    print(setting_loader.getSingleValueFrom("hitbox_offset", "player"))