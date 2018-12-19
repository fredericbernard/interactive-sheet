from typing import Tuple

from jivago.lang.registry import Component

from vision_project.api.drawing_model import TextModel
from vision_project.vision.util import RelativeWorldCoordinate


@Component
class TextAssembler(object):

    def from_text_model(self, text_model: TextModel) -> Tuple[str, RelativeWorldCoordinate]:
        return text_model.text, RelativeWorldCoordinate(text_model.center[0], text_model.center[1])
