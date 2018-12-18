import unittest

from vision_project.detection.sheet import Sheet, WIDTH_MM, HEIGHT_MM
from vision_project.vision.util import CameraCoordinate, RelativeWorldCoordinate

ORIGIN = CameraCoordinate(588, 437)
OPPOSITE = CameraCoordinate(538, 216)
MIDDLE_OF_SHEET = CameraCoordinate(((OPPOSITE.x - ORIGIN.x) / 2) + ORIGIN.x, ((ORIGIN.y - OPPOSITE.y) / 2) + OPPOSITE.y)
POINT_OUT_OF_SHEET = CameraCoordinate(ORIGIN.x + 10, ORIGIN.y + 10)


class SheetTest(unittest.TestCase):

    def setUp(self):
        self.sheet = Sheet(ORIGIN, OPPOSITE)

    def test_whenGettingCameraPosition_thenCalculateOffsetUsingRelativeCoordinate(self):
        translated_coordinates = self.sheet.calculate_offset(RelativeWorldCoordinate(10, 0))

        self.assertTrue(translated_coordinates.x > ORIGIN.x)
        self.assertTrue(ORIGIN.y - 7 < translated_coordinates.y < ORIGIN.y + 7) # :woman_shrugging: Ça a l'air de marcher.

    def test_givenUsLetterSize_whenGettingCameraPositionOffset_thenPositionIsAtOppositeCorner(self):
        offset = self.sheet.calculate_offset(RelativeWorldCoordinate(WIDTH_MM, HEIGHT_MM))

        self.assertTrue(offset.isclose(self.sheet.opposite_corner))

    def test_givenCameraCoordinateNotOnSheet_whenConvertingToRelativeCoordinate_thenNone(self):
        relative_coordinate = self.sheet.to_relative_coordinate(POINT_OUT_OF_SHEET)

        self.assertIsNone(relative_coordinate)

    def test_givenCameraCoordinateOnSheet_whenConvertingToRelativeCoordinate_thenRelativeCoordinateComputed(self):
        relative_coordinate = self.sheet.to_relative_coordinate(MIDDLE_OF_SHEET)

        expected_coordinate = RelativeWorldCoordinate(WIDTH_MM / 2, HEIGHT_MM / 2)
        self.assertTrue(expected_coordinate.is_close(relative_coordinate, delta=0.65))
