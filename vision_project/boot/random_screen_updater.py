from jivago.lang.annotations import Override, Inject
from jivago.lang.runnable import Runnable
from jivago.scheduling.annotations import Scheduled, Duration

from vision_project.drawing.drawing import Drawing
# TODO remove when happy with behaviour
from vision_project.vision.util import RelativeWorldCoordinate


# @Scheduled(every=Duration.SECOND)
class RandomScreenUpdater(Runnable):

    @Inject
    def __init__(self, drawing: Drawing):
        self.drawing = drawing

    @Override
    def run(self):
        self.drawing.clear()
        self.drawing.draw_line(RelativeWorldCoordinate(0, 0), RelativeWorldCoordinate(20, 20))
        self.drawing.draw_line(RelativeWorldCoordinate(20, 0), RelativeWorldCoordinate(0, 20))
