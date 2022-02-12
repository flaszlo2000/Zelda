from typing import Dict, Union
from pathlib import Path
from pygame import Surface
from pygame.image import load as pygame_image_load


class ImageProvider:
    def __init__(self, initial_images: Dict[Path, Surface] = dict()):
        self.__images = initial_images # NOTE: these images are not conerted

    @staticmethod
    def _checkPathType(image_path: Union[str, Path]) -> Path:
        result = image_path

        if not isinstance(image_path, Path):
            result = Path(image_path)

        return result

    # TODO: make this cached
    def provide(self, image_path: Union[str, Path]) -> Surface:
        image_path = ImageProvider._checkPathType(image_path)

        if image_path in self.__images.keys():
            return self.__images[image_path]

        if not image_path.exists():
            raise FileExistsError(f"*{image_path}* does not exist!")

        image = pygame_image_load(image_path)
        self.__images[image_path] = image

        return self.__images[image_path]

    def provideWithConvert(self, image_path: Union[str, Path]) -> Surface:
        return self.provide(image_path).convert()

    def provideWithAlphaConvert(self, image_path: Union[str, Path]) -> Surface:
        return self.provide(image_path).convert_alpha()


image_provider = ImageProvider()