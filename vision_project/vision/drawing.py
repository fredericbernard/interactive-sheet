from vision_project.vision.image import Image
from vision_project.vision.util import PixelCoordinate


def draw_crosshair(image: Image, target: PixelCoordinate, colour: list, *, size=10) -> None:
    for i in range(-int(size/2), int(size/2)):
        for j in range(-int(size/5), int(size/5)):
            pixel = PixelCoordinate(target.x + i, target.y + j)
            if image.contains(pixel):
                image[pixel] = colour

    for i in range(-int(size/2), int(size/2)):
        for j in range(-int(size/5), int(size/5)):
            pixel = PixelCoordinate(target.x + j, target.y + i)
            if image.contains(pixel):
                image[pixel] = colour
