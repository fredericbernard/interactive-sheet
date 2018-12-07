import cv2
import yaml
import numpy as np
import os

import vision_project
from vision_project.vision.util import WorldCoordinate


class DistanceCalculator:

    def __init__(self):
        config_file_path = os.path.dirname(vision_project.vision.__file__)
        with open(os.path.join(config_file_path, 'config/distance_calibration.yaml')) as distance_calibration_file:
            camera_calibration = yaml.load(distance_calibration_file)
        with open(os.path.join(config_file_path, 'config/camera_calibration.yaml')) as camera_calibration_file:
            distance_calibration = yaml.load(camera_calibration_file)

        self.inverse_rotation_matrix = camera_calibration.get('inverse_rotation_matrix')
        self.inverse_rotation_matrix = np.asarray(self.inverse_rotation_matrix)

        self.camera_matrix = distance_calibration.get('camera_matrix')
        self.camera_matrix = np.asarray(self.camera_matrix)
        self.inverse_camera_matrix = camera_calibration.get('inverse_camera_matrix')

        self.inverse_camera_matrix = np.asarray(self.inverse_camera_matrix)

        self.distance_coefficients = distance_calibration.get('dist_coeff')
        self.distance_coefficients = np.asarray(self.distance_coefficients)

        self.translation_vector = camera_calibration.get('tvec')
        self.translation_vector = np.asarray(self.translation_vector)

    def convert_undistorted_pixel_x_y_to_real_point(self, x, y):
        uv_point = np.array([x, y, np.ones(shape=1)]).reshape(3, 1)
        t = self.inverse_rotation_matrix.dot(self.inverse_camera_matrix).dot(uv_point)
        t2 = self.inverse_rotation_matrix.dot(self.translation_vector)
        s = (t2[2]) / t[2]
        object_point = (self.inverse_rotation_matrix.dot(s.item(0) * self.inverse_camera_matrix.dot(uv_point) - self.translation_vector))
        return WorldCoordinate(object_point.item(0), object_point.item(1))

    def convert_undistorted_point_x_y_to_pixel(self, point):
        uv_point = np.array([point.get_x().to_millimeters(), point.get_y().to_millimeters(), np.zeros(shape=1)]).reshape(1, 3)
        data = cv2.projectPoints(uv_point, self.rvec, self.translation_vector, self.camera_matrix, self.distance_coefficients)[0]
        x = data[0][0][0]
        y = data[0][0][1]
        return x, y

