import cv2
import yaml
import numpy as np

from vision_project.vision.util import WorldCoordinate


class DistanceCalculator:

    def __init__(self):
        with open('/cameracalibration/distance_calibration_hi_res.yaml') as f:
            loaded_dict = yaml.load(f)
        with open('/cameracalibration/camera_calibration_hi_res.yaml') as f2:
            loaded_dict2 = yaml.load(f2)
        self.iR = loaded_dict.get('inverse_rotation_matrix')
        self.iR = np.asarray(self.iR)
        self.C = loaded_dict2.get('camera_matrix')
        self.C = np.asarray(self.C)
        self.iC = loaded_dict.get('inverse_camera_matrix')
        self.iC = np.asarray(self.iC)
        self.D = loaded_dict2.get('dist_coeff')
        self.D = np.asarray(self.D)
        self.tvec = loaded_dict.get('tvec')
        self.tvec = np.asarray(self.tvec)
        self.rvec = loaded_dict.get('rvec')
        self.rvec = np.asarray(self.rvec)

    def convert_undistorted_pixel_x_y_z_to_real_point(self, x, y, z):
        uv_point = np.array([x, y, np.ones(shape=1)]).reshape(3, 1)
        t = self.iR.dot(self.iC).dot(uv_point)
        t2 = self.iR.dot(self.tvec)
        s = (t2[2]) / t[2]
        object_point = (self.iR.dot(s.item(0) * self.iC.dot(uv_point) - self.tvec))
        return WorldCoordinate(object_point.item(0), object_point.item(1))

    def convert_undistorted_point_x_y_to_pixel(self, point):
        uv_point = np.array([point.get_x().to_millimeters(), point.get_y().to_millimeters(), np.zeros(shape=1)]).reshape(1, 3)
        data = cv2.projectPoints(uv_point, self.rvec, self.tvec, self.C, self.D)[0]
        x = data[0][0][0]
        y = data[0][0][1]
        return x, y

