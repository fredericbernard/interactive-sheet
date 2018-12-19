import unittest
from unittest import mock

from vision_project.detection.finger_detector import FingerDetector
from vision_project.detection.sheet_detector import SheetDetector
from vision_project.drawing.drawing import Drawing
from vision_project.drawing.finger_drawing_worker import FingerDrawingWorker
from vision_project.vision.image_repository import ImageRepository


class FingerDrawingWorkerTest(unittest.TestCase):

    def setUp(self):
        self.image_repository: ImageRepository = mock.create_autospec(ImageRepository)
        self.finger_detector: FingerDetector = mock.create_autospec(FingerDetector)
        self.sheet_detector: SheetDetector = mock.create_autospec(SheetDetector)
        self.drawing: Drawing = mock.create_autospec(Drawing)
        self.finger_drawing_worker: FingerDrawingWorker = FingerDrawingWorker(self.image_repository, self.sheet_detector
                                                                              , self.drawing, self.finger_detector)

    def test_givenNoFingersDetected_whenDrawing_thenNothingIsDrawned(self):
        self.finger_detector.find_finger(None).return_value = None

        self.finger_drawing_worker.run()
        self.finger_drawing_worker.cleanup()

        self.drawing.draw_line().assert_not_called()
