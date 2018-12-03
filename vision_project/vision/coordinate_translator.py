from jivago.lang.annotations import Override

from vision_project.vision.util import CameraCoordinate, RelativeWorldCoordinate, ProjectorCoordinate, PixelCoordinate


class CoordinateTranslator(object):

    def to_projector(self, origin: CameraCoordinate,
                     relative_coordinate: RelativeWorldCoordinate) -> ProjectorCoordinate:
        raise NotImplementedError


class DummyCoordinateTranslator(CoordinateTranslator):

    @Override
    def to_projector(self, origin: CameraCoordinate,
                     relative_coordinate: RelativeWorldCoordinate) -> ProjectorCoordinate:
        return origin + PixelCoordinate(int(relative_coordinate.x), int(relative_coordinate.y))
