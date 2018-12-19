from typing import List

from jivago.lang.annotations import Serializable


@Serializable
class LineModel(object):
    def __init__(self, start: List[int], end: List[int]):
        self.start = start
        self.end = end


@Serializable
class DrawingModel(object):
    lines: List[LineModel]

    def __init__(self, lines: List[LineModel]):
        self.lines = lines


@Serializable
class TextModel(object):
    text: str
    center: List[int]
