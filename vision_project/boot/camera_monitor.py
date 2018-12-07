from jivago.config.startup_hooks import PostInit
from jivago.lang.annotations import Override, Inject
from jivago.lang.runnable import Runnable

from vision_project.vision.image_repository import ImageRepositoryObserver, ImageRepository, SimpleImageRepository


@PostInit
class CameraMonitor(Runnable, ImageRepositoryObserver):

    @Inject
    def __init__(self, image_repository: ImageRepository):
        self.image_repository: SimpleImageRepository = image_repository

    @Override
    def notify(self):
        self.image_repository.get_next_image().show_do_not_close()

    @Override
    def run(self):
        self.image_repository.register(self)
