from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.jivago_application import JivagoApplication
from jivago.lang.annotations import Override

import vision_project
from vision_project.vision.coordinate_converter import CalibratedCoordinateTranslator
from vision_project.vision.coordinate_translator import CoordinateTranslator, DummyCoordinateTranslator
from vision_project.vision.image_repository import ImageRepository, SimpleImageRepository


class CameraCaptureContext(ProductionJivagoContext):

    @Override
    def configure_service_locator(self):
        super().configure_service_locator()
        repository = SimpleImageRepository()
        self.serviceLocator.bind(ImageRepository, repository)
        self.serviceLocator.bind(CoordinateTranslator, CalibratedCoordinateTranslator)


app = JivagoApplication(vision_project, context=CameraCaptureContext)

if __name__ == "__main__":
    app.run_dev()
