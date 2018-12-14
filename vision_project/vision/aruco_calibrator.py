import os
import threading

import cv2
from cv2 import aruco
from time import sleep

import PIL
import numpy as np
import yaml
from PIL import ImageTk
from jivago.lang.annotations import Inject
from numpy.linalg import inv

import vision_project
from vision_project.projection.projector_window import ProjectorWindow
from vision_project.vision.image_repository import ImageRepository, LiveCapture


class ArucoCalibrator(object):

    @Inject
    def __init__(self, projector_window: ProjectorWindow, image_repository: ImageRepository):
        self.image_repository = image_repository
        self.projector_window = projector_window
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

    def show_aruco(self):
        image = aruco.drawMarker(self.aruco_dict, 3, 600)

        photo = ImageTk.PhotoImage(image=PIL.Image.fromarray(image))

        self.projector_window.canvas.create_image(500, 400, image=photo)
        return np.array([[500 + 300, 400 + 300], [500 + 300, 400 - 300], [500 - 300, 400 - 300],
                         [500 - 300, 400 + 300]], dtype=np.float32)

    def detect_aruco(self):
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

    ret, rvec, tvec = cv2.solvePnP(corners_on_projector, corners_on_image, camera_matrix, distance_coefficients)
    rotation_vector = cv2.Rodrigues(rvec)[0]
    rotation_matrix = np.matrix(rotation_vector)
    iR = inv(rotation_matrix)
    write_distance_calibration_file(iR, iC, tvec)


if __name__ == '__main__':
    window = ProjectorWindow()
    thread = threading.Thread(target=window.main)
    thread.start()
    capture = LiveCapture("/dev/video0")
    calibrator = ArucoCalibrator(window, capture)

    corners_camera = calibrator.show_aruco()

    corners_projector = []
    sleep(5)
    while not corners_projector:
        capture.get_next_image().show_do_not_close()
        corners_projector = calibrator.detect_aruco()
        print(corners_projector)

    # array = []
    # for i in corners_projector[0][0]:
    #     array.append([i[0], i[1], 0])
    calibrate(corners_projector[0], corners_camera)

    def draw_circle(canvas, x, y, rad):
        return canvas.create_oval(x - rad, y - rad, x + rad, y + rad, width=0, fill='blue')

