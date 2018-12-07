import logging
import time
from jivago.lang.annotations import BackgroundWorker, Inject, Override
from jivago.lang.runnable import Runnable

from vision_project.drawing.drawing import Drawing
from vision_project.vision.image_repository import ImageRepository


@BackgroundWorker
class FingerDrawingWorker(Runnable):

    LOGGER = logging.getLogger("FingerDrawingWorker")

    @Inject
    def __init__(self, image_repository: ImageRepository, drawing: Drawing):
        self.drawing = drawing
        self.image_repository = image_repository
        self.should_exit = False

    @Override
    def run(self):
        while not self.should_exit:
            # TODO : Prendre deux images, comparer le delta position du doigt, dessiner une ligne sur drawing
            time.sleep(0.25)

    def cleanup(self):
        self.should_exit = True
