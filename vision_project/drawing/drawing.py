import threading
from typing import List, Tuple

from jivago.lang.registry import Component, Singleton

from vision_project.vision.util import RelativeWorldCoordinate


@Component
@Singleton
class Drawing(object):

    def __init__(self):
        self.lock = threading.Lock()
        self.lines: List[Tuple[RelativeWorldCoordinate, RelativeWorldCoordinate]] = []

    def draw_line(self, start: RelativeWorldCoordinate, end: RelativeWorldCoordinate):
        with self.lock:
            self.lines.append((start, end))

    def get_lines(self) -> List[Tuple[RelativeWorldCoordinate, RelativeWorldCoordinate]]:
        return self.lines

    def clear(self):
        with self.lock:
            self.lines = []
