from vision_project.vision.util import CameraCoordinate


class Sheet(object):

    def __init__(self, origin: CameraCoordinate, oposite_corner: CameraCoordinate):
        self.origin = origin
        self.oposite_corner = oposite_corner
