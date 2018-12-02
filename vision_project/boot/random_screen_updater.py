import random

from jivago.lang.annotations import Override, Inject
from jivago.lang.runnable import Runnable
from jivago.scheduling.annotations import Scheduled, Duration

from vision_project.projection.projector_window import ProjectorWindow


# TODO remove when happy with behaviour

@Scheduled(every=Duration.SECOND)
class RandomScreenUpdater(Runnable):

    @Inject
    def __init__(self, projector_window: ProjectorWindow):
        self.projector_window = projector_window

    @Override
    def run(self):
        colours = ['black', 'blue', 'pink', 'red', 'green', 'gray', 'magenta', 'purple', 'teal']
        random.shuffle(colours)
        colour = colours[0]
        self.projector_window.canvas.create_line(random.randint(0, 600), random.randint(0, 600), random.randint(0, 600),
                                                 random.randint(0, 600), fill=colour, width=random.randint(1, 5))
        if random.randint(0, 25) > 22:
            self.projector_window.canvas.delete('all')
