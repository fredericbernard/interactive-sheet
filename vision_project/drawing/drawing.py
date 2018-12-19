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
        self.texts: List[Tuple[str, RelativeWorldCoordinate]] = []

    def draw_line(self, start: RelativeWorldCoordinate, end: RelativeWorldCoordinate):
        with self.lock:
            self.lines.append((start, end))

    def get_lines(self) -> List[Tuple[RelativeWorldCoordinate, RelativeWorldCoordinate]]:
        return self.lines

    def add_text(self, text: str, center: RelativeWorldCoordinate):
        with self.lock:
            self.texts.append((text, center))

    def get_texts(self):
        return self.texts

    def clear(self):
        with self.lock:
            self.lines = []
