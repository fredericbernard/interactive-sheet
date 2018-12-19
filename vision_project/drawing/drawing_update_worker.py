import logging
import time
from typing import List, Tuple

from jivago.lang.annotations import BackgroundWorker, Override, Inject
from jivago.lang.runnable import Runnable
from jivago.lang.stream import Stream

from vision_project.detection.sheet import Sheet
from vision_project.detection.sheet_detector import SheetDetector
from vision_project.drawing.drawing import Drawing
from vision_project.projection.projector_window import ProjectorWindow
from vision_project.vision.coordinate_translator import CoordinateTranslator
from vision_project.vision.image_repository import ImageRepository
from vision_project.vision.util import RelativeWorldCoordinate


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
        last_sheets: List[Sheet] = []
        last_number_of_lines = 0
        while not self.should_exit:
            try:
                image = self.image_repository.get_next_image()
                sheets = self.sheet_detector.find_sheets(image)
                if self._should_refresh_sheets(sheets, last_sheets, last_number_of_lines):
                    self.projector_window.clear_canvas()
                    self._refresh_sheets(sheets)
                last_sheets = sheets
                last_number_of_lines = len(self.drawing.get_lines())

            except Exception as e:
                self.LOGGER.warning(f"Unknown error while redrawing. {e}")
            finally:
                # pass
                time.sleep(0.1)

    def _should_refresh_sheets(self, sheets: List[Sheet], last_sheets: List[Sheet], last_number_of_lines: int):
        matching_sheets = Stream(last_sheets).filter(lambda last_sheet: self._is_in(last_sheet, sheets)).toList()
        if not (len(matching_sheets) == len(sheets) == len(last_sheets)
                and last_number_of_lines == len(self.drawing.get_lines())):
            return True
        return False

    def _is_in(self, sheet: Sheet, sheets: List[Sheet]):
        matching_sheet = Stream(sheets).firstMatch(lambda sheet_to_compare:
                                                   sheet.origin.isclose(sheet_to_compare.origin, 10)
                                                    and
                                                   sheet.opposite_corner.isclose(sheet_to_compare.opposite_corner, 10))
        if matching_sheet is not None:
            return True
        return False

    def _refresh_sheets(self, sheets: List[Sheet]):
        for sheet in sheets:
            lines = self.drawing.get_lines()
            self._draw_lines_on_sheet(lines, sheet)
            texts = self.drawing.get_texts()
            self._draw_texts_on_sheet(texts, sheet)

    def _draw_lines_on_sheet(self, lines: List[Tuple[RelativeWorldCoordinate, RelativeWorldCoordinate]], sheet: Sheet):
        for start, end in lines:
            start_camera_coords, end_camera_coords = sheet.calculate_offset(start), sheet.calculate_offset(end)
            self.projector_window.draw_line(
                self.coordinate_translator.to_projector(start_camera_coords),
                self.coordinate_translator.to_projector(end_camera_coords)
            )

    def _draw_texts_on_sheet(self, texts: List[Tuple[str, RelativeWorldCoordinate]], sheet: Sheet):
        for text, center in texts:
            center_camera_coords = sheet.calculate_offset(center)
            self.projector_window.add_text(texts, self.coordinate_translator.to_projector(center_camera_coords))

    def cleanup(self):
        self.should_exit = True
