import unittest

from vision_project.detection.sheet import Sheet, WIDTH_MM, HEIGHT_MM
from vision_project.vision.util import CameraCoordinate, RelativeWorldCoordinate

ORIGIN = CameraCoordinate(588, 437)
OPPOSITE = CameraCoordinate(538, 216)


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
