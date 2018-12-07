import threading
from time import sleep

import PIL
import cv2
from PIL import ImageTk
from cv2 import aruco
from jivago.lang.annotations import Inject

from vision_project.projection.projector_window import ProjectorWindow
from vision_project.vision.image_repository import ImageRepository, LiveCapture


class ArucoCalibrator(object):

    @Inject
    def __init__(self, projector_window: ProjectorWindow, image_repository: ImageRepository):
        self.image_repository = image_repository
        self.projector_window = projector_window

    def show_aruco(self):
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

        image = aruco.drawMarker(aruco_dict, 3, 700)

        photo = ImageTk.PhotoImage(image=PIL.Image.fromarray(image))

        self.projector_window.canvas.create_image(500, 400, image=photo)

    def detect_aruco(self):
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

        image = self.image_repository.get_next_image()
        gray = cv2.cvtColor(image.frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict,
                                                              parameters=aruco.DetectorParameters_create())

        print(corners)


if __name__ == '__main__':
    window = ProjectorWindow()
    calibrator = ArucoCalibrator(window, LiveCapture("/dev/video0"))

    thread = threading.Thread(target=window.main)

    thread.start()
    calibrator.show_aruco()

    while True:
        sleep(5)
        calibrator.detect_aruco()
