from math import sqrt

import math

from vision_project.vision.util import CameraCoordinate, RelativeWorldCoordinate

WIDTH_MM = 215.9
HEIGHT_MM = 279.4
DIAGONAL_MM = sqrt(WIDTH_MM ** 2 + HEIGHT_MM ** 2)
SHEET_ANGLE_RAD = 0.9129


class Sheet(object):

    def __init__(self, origin: CameraCoordinate, opposite: CameraCoordinate):
        self.origin = origin
        self.opposite_corner = opposite
        self.scaling_factor = (opposite - origin).euclidean_length() / DIAGONAL_MM
        self.width_px = WIDTH_MM * self.scaling_factor
        self.height_px = HEIGHT_MM * self.scaling_factor
        self.main_axis = (opposite - origin).rotate(SHEET_ANGLE_RAD).normalize()
        self.secondary_axis = self.main_axis.rotate(-math.pi / 2)

    def calculate_offset(self, relative_coordinate: RelativeWorldCoordinate) -> CameraCoordinate:
        # Assumes sheet in portrait mode for variable naming
        horizontal_offset = self.main_axis * (relative_coordinate.x * self.scaling_factor)
        vertical_offset = self.secondary_axis * (relative_coordinate.y * self.scaling_factor)

        offset = horizontal_offset + vertical_offset

        return self.origin + offset
        print("hello")
