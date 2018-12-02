from math import cos, sin, radians
from typing import List

import cv2

from vision_project.detection.sheet import Sheet
from vision_project.vision import colourspace
from vision_project.vision.image import Image
from vision_project.vision.util import CameraCoordinate


class SheetDetector(object):

    def find_sheets(self, image: Image) -> List[Sheet]:
        hsv_image = colourspace.bgr_to_hsv(image)
        white_mask = hsv_image.get_in_range_mask([0, 0, 150], [180, 255, 235])

        im, contours, hier = cv2.findContours(white_mask.matrix, cv2.RETR_TREE,
                                              cv2.CHAIN_APPROX_SIMPLE)

        sheets = []

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w > 100 and h > 100:
                center_xy, width_height, angle = cv2.minAreaRect(c)

                corner = CameraCoordinate(
                    center_xy[0] - (width_height[0] * cos(radians(angle)) - width_height[1] * sin(radians(angle + 180))) / 2,
                    center_xy[1] + (width_height[0] * sin(radians(angle + 180)) - width_height[1] * cos(radians(angle + 180))) / 2
                )

                other_corner = corner + CameraCoordinate(
                    int((width_height[0] * cos(radians(angle)) - width_height[1] * sin(radians(angle + 180)))),
                    int(-(width_height[0] * sin(radians(angle + 180)) - width_height[1] * cos(radians(angle + 180))))
                )

                sheets.append(Sheet(corner, other_corner))

        return sheets
