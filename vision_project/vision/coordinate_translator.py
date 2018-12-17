from jivago.lang.annotations import Override

from vision_project.vision.util import CameraCoordinate, ProjectorCoordinate


class CoordinateTranslator(object):

    def to_projector(self, point: CameraCoordinate) -> ProjectorCoordinate:
        raise NotImplementedError


class DummyCoordinateTranslator(CoordinateTranslator):

    @Override
    def to_projector(self, point: CameraCoordinate) -> ProjectorCoordinate:
        return point
