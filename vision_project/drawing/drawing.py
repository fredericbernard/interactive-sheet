import threading
from typing import List, Tuple

from jivago.lang.registry import Component, Singleton

from vision_project.vision.util import RelativeWorldCoordinate


@Component
@Singleton
class Drawing(object):

    def __init__(self):
        self._lock = threading.Lock()
        self.lines: List[Tuple[RelativeWorldCoordinate, RelativeWorldCoordinate]] = []
        self.texts: List[Tuple[str, RelativeWorldCoordinate]] = []
        self.locked = False

    def draw_line(self, start: RelativeWorldCoordinate, end: RelativeWorldCoordinate):
        with self._lock:
            self.lines.append((start, end))

    def get_lines(self) -> List[Tuple[RelativeWorldCoordinate, RelativeWorldCoordinate]]:
        return self.lines

    def add_text(self, text: str, center: RelativeWorldCoordinate):
        with self._lock:
            self.texts.append((text, center))

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def get_texts(self):
        return self.texts

    def clear(self):
        with self._lock:
            self.lines = []
