import logging
import time

from jivago.lang.annotations import BackgroundWorker, Override, Inject
from jivago.lang.runnable import Runnable

from vision_project.detection.sheet_detector import SheetDetector
from vision_project.drawing.drawing import Drawing
from vision_project.projection.projector_window import ProjectorWindow
from vision_project.vision.coordinate_translator import CoordinateTranslator
from vision_project.vision.image_repository import ImageRepository


@BackgroundWorker
class DrawingUpdateWorker(Runnable):
    LOGGER = logging.getLogger("DrawingUpdateWorker")

    @Inject
    def __init__(self, drawing: Drawing, image_repository: ImageRepository, sheet_detector: SheetDetector,
                 projector_window: ProjectorWindow, coordinate_translator: CoordinateTranslator):
        self.coordinate_translator = coordinate_translator
        self.projector_window = projector_window
        self.sheet_detector = sheet_detector
        self.image_repository = image_repository
        self.drawing = drawing
        self.should_exit = False

    @Override
    def run(self):
        while not self.should_exit:
            try:
                image = self.image_repository.get_next_image()

                sheets = self.sheet_detector.find_sheets(image)
                self.projector_window.clear_canvas()
                for sheet in sheets:
                    lines = self.drawing.get_lines()
                    for start, end in lines:
                        start_camera_coords, end_camera_coords = sheet.calculate_offset(start), sheet.calculate_offset(
                            end)

                        self.projector_window.draw_line(
                            self.coordinate_translator.to_projector(start_camera_coords),
                            self.coordinate_translator.to_projector(end_camera_coords)
                        )

            except Exception as e:
                self.LOGGER.warning(f"Unknown error while redrawing. {e}")
            finally:
                time.sleep(0.25)

    def cleanup(self):
        self.should_exit = True
