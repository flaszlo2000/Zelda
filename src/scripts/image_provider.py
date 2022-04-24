from pathlib import Path
from typing import Dict, Union

from pygame.image import load as pygame_image_load
from pygame.surface import Surface


class ImageProvider:
    def __init__(self, initial_images: Dict[Path, Surface] = dict()):
        self.__images = initial_images # NOTE: these images are not converted

    @staticmethod
    def _checkPathType(image_path: Union[str, Path]) -> Path:
        if not isinstance(image_path, Path):
            image_path = Path(image_path)

        return image_path

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
