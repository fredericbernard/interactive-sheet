from math import sqrt
from typing import List

import cv2
from jivago.lang.registry import Component
from jivago.lang.stream import Stream

from vision_project.detection.sheet import Sheet
from vision_project.vision import colourspace
from vision_project.vision.image import Image
from vision_project.vision.util import CameraCoordinate


@Component
class SheetDetector(object):

    def find_sheets(self, image: Image) -> List[Sheet]:
        hsv_image = colourspace.bgr_to_hsv(image)
        white_mask = hsv_image.get_in_range_mask([0, 0, 150], [180, 255, 235])

        im, contours, hier = cv2.findContours(white_mask.matrix, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        sheets = []

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w > 100 and h > 100:
                corners = cv2.boxPoints(cv2.minAreaRect(c))

                distances = Stream.range(1, 4) \
                                .map(lambda i: (corners[i - 1], corners[i])) \
                                .map(euclidean_distance).toList() + [euclidean_distance(corners[-1], corners[0])]
                corners = Stream(corners).toList() + [corners[0]]

                length_threshold = (max(distances) + min(distances)) / 2

                opposing_corners = Stream.zip(range(1, 5), distances + distances).filter(
                    lambda _, d: d > length_threshold).map(
                    lambda i, _: corners[i]).toList()
                origin = Stream(opposing_corners).reduce([0, 0], lambda acc, e: e if e[1] > acc[1] else acc)
                opposite = Stream(opposing_corners).firstMatch(lambda e: e[0] != origin[0] or e[1] != origin[1])

                sheets.append(Sheet(CameraCoordinate(*origin), CameraCoordinate(*opposite)))

        return sheets


def euclidean_distance(first_point: list, second_point: list) -> float:
    return sqrt((first_point[0] - second_point[0]) ** 2 + (first_point[1] - second_point[1]) ** 2)
