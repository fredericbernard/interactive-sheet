from jivago.lang.annotations import BackgroundWorker, Override, Inject
from jivago.lang.runnable import Runnable

from vision_project.projection.projector_window import ProjectorWindow


@BackgroundWorker
class GuiWorker(Runnable):

    @Inject
    def __init__(self, main_window: ProjectorWindow):
        self.main_window = main_window

    @Override
    def run(self):
        self.main_window.main()
