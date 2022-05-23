from dataclasses import dataclass, field
from os import listdir
from pathlib import Path
from typing import Any, Dict, List, cast

from game_essentails.data.loaders.loader_factory import DataLoaderFactory
from game_essentails.data.models import HANDLER_MAP
from game_essentails.data.models.base import GameData, SingleValueData


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
                result[key] = cast(List[SingleValueData], setting_list)

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
    from pprint import pprint
    setting_loader = SettingLoader(Path("./settings"))
    setting_loader.importSettings()

    # tests
    # print(setting_loader.getSingleValueFrom("common", "ui_font"))
    # print(setting_loader.getSingleValueFrom("hitbox_offset", "player"))
    pprint(setting_loader["players"])
    # for content in setting_loader["monsters"]:
    #     print(content)

    # for effect in setting_loader["effects"]:
    #     pprint(effect)
