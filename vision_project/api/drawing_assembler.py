from typing import Tuple

from jivago.lang.registry import Component
from jivago.lang.stream import Stream

from vision_project.api.drawing_model import DrawingModel, LineModel
from vision_project.drawing.drawing import Drawing
from vision_project.vision.util import RelativeWorldCoordinate


@Component
class DrawingAssembler(object):

    def to_model(self, drawing: Drawing) -> DrawingModel:
        return DrawingModel(
            Stream(drawing.get_lines()).map(lambda l: self._to_line_model(l)).toList()
        )

    def _to_line_model(self, line: Tuple[RelativeWorldCoordinate, RelativeWorldCoordinate]) -> LineModel:
        return LineModel(
            [line[0].y, line[0].x],
            [line[1].y, line[1].x]
        )

    def from_line_model(self, line_model: LineModel) -> Tuple[RelativeWorldCoordinate, RelativeWorldCoordinate]:
        return (RelativeWorldCoordinate(line_model.start[1], line_model.start[0]),
                RelativeWorldCoordinate(line_model.end[1], line_model.end[0]))
