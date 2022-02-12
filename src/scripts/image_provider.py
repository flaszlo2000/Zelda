from typing import Dict
from pathlib import Path
from pygame import Surface
from pygame.image import load as pygame_image_load


class ImageProvider:
    def __init__(self, initial_images: Dict[Path, Surface] = {}):
        self.__images = initial_images

    def provide(self, image_path: Path) -> Surface:
        if image_path in self.__images.keys():
            return self.__images[image_path]

        if not image_path.exists():
            raise FileExistsError(f"*{image_path}* does not exist!")

        image = pygame_image_load(image_path).convert()
        self.__images[image_path] = image


image_provider = ImageProvider()