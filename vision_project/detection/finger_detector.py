from typing import Optional

from jivago.lang.registry import Component

from vision_project.detection.finger import Finger
from vision_project.vision.image import Image


@Component
class FingerDetector(object):

    def find_finger(self, image: Image) -> Optional[Finger]:
        pass
