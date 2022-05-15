from csv import reader
from os import walk
from pathlib import Path
from typing import List

from pygame.surface import Surface

from scripts.image_provider import image_provider


def import_csv_layout(path: str) -> List[List[str]]:
    terrain_map: List[List[str]] = []
    with open(path) as level_map:
        layout = reader(level_map,delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path: str) -> List[Surface]:
    surface_list: List[Surface] = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = image_provider.provideWithAlphaConvert(Path(full_path))
            surface_list.append(image_surf)

    return surface_list
