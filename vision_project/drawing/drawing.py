import threading
from typing import List, Tuple

from jivago.lang.registry import Component, Singleton
from jivago.lang.stream import Stream

from vision_project.vision.coordinate_translator import CoordinateTranslator
from vision_project.vision.util import RelativeWorldCoordinate, ProjectorCoordinate, CameraCoordinate


@Component
@Singleton
class Drawing(object):

    def __init__(self):
        self.lock = threading.Lock()
        self.lines: List[Tuple[RelativeWorldCoordinate, RelativeWorldCoordinate]] = []

    def draw_line(self, start: RelativeWorldCoordinate, end: RelativeWorldCoordinate):
        with self.lock:
            self.lines.append((start, end))

    def get_lines(self, origin: CameraCoordinate, coordinate_translator: CoordinateTranslator) -> \
            List[Tuple[ProjectorCoordinate, ProjectorCoordinate]]:
        return Stream(self.lines).map(lambda start, end: (coordinate_translator.to_projector(origin, start),
                                                          coordinate_translator.to_projector(origin, end))).toList()

    def clear(self):
        with self.lock:
            self.lines = []
