import threading
from time import sleep

import os
import PIL
import cv2
import yaml
import numpy as np
from jivago.lang.stream import Stream

from numpy.linalg import inv
from PIL import ImageTk
import cv2.aruco as aruco
from jivago.lang.annotations import Inject

import infra
import vision_project
from vision_project.projection.projector_window import ProjectorWindow
from vision_project.vision.coordinate_converter import CalibratedCoordinateTranslator
from vision_project.vision.image_repository import ImageRepository, LiveCapture
from vision_project.vision.util import PixelCoordinate


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
        return np.array([[150, 50, 0], [850, 50, 0], [850, 750, 0], [150, 750, 0]], dtype=np.float32)

    def detect_aruco(self):
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

        image = self.image_repository.get_next_image()
        gray = cv2.cvtColor(image.frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict,
                                                              parameters=aruco.DetectorParameters_create())
        return corners


def write_distance_calibration_file(inverse_rotation_matrix, inverse_camera_matrix, translation_vector):
    data = {'inverse_rotation_matrix': np.asarray(inverse_rotation_matrix).tolist(),
            'inverse_camera_matrix': np.asarray(inverse_camera_matrix).tolist(),
            'tvec': np.asarray(translation_vector).tolist()}

    with open(os.path.join(os.path.dirname(vision_project.vision.__file__), 'config/distance_calibration.yaml'),
              'w') as f:
        yaml.dump(data, f)


def calibrate(corners_on_image, corners_on_projector):
    with open(os.path.join(os.path.dirname(vision_project.vision.__file__), 'config/camera_calibration.yaml')) as f:
        loaded_dict = yaml.load(f)

    distance_coefficients = loaded_dict.get('dist_coeff')
    distance_coefficients = np.asarray(distance_coefficients)
    camera_matrix = loaded_dict.get('camera_matrix')
    camera_matrix = np.asarray(camera_matrix)
    cameraMatrix = np.matrix(camera_matrix)
    iC = inv(cameraMatrix)

    ret, rvec, tvec = cv2.solvePnP(corners_on_image, corners_on_projector, camera_matrix, distance_coefficients)
    rotation_vector = cv2.Rodrigues(rvec)[0]
    rotation_matrix = np.matrix(rotation_vector)
    iR = inv(rotation_matrix)
    write_distance_calibration_file(iR, iC, tvec)


if __name__ == '__main__':
    window = ProjectorWindow()
    thread = threading.Thread(target=window.main)
    thread.start()

    calibrator = ArucoCalibrator(window, LiveCapture("/dev/video0"))

    corners_camera = calibrator.show_aruco()

    corners_projector = []
    sleep(2)
    while not corners_projector:
        sleep(1)
        corners_projector = calibrator.detect_aruco()
        print("corners_projector", corners_projector)

    print("camera_corners", corners_camera)

    calibrate(corners_camera, corners_projector[0])


    def draw_circle(canvas, x, y, rad):
        return canvas.create_oval(x - rad, y - rad, x + rad, y + rad, width=0, fill='blue')


    converter = CalibratedCoordinateTranslator()
    Stream(corners_projector[0][0]).map(lambda x, y: PixelCoordinate(x, y)).map(lambda x: converter.to_projector(x)).forEach(
        lambda p: draw_circle(window.canvas, p.x, p.y, 10))

    # draw_circle(window.canvas, 850, 750, 10)
