from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional, SupportsIndex


@dataclass
class Folder:
    __allowed_file_formats__ = (".jpg", ".png")

    sprites: List[Path] = field(default_factory = list)

    def __getitem__(self, __i: SupportsIndex) -> Path:
        return self.sprites[__i]

@dataclass
class GraphicsFolder:
    attack: Optional[Folder] = field(default = None)
    idle: Optional[Folder] = field(default = None)
    move: Optional[Folder] = field(default = None)

    def __setitem__(self, param_key: str, value: Any) -> None:
        self.__dict__[param_key] = value

def obtain_folder_content(folder_path: Path) -> GraphicsFolder:
    if not folder_path.exists() or not folder_path.is_dir():
        raise AttributeError(f"*{folder_path}* does not exist or not a folder!")

    result = GraphicsFolder()

    for needed_folder_name in GraphicsFolder.__annotations__:
        optional_sub_folder = folder_path.joinpath(needed_folder_name)

        if optional_sub_folder.exists():
            # check for files
            sprites: List[Path] = list()
            for sub_folder_file in optional_sub_folder.iterdir():
                if not sub_folder_file.is_file(): continue

                if sub_folder_file.suffix in Folder.__allowed_file_formats__:
                    sprites.append(sub_folder_file)
            
            result[needed_folder_name] = Folder(sprites)

    return result
